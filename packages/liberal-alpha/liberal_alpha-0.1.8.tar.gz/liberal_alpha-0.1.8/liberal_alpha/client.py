#!/usr/bin/env python3
import grpc
import json
import time
import threading
import logging
import asyncio
import requests 
import argparse
import os
import sys  # 新增：用于 HTTP 请求

from .exceptions import ConnectionError, RequestError
from .proto import service_pb2, service_pb2_grpc
from .subscriber import main_async
from .crypto import get_wallet_address

logger = logging.getLogger(__name__)

class LiberalAlphaClient:
    """
    Liberal Alpha SDK Client for sending data via gRPC, subscribing to WebSocket data,
    and fetching user's record information.

    Parameters:
      - host (optional, default "127.0.0.1")
      - port (optional, default 8128)
      - rate_limit_enabled (optional, default True)
      - api_key (optional; required for subscribing and fetching records)
      - private_key (optional; required for subscribing)

    The wallet address is automatically computed from the private key.
    The base URL is fixed to "https://api.liberalalpha.com" (will be updated later).
    """
    
    def __init__(self, host=None, port=None, rate_limit_enabled=None, api_key=None, private_key=None):
        self.host = host if host is not None else "127.0.0.1"
        self.port = port if port is not None else 8128
        self.rate_limit_enabled = rate_limit_enabled if rate_limit_enabled is not None else True
        self.api_key = api_key
        self.private_key = private_key
        # Wallet is computed automatically from private_key (if provided)
        self.wallet = get_wallet_address(private_key) if private_key else None
        # Base URL is fixed
        self.base_url = "https://api.liberalalpha.com"
        self._lock = threading.Lock()
        try:
            self.channel = grpc.insecure_channel(f"{self.host}:{self.port}")
            self.stub = service_pb2_grpc.JsonServiceStub(self.channel)
            grpc.channel_ready_future(self.channel).result(timeout=5)
        except grpc.RpcError as e:
            raise ConnectionError(details=str(e))
    
    def send_data(self, identifier: str, data: dict, record_id: str):
        """
        Send data via gRPC.
        This method does not require API key and private key checks.
        If the request fails, it is likely that no runner is running.
        """
        try:
            return self._send_request(identifier, data, "raw", record_id)
        except grpc.RpcError as e:
            raise RequestError(
                message="Failed to send gRPC request. No runner is running. Please start the runner.",
                code=e.code().value if e.code() else None,
                details=str(e.details())
            )
    
    def send_alpha(self, identifier: str, data: dict, record_id: str):
        """
        Send alpha signal via gRPC.
        This method does not require API key and private key checks.
        If the request fails, it is likely that no runner is running.
        """
        try:
            return self._send_request(identifier, data, "raw", record_id)
        except grpc.RpcError as e:
            raise RequestError(
                message="Failed to send gRPC request. No runner is running. Please start the runner.",
                code=e.code().value if e.code() else None,
                details=str(e.details())
            )
    
    def _send_request(self, identifier: str, data: dict, event_type: str, record_id: str):
        # Check if host and port are provided; if not, raise an error.
        if not self.host or not self.port:
            raise ValueError("Client is missing host and port parameters")
        
        with self._lock:
            current_time_ms = int(time.time() * 1000)
            metadata = {
                "source": "liberal_alpha_sdk",
                "entry_id": identifier,
                "record_id": record_id,
                "timestamp_ms": str(current_time_ms)
            }
            request = service_pb2.JsonRequest(
                json_data=json.dumps(data),
                event_type=event_type,
                timestamp=current_time_ms,
                metadata=metadata
            )
            response = self.stub.ProcessJson(request)
            logger.info(f"gRPC Response: {response}")
            return {
                "status": response.status,
                "message": response.message,
                "result": json.loads(response.result_json) if response.result_json else None,
                "error": response.error if response.error else None
            }
    
    def subscribe_data(self, record_id=None, max_reconnect=5, on_message: callable = None):
        """
        Subscribe to real-time data via WebSocket.
        This method requires that both API key and private key are provided.
        If record_id is provided, subscribe to that record only.
        Otherwise, continuously poll for new subscribed records.
        """
        if not self.api_key or not self.private_key:
            logger.error("API key and private key must be provided for subscribing to data.")
            return
        try:
            asyncio.run(
                main_async(api_key=self.api_key, base_url=self.base_url, wallet_address=self.wallet,
                           private_key=self.private_key, record_id=record_id,
                           max_reconnect=max_reconnect, on_message=on_message)
            )
        except KeyboardInterrupt:
            logger.info("Subscription interrupted by user")
        except Exception as e:
            logger.error(f"Error during subscription: {e}")
    
    def my_records(self):
        """
        Fetch the records associated with the current API key by calling the backend endpoint /api/records.
        Returns the records as parsed JSON, or None if fetching fails.
        """
        if not self.api_key:
            logger.error("API key is required to fetch records.")
            return None
        url = f"{self.base_url}/api/records"
        headers = {"X-API-Key": self.api_key}
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                records = response.json()
                return records
            else:
                logger.error(f"Failed to fetch records: HTTP {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"Error fetching records: {e}")
            return None
        
    def my_subscriptions(self):
        """
        Fetch the subscriptions associated with the current API key by calling the backend endpoint /api/subscriptions.
        Returns the subscriptions as parsed JSON, or None if fetching fails.
        """
        if not self.api_key:
            logger.error("API key is required to fetch subscriptions.")
            return None
        url = f"{self.base_url}/api/subscriptions"
        headers = {"X-API-Key": self.api_key}
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                subscriptions = response.json()
                return subscriptions
            else:
                logger.error(f"Failed to fetch subscriptions: HTTP {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"Error fetching subscriptions: {e}")
            return None

    def my_historical_entries(self, record_id: int, page: int = 1, page_size: int = 10):
        """
        Fetch historical subscription data (entries) for a given record by calling the /api/entries/history endpoint.
        
        Args:
            record_id (int): The record ID for which to fetch historical data.
            page (int): The page number (default is 1).
            page_size (int): Number of entries per page (default is 10).

        Returns:
            dict or None: Parsed JSON data if success; otherwise, None.
        """
        if not self.api_key:
            logger.error("API key is required to fetch historical entries.")
            return None
        
        url = f"{self.base_url}/api/entries/history"
        headers = {"X-API-Key": self.api_key}
        params = {
            "record_id": record_id,
            "page": page,
            "page_size": page_size
        }
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get("status", "").lower() == "success":
                    return data.get("data")
                else:
                    logger.error(f"API error: {data.get('message', 'Unknown error')}")
                    return None
            else:
                logger.error(f"Failed to fetch historical entries: HTTP {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"Error fetching historical entries: {e}")
            return None

liberal = None

def initialize(host=None, port=None, rate_limit_enabled=None, api_key=None, private_key=None):
    global liberal
    liberal = LiberalAlphaClient(host, port, rate_limit_enabled, api_key, private_key)
    logger.info(f"SDK initialized: liberal={liberal}")

def main():
    parser = argparse.ArgumentParser(
        prog="liberal_alpha",
        description="Liberal Alpha CLI - interact with gRPC backend & WebSocket stream"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Send data
    send_parser = subparsers.add_parser("send", help="Send data via gRPC")
    send_parser.add_argument("--id", required=True, help="Record ID (entry_id)")
    send_parser.add_argument("--data", required=True, help="Data in JSON format")
    send_parser.add_argument("--record", required=True, help="Record ID")

    # Show records
    subparsers.add_parser("records", help="List your records")

    # Show subscriptions
    subparsers.add_parser("subscriptions", help="List your subscriptions")

    # Subscribe
    sub_parser = subparsers.add_parser("subscribe", help="Subscribe to data")
    sub_parser.add_argument("--record", help="Specific record ID (optional)")

    # Fetch historical entries
    history_parser = subparsers.add_parser("history", help="Fetch historical subscription data for a record")
    history_parser.add_argument("--record", required=True, help="Record ID")
    history_parser.add_argument("--page", type=int, default=1, help="Page number (default: 1)")
    history_parser.add_argument("--page_size", type=int, default=10, help="Number of entries per page (default: 10)")

    # Show version
    subparsers.add_parser("version", help="Show CLI version")

    args = parser.parse_args()

    # 从环境变量读取 API key 和 private key
    api_key = os.environ.get("LIBALPHA_API_KEY")
    private_key = os.environ.get("LIBALPHA_PRIVATE_KEY")

    # 初始化 client
    global liberal
    initialize(api_key=api_key, private_key=private_key)

    if args.command == "send":
        try:
            data = json.loads(args.data)
            result = liberal.send_data(identifier=args.id, data=data, record_id=args.record)
            print("✅ Send result:", json.dumps(result, indent=2))
        except Exception as e:
            print("❌ Error sending data:", e)
            sys.exit(1)

    elif args.command == "records":
        records = liberal.my_records()
        print(json.dumps(records, indent=2) if records else "No records found.")

    elif args.command == "subscriptions":
        subs = liberal.my_subscriptions()
        print(json.dumps(subs, indent=2) if subs else "No subscriptions found.")

    elif args.command == "subscribe":
        liberal.subscribe_data(record_id=args.record)

    elif args.command == "history":
        try:
            record_id = int(args.record)
        except ValueError:
            print("Record ID must be an integer.")
            sys.exit(1)
        historical_data = liberal.my_historical_entries(record_id, page=args.page, page_size=args.page_size)
        if historical_data:
            print(json.dumps(historical_data, indent=2))
        else:
            print("No historical data found or an error occurred.")

    elif args.command == "version":
        print("Liberal Alpha CLI v0.1.7")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()

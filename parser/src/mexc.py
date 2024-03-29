"""MEXC tickers parser"""
import hashlib
import hmac

import httpx
from src.endpoints import NEW_ORDER_ENDPOINT
from src.utils import get_mexc_timestamp

from consts import needle


class MexcClient:
    """HTTP Client to interact with MEXC API"""

    def __init__(
            self,
            api_key: str,
            api_secret: str,
            base_url: str = "https://api.mexc.com",
            recv_window: int = 5000
    ):
        self.api_key = api_key
        self.api_secret = api_secret

        self.base_url = base_url
        self.recv_window = recv_window

        self.client = httpx.Client(http2=True)
        self.headers = {
            "Content-Type": "application/json",
            "X-MEXC-APIKEY": self.api_key
        }

    def __get_query(self, params: dict) -> str:
        """Returns a query string of all given parameters"""
        query = ""
        for key, value in params.items():
            query += f"{key}={value}&"
        return query[:-1]

    def __get_signature(self, query: str) -> str:
        """Returns the signature based on the api secret and the query."""
        return hmac.new(
            self.api_secret.encode("utf-8"), query.encode("utf-8"), hashlib.sha256
        ).hexdigest()

    def __send_request(
            self, endpoint: str, params: dict, sign: bool = True
    ) -> dict:
        """Sends a request with the given method to the given endpoint."""

        if sign:
            params["recvWindow"] = self.recv_window
            params["timestamp"] = get_mexc_timestamp()
            params["signature"] = self.__get_signature(self.__get_query(params))

        response = self.client.post(
            url=self.base_url + endpoint,
            params=params,
            headers=self.headers
        )

        # if response.status_code != 200:
        #     raise MexcAPIError(response.status_code, response.json().get("msg"))

        return response.json()

    def new_order(self, params):
        updated_params = params
        updated_params['price'] = '{:.8f}'.format(float(params['price']))
        print(updated_params)
        return self.__send_request(NEW_ORDER_ENDPOINT, params)

    def get_tickers(self) -> dict | None:
        """Returns all tickers list"""
        try:
            url = "https://api.mexc.com/api/v3/ticker/bookTicker"
            response = self.client.get(url, headers=self.headers)
            return response.json()
        except Exception as error:
            print(f"Ошибка получения тикеров: {error}")
            return None

    @staticmethod
    def filter_tickers(tickers: dict) -> dict:
        """Restructure of list with all tickers"""
        result = {}
        for ticker in tickers:
            # Skip other tickers
            if ticker['symbol'] not in needle:
                continue

            result[ticker['symbol']] = {
                'ask': float(ticker['askPrice']),
                'bid': float(ticker['bidPrice']),
                'ask_size': float(ticker['askQty']),
                'bid_size': float(ticker['bidQty']),
            }

        return result

    def get_data(self) -> dict | None:
        """Returns info about all needle tickers"""
        tickers = self.get_tickers()

        if not tickers:
            return None

        data = self.filter_tickers(tickers)
        return data

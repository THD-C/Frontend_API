from csv import excel

from google.protobuf.json_format import MessageToDict
from fastapi import APIRouter, HTTPException, Request, Query
from grpc import RpcError
from datetime import datetime, timedelta
from pydantic import BaseModel
from enum import Enum

from src.connections import currency_stub
from currency import currency_pb2, currency_type_pb2
from src.connections import prices_stub
from coins import coins_pb2
from src.router.currency import get_currency_type

from src.utils.logger import logger
from src.utils.auth import verify_user

crypto_router = APIRouter(tags=["Crypto data"])


@crypto_router.get("/details", responses={
    500: {
        "description": "Problems occurred inside the server",
        "content": {
            "application/json": {
                "example": {"detail": "internal_server_error"}
            }
        }
    },
    400: {
        "description": "Invalid data passed to endpoint",
        "content": {
            "application/json": {
                "example": {"detail": "invalid_data"}

            }
        }
    },
    401: {
        "description": "Authorization failure",
        "content": {
            "application/json": {
                "example": [{"detail": "no_authorization_header"},
                            {"detail": "invalid_auth_scheme"},
                            {"detail": "invalid_token"},
                            {"detail": "expired_token"},
                            {"detail": "unauthorized_user_for_method"}
                            ]

            }
        }
    },
    200: {
        "description": "Details of cryptocurrency in fiat currency specified in params",
        "content": {
            "application/json": {
                "example": {
                    "status": "success",
                    "data": {
                        "id": "bitcoin",
                        "market_data": {
                            "price_change_percentage_24h_in_currency": -3.806,
                            "total_volume": 197255869075.0,
                            "high_24h": 409703.0,
                            "market_cap": 7735883719797.0,
                            "current_price": 390614.0,
                            "low_24h": 390175.0,
                            "price_change_24h_in_currency": -15454.95814470714
                        },
                        "symbol": "btc",
                        "name": "Bitcoin"
                    },
                    "error_message": "",
                    "values_in_currency": "pln"
                }
            }
        }
    }
}, description='Returns details of cryptocurrency in fiat currency specified in params')
def get_crypto_details(
        request: Request,
        coin_id: str = Query(..., description="Name of crypto for which data will be received"),
        currency: str = Query("usd", description="Currency code in which data will be received")):
    auth_header = request.headers.get("Authorization")
    verify_user(auth_header)

    if coin_id == "":
        raise HTTPException(status_code=400,
                            detail="invalid_data")

    currency_type = get_currency_type(currency)
    currency_type = currency_type["currency_type"]
    currency_crypto_type = get_currency_type(coin_id)
    currency_crypto_type = currency_crypto_type["currency_type"]

    if currency_type != "FIAT" or currency_crypto_type != "CRYPTO" or \
            currency_type == "NOT_SUPPORTED" or \
            currency_crypto_type == "NOT_SUPPORTED":
        raise HTTPException(status_code=400,
                            detail="invalid_data")

    try:
        coin_details_message: coins_pb2.CoinDataRequest = coins_pb2.CoinDataRequest(coin_id=coin_id,
                                                                                    fiat_currency=currency)
        response: coins_pb2.DataResponse = prices_stub.GetCoinData(coin_details_message)
    except RpcError as e:
        logger.error("gRPC error details:", e)
        raise HTTPException(status_code=500,
                            detail="internal_server_error")

    if response.status == "success":
        logger.info("Details for ", coin_id, " retrieved successfully")
        endpoint_response = MessageToDict(response,
                                          preserving_proto_field_name=True,
                                          always_print_fields_with_no_presence=True)
        endpoint_response["values_in_currency"] = currency
        return endpoint_response
    else:
        logger.error("Coin details error: ", response.status, " with message: ", response.error_message)
        raise HTTPException(status_code=500,
                            detail="internal_server_error")


@crypto_router.get("/historical-data", responses={
    500: {
        "description": "Problems occurred inside the server",
        "content": {
            "application/json": {
                "example": {"detail": "internal_server_error"}
            }
        }
    },
    400: {
        "description": "Invalid data passed to endpoint",
        "content": {
            "application/json": {
                "example": {"detail": "invalid_data"}

            }
        }
    },
    401: {
        "description": "Authorization failure",
        "content": {
            "application/json": {
                "example": [{"detail": "no_authorization_header"},
                            {"detail": "invalid_auth_scheme"},
                            {"detail": "invalid_token"},
                            {"detail": "expired_token"},
                            {"detail": "unauthorized_user_for_method"}
                            ]

            }
        }
    },
    200: {
        "description": "Historical data of cryptocurrency in fiat currency specified in params",
        "content": {
            "application/json": {
                "example": [{
                    "status": "success",
                    "data": {
                        "timestamp": [
                            1735162568042,
                            1735162873987,
                            1735163178020,
                            1735244446553,
                            1735244776319,
                            1735245056234
                        ],
                        "price": [
                            98379.61165801862,
                            98458.46152136194,
                            98342.98185484544,
                            95435.01407619793,
                            95358.78646932913,
                            95472.464093301
                        ]
                    },
                    "error_message": "",
                    "values_in_currency": "usd"
                },
                    {
                        "status": "success",
                        "data": {
                            "close": [
                                93734,
                                93788,
                                93820,
                                93937
                            ],
                            "low": [
                                93734,
                                93788,
                                93820,
                                93637
                            ],
                            "open": [
                                94011,
                                93810,
                                93822,
                                93834
                            ],
                            "high": [
                                94215,
                                94054,
                                94145,
                                93937
                            ],
                            "timestamp": [
                                1735669800000,
                                1735671600000,
                                1735673400000,
                                1735675200000
                            ]
                        },
                        "error_message": "",
                        "values_in_currency": "usd"
                    }
                ]
            }
        }
    }
}, description='Returns historical data of cryptocurrency in fiat currency specified in params')
def get_crypto_historical_data(
        request: Request,
        coin_id: str = Query(..., description="Name of crypto for which data will be received"),
        currency: str = Query("usd", description="Currency code in which data will be received"),
        start_date: datetime = Query(datetime.now() - timedelta(days=1), description="Start date for historical data"),
        end_date: datetime = Query(datetime.now(), description="End date for historical data"),
        ohlc_data: bool = Query(False, description="Specifies if data should be in OHLC format"),
):
    auth_header = request.headers.get("Authorization")
    verify_user(auth_header)

    if coin_id == "":
        raise HTTPException(status_code=400,
                            detail="invalid_data")

    currency_type = get_currency_type(currency)
    currency_type = currency_type["currency_type"]
    currency_crypto_type = get_currency_type(coin_id)
    currency_crypto_type = currency_crypto_type["currency_type"]

    if currency_type != "FIAT" or currency_crypto_type != "CRYPTO" or \
            currency_type == "NOT_SUPPORTED" or \
            currency_crypto_type == "NOT_SUPPORTED" or \
            end_date < start_date or \
            start_date > datetime.today() or \
            end_date > datetime.today():
        raise HTTPException(status_code=400,
                            detail="invalid_data")

    coin_details_message: coins_pb2.HistoricalDataRequest = coins_pb2.HistoricalDataRequest(coin_id=coin_id,
                                                                                            fiat_currency=currency,
                                                                                            start_date=start_date,
                                                                                            end_date=end_date)

    try:
        if ohlc_data:
            response: coins_pb2.DataResponse = prices_stub.GetHistoricalCandleData(coin_details_message)
        else:
            response: coins_pb2.DataResponse = prices_stub.GetHistoricalData(coin_details_message)
    except RpcError as e:
        logger.error("gRPC error details:", e)
        raise HTTPException(status_code=500,
                            detail="internal_server_error")

    if response.status == "success":
        logger.info("Details for ", coin_id, " retrieved successfully")
        endpoint_response = MessageToDict(response,
                                          preserving_proto_field_name=True,
                                          always_print_fields_with_no_presence=True)
        endpoint_response["values_in_currency"] = currency
        return endpoint_response
    else:
        logger.error("Coin details error: ", response.status, " with message: ", response.error_message)
        raise HTTPException(status_code=500,
                            detail="internal_server_error")


@crypto_router.get("/coins", responses={
    500: {
        "description": "Problems occurred inside the server",
        "content": {
            "application/json": {
                "example": {"detail": "internal_server_error"}
            }
        }
    },
    400: {
        "description": "Invalid data passed to endpoint",
        "content": {
            "application/json": {
                "example": {"detail": "invalid_data"}

            }
        }
    },
    401: {
        "description": "Authorization failure",
        "content": {
            "application/json": {
                "example": [{"detail": "no_authorization_header"},
                            {"detail": "invalid_auth_scheme"},
                            {"detail": "invalid_token"},
                            {"detail": "expired_token"},
                            {"detail": "unauthorized_user_for_method"}
                            ]

            }
        }
    },
    200: {
        "description": "List of crypto with most important details",
        "content": {
            "application/json": {
                "example": {
                    "coins": [
                        {
                            "ethereum": {
                                "id": "ethereum",
                                "market_data": {
                                    "total_volume": 19154744209.0,
                                    "price_change_percentage_24h_in_currency": -2.10623,
                                    "high_24h": 3422.37,
                                    "market_cap": 403511146186.0,
                                    "current_price": 3348.83,
                                    "low_24h": 3299.88,
                                    "price_change_24h_in_currency": -72.05169091567541
                                },
                                "symbol": "eth",
                                "name": "Ethereum"
                            }
                        },
                        {
                            "tether": {
                                "id": "tether",
                                "market_data": {
                                    "total_volume": 61240126683.0,
                                    "price_change_percentage_24h_in_currency": -0.06587,
                                    "high_24h": 1.0,
                                    "market_cap": 138775884877.0,
                                    "current_price": 0.998231,
                                    "low_24h": 0.993855,
                                    "price_change_24h_in_currency": -0.000658007502949864
                                },
                                "symbol": "usdt",
                                "name": "Tether"
                            }
                        }]
                }
            }
        }
    }
}, description='Returns list of supported cryptocurrencies with most important details for display')
def get_list_of_coins(request: Request,
                      currency: str = Query('usd', description="Currency code in which data will be received")
                      ):
    auth_header = request.headers.get("Authorization")
    verify_user(auth_header)

    currency_type = get_currency_type(currency)
    currency_type = currency_type["currency_type"]

    if currency_type != "FIAT":
        logger.error("Currency is not supported or cryptocurrency. List of coins must be in FIAT")
        raise HTTPException(status_code=400,
                            detail="invalid_data")

    try:
        coins_list_message: coins_pb2.ListDataForAllCoinsRequest = coins_pb2.ListDataForAllCoinsRequest(
            fiat_currency=currency)

        response: coins_pb2.ListDataForAllCoinsResponse = prices_stub.GetListDataForAllCoins(coins_list_message)
    except RpcError as e:
        logger.error("gRPC error details:", e)
        raise HTTPException(status_code=500,
                            detail="internal_server_error")

    if response.status == "success" and len(response.data) != 0:
        logger.info("Fetched list of all available coins")
        dict_data = MessageToDict(response,
                                  preserving_proto_field_name=True,
                                  always_print_fields_with_no_presence=True)
        return {"coins": dict_data["data"]}
    else:
        logger.warning("No coins available - consider error in communication")
        raise HTTPException(status_code=204)

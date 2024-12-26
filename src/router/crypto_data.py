from csv import excel

from google.protobuf.json_format import MessageToDict
from fastapi import APIRouter, HTTPException, Request, Query
from grpc import RpcError
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


@crypto_router.get("/details")
def get_crypto_details(
        coin_id: str = Query(description="Name of crypto for which data will be received"),
        request: Request,
        currency: str = Query("usd", description="Currency code in which data will be received")):
    auth_header = request.headers.get("Authorization")
    jwt_payload = verify_user(auth_header)

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

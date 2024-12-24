from google.protobuf.json_format import MessageToDict
from fastapi import APIRouter, HTTPException, Request
from grpc import RpcError
from pydantic import BaseModel
from enum import Enum

from src.connections import currency_stub
from currency import currency_pb2, currency_type_pb2

from src.utils.logger import logger

currency = APIRouter(tags=["Currency"])

currency_types_mapper = {
    currency_type_pb2.CURRENCY_TYPE_NOT_SUPPORTED: "NOT_SUPPORTED",
    currency_type_pb2.CURRENCY_TYPE_FIAT: "FIAT",
    currency_type_pb2.CURRENCY_TYPE_CRYPTO: "CRYPTO"
}


class CurrencyType(str, Enum):
    FIAT = "FIAT"
    CRYPTO = "CRYPTO"

    def to_grpc(self):
        mapping = {
            self.FIAT: currency_type_pb2.CURRENCY_TYPE_FIAT,
            self.CRYPTO: currency_type_pb2.CURRENCY_TYPE_CRYPTO
        }
        return mapping[self]


@currency.get("/", responses={
    500: {
        "description": "Problems occurred inside the server",
        "content": {
            "application/json": {
                "example": {"detail": "internal_server_error"}
            }
        }
    },
    400: {
        "description": "Creation of wallet failed",
        "content": {
            "application/json": {
                "example": [{"detail": "operation_failed"},
                            {"detail": "negative_value"}
                            ]
            }
        }
    },
    200: {
        "description": "Returns type of currency (FIAT, CRYPTO, NOT_SUPPORTED)",
        "content": {
            "application/json": {
                "example": {
                    "currency_name": "PLN",
                    "currency_type": "FIAT"
                }
            }
        }
    }
}, description='Returns type of given currency')
def get_currency_type(currency_name: str):
    currency_message = currency_pb2.CurrencyDetails(currency_name=currency_name)
    try:
        currency_type_response: currency_pb2.CurrencyTypeMsg = currency_stub.GetCurrencyType(currency_message)
    except RpcError as e:
        logger.error("gRPC error details:", e)
        raise HTTPException(status_code=500,
                            detail="internal_server_error")

    logger.info(f"Currency name: {currency_name}, currency_type: {currency_types_mapper[currency_type_response.type]}")
    endpoint_response = {
        "currency_name": currency_name,
        "currency_type": currency_types_mapper[currency_type_response.type]
    }
    return endpoint_response


@currency.get("/currencies",
              responses={
                  500: {
                      "description": "Problems occurred inside the server",
                      "content": {
                          "application/json": {
                              "example": {"detail": "internal_server_error"}
                          }
                      }
                  },
                  200: {
                      "description": "List of currencies for given type",
                      "content": {
                          "application/json": {
                              "example": {
                                  "currencies": [
                                      {
                                          "currency_name": "ars"
                                      },
                                      {
                                          "currency_name": "gel"
                                      },
                                      {
                                          "currency_name": "bdt"
                                      },
                                      {
                                          "currency_name": "hkd"
                                      },
                                      {
                                          "currency_name": "huf"
                                      },
                                      {
                                          "currency_name": "idr"
                                      }
                                  ]
                              }
                          }
                      }
                  }
              },
              description='Returns currencies of given type')
def get_currencies_by_type(currency_type: CurrencyType):
    type_message = currency_pb2.CurrencyTypeMsg(type=currency_type.to_grpc())

    try:
        currencies_list: currency_pb2.CurrencyList = currency_stub.GetSupportedCurrencies(type_message)
    except RpcError as e:
        logger.error("gRPC error details:", e)
        raise HTTPException(status_code=500,
                            detail="internal_server_error")

    if len(currencies_list.currencies) == 0:
        logger.info("No currencies found")
        raise HTTPException(status_code=204)
    else:
        return MessageToDict(currencies_list,
                             preserving_proto_field_name=True,
                             always_print_fields_with_no_presence=True)

from google.protobuf.json_format import MessageToDict
from fastapi import APIRouter, HTTPException, Request, Query
from grpc import RpcError

from src.connections import prices_stub
from coins import coins_pb2

from src.utils.auth import verify_user
from src.router.wallets import get_wallets, get_wallet_by_id

from src.utils.logger import logger

statistics_router = APIRouter(tags=["Statistics"])


@statistics_router.get(
    "/portfolio-diversity",
    responses={
        500: {
            "description": "Problems occurred inside the server",
            "content": {
                "application/json": {"example": {"detail": "internal_server_error"}}
            },
        },
        400: {
            "description": "Operation failure",
            "content": {
                "application/json": {"example": {"detail": "operation_failed"}}
            },
        },
        401: {
            "description": "Authorization failure",
            "content": {
                "application/json": {
                    "example": [
                        {"detail": "no_authorization_header"},
                        {"detail": "invalid_auth_scheme"},
                        {"detail": "invalid_token"},
                        {"detail": "expired_token"},
                        {"detail": "unauthorized_user_for_method"},
                    ]
                }
            },
        },
        204: {"description": "User have no wallets"},
        200: {
            "description": "List containing share of cryptocurrencies in portfolio",
            "content": {
                "application/json": {
                    "example": {
                        "calculation_fiat_currency": "usd",
                        "crypto_wallets_statistics": [
                            {
                                "cryptocurrency": "BITCOIN",
                                "fiat_value": 4898400,
                                "current_price": 97968,
                                "share_in_portfolio": 96.43,
                            },
                            {
                                "cryptocurrency": "ETHEREUM",
                                "fiat_value": 181562,
                                "current_price": 3631.24,
                                "share_in_portfolio": 3.57,
                            },
                            {
                                "cryptocurrency": "RIPPLE",
                                "fiat_value": 23.799999999999997,
                                "current_price": 2.38,
                                "share_in_portfolio": 0,
                            },
                        ],
                    }
                }
            },
        },
    },
    description="Returns a list containing share of cryptocurrencies in portfolio",
)
async def get_portfolio_diversity(
    request: Request,
    user_id: str = Query(None, description="User ID"),
    currency: str = Query(
        "usd", description="Currency in which prices will be calculated", max_length=3
    ),
):
    list_of_wallets = get_wallets(request, user_id)
    currency = currency.lower()

    crypto_wallets = []
    for wallet in list_of_wallets["wallets"]:
        if wallet["is_crypto"]:
            crypto_wallets.append(wallet)

    try:
        coins_prices: coins_pb2.DataResponse = prices_stub.GetAllCoinsPrices(
            coins_pb2.AllCoinsPricesRequest()
        )
    except RpcError as e:
        logger.error("gRPC error details:", e)
        raise HTTPException(status_code=500, detail="internal_server_error")

    coins_prices = coins_prices.data

    sum_value = 0
    response = {
        "calculation_fiat_currency": currency,
        "crypto_wallets_statistics": [],
    }
    for crypto_wallet in crypto_wallets:
        current_price = float(coins_prices[crypto_wallet["currency"].lower()][currency])
        crypto_value = float(crypto_wallet["value"]) * current_price
        sum_value += crypto_value
        response["crypto_wallets_statistics"].append(
            {
                "cryptocurrency": crypto_wallet["currency"],
                "fiat_value": crypto_value,
                "current_price": current_price,
            }
        )
        
    if sum_value == 0:
        sum_value = 1
      
    for wallet in response["crypto_wallets_statistics"]:
        wallet["share_in_portfolio"] = round(wallet["fiat_value"] / sum_value * 100, 2)

    return response


@statistics_router.get(
    "/crypto-estimation",
    responses={
        500: {
            "description": "Problems occurred inside the server",
            "content": {
                "application/json": {"example": {"detail": "internal_server_error"}}
            },
        },
        400: {
            "description": "Operation failure",
            "content": {
                "application/json": {"example": {"detail": "operation_failed"}}
            },
        },
        401: {
            "description": "Authorization failure",
            "content": {
                "application/json": {
                    "example": [
                        {"detail": "no_authorization_header"},
                        {"detail": "invalid_auth_scheme"},
                        {"detail": "invalid_token"},
                        {"detail": "expired_token"},
                        {"detail": "unauthorized_user_for_method"},
                    ]
                }
            },
        },
        204: {"description": "User have no wallets"},
        200: {
            "description": "List containing cryptocurrencies value estimation in portfolio",
            "content": {
                "application/json": {
                    "example": {
                        "calculation_fiat_currency": "usd",
                        "estimations": [
                            {
                                "cryptocurrency": "BITCOIN",
                                "amount": "50.0",
                                "estimated_fiat_value": 4892200,
                            },
                            {
                                "cryptocurrency": "ETHEREUM",
                                "amount": "50.0",
                                "estimated_fiat_value": 181150,
                            },
                        ],
                    }
                }
            },
        },
    },
    description="Returns a list containing estimated value of cryptocurrencies in portfolio",
)
async def get_crypto_estimation(
    request: Request,
    user_id: str = Query(None, description="User ID"),
    currency: str = Query(
        "usd", description="Currency in which prices will be calculated"
    ),
    wallet_id: str = Query(
        None, description="Crypto currency wallet for which prices will be calculated"
    ),
):
    auth_header = request.headers.get("Authorization")
    jwt_payload = verify_user(auth_header)

    try:
        coins_prices: coins_pb2.DataResponse = prices_stub.GetAllCoinsPrices(
            coins_pb2.AllCoinsPricesRequest()
        )
    except RpcError as e:
        logger.error("gRPC error details:", e)
        raise HTTPException(status_code=500, detail="internal_server_error")
    coins_prices = coins_prices.data

    response = {"calculation_fiat_currency": currency, "estimations": []}

    if wallet_id is None:
        list_of_wallets = get_wallets(
            request, user_id if user_id is not None else jwt_payload["id"]
        )
        list_of_wallets = list_of_wallets

        for wallet in list_of_wallets["wallets"]:
            response["estimations"].append(
                {
                    "cryptocurrency": wallet["currency"],
                    "amount": wallet["value"],
                    "estimated_fiat_value": float(wallet["value"])
                    * float(coins_prices[wallet["currency"].lower()][currency]),
                }
            )

        return response
    else:
        wallet_details = get_wallet_by_id(wallet_id, request)
        response["estimations"].append(
            {
                "cryptocurrency": wallet_details["currency"],
                "amount": wallet_details["value"],
                "estimated_fiat_value": float(wallet_details["value"])
                * float(coins_prices[wallet_details["currency"].lower()][currency]),
            }
        )
        return response

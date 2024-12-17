from google.protobuf.json_format import MessageToDict
from fastapi import APIRouter, HTTPException, Request
from grpc import RpcError
from pydantic import BaseModel
import stripe

from secret import secret_pb2
from src.connections import secret_stub, payment_stub
from payment import payment_state_pb2, payment_pb2
from src.utils.auth import verify_user

from src.utils.logger import logger
from src.utils.payment_scheduler import get_session_status

SUPPORTED_CURRENCIES = ['USD', 'EUR', 'GBP', 'PLN']

success_urls = [
    "http://localhost:4200/payment/success",
    "http://localhost/payment/success",
    "http://thdc/payment/success",
    "http://thdc.tail8ec47f.ts.net/payment/success"
]

failure_urls = [
    "http://localhost:4200/payment/fail",
    "http://localhost/payment/fail",
    "http://thdc/payment/fail",
    "http://thdc.tail8ec47f.ts.net/payment/fail"
]

try:
    message = secret_pb2.SecretName(name="STRIPE_SECRET_KEY")
    response_secret: secret_pb2.SecretValue = secret_stub.GetSecret(message)
    STRIPE_SECRET = response_secret.value
    stripe.api_key = STRIPE_SECRET
except RpcError as err:
    logger.error(f"Error retrieving secret: {err}")


class MakePayment(BaseModel):
    currency: str
    nominal: str


payments = APIRouter(tags=["Payments"])


@payments.post("/", responses={
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
                "example": [{"detail": "not_supported_currency"},
                            {"detail": "invalid_nominal"}]
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
        "description": "Details of created wallet",
        "content": {
            "application/json": {
                "example": [
                    {"session_url": "string i.e. https://stripe.com/payment/dsgq35211gs2",
                     "success_urls": success_urls,
                     "failure_urls": failure_urls,
                     "payment_details": {
                            "id": "dsgq35211gs2",
                            "currency": "PLN",
                            "value": "250.32",
                            "user_id": "2",
                            "state": "PAYMENT_STATE_PENDING"
                        }
                     }
                ]
            }
        }
    }
}, description='Returns details about created payment and redirections')
def payment(payment_details: MakePayment, request: Request):
    auth_header = request.headers.get("Authorization")
    jwt_payload = verify_user(auth_header)

    if payment_details.currency not in SUPPORTED_CURRENCIES:
        raise HTTPException(400, "not_supported_currency")

    if float(payment_details.nominal) <= 0:
        raise HTTPException(400, 'invalid_nominal')

    currency_symbol = payment_details.currency.lower()
    operation_nominal = float(payment_details.nominal) * 100
    user_id = jwt_payload['id']

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': currency_symbol,
                    'product_data': {
                        'name': f"Donate from {user_id}."
                    },
                    'unit_amount': int(operation_nominal)
                },
                'quantity': 1
            }],
            mode='payment',
            success_url=success_urls[0],
            cancel_url=failure_urls[0],
            metadata={
                "success_urls": ','.join(success_urls),
                "failure_urls": ','.join(failure_urls),
            }
        )
    except stripe.error.StripeError as e:
        logger.error(f"Error creating payment session: {e}")
        raise HTTPException(400, 'invalid_payment_session')

    try:
        payment_message: payment_pb2.PaymentDetails = payment_pb2.PaymentDetails(**payment_details.dict(),
                                                                                 id=session.id,
                                                                                 user_id=jwt_payload['id'],
                                                                                 state=payment_state_pb2.PAYMENT_STATE_PENDING)
        payment_details_response: payment_pb2.PaymentDetails = payment_stub.CreatePayment(payment_message)

    except RpcError as e:
        logger.error("gRPC error details:", e)
        stripe.checkout.Session.expire(session.id)
        raise HTTPException(500, 'internal_server_error')

    response = [{
        "session_url": session.url,
        "payment_details": MessageToDict(payment_details_response, preserving_proto_field_name=True),
        "success_urls": success_urls,
        "failure_urls": failure_urls
    }]

    return response


@payments.get("/", responses={
    500: {
        "description": "Problems occurred inside the server",
        "content": {
            "application/json": {
                "example": {"detail": "internal_server_error"}
            }
        }
    },
    400: {
        "description": "Getting payment failed",
        "content": {
            "application/json": {
                "example": {"detail": "operation_failed"}
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
    204: {
        "description": "No payment with specified id"
    },
    200: {
        "description": "Details of specified payment",
        "content": {
            "application/json": {
                "example": {
                    "id": "dsgq35211gs2",
                    "currency": "PLN",
                    "value": "250.32",
                    "user_id": "2",
                    "state": "PAYMENT_STATE_PENDING"
                }
            }
        }
    }
}, description="Returns payment details of specified id")
def get_payment_details(payment_id, request: Request):
    auth_header = request.headers.get("Authorization")
    jwt_payload = verify_user(auth_header)

    payment_id_message = payment_pb2.PaymentID(id=payment_id)

    try:
        payment_details_response: payment_pb2.PaymentDetails = payment_stub.GetPayment(payment_id_message)
    except RpcError as e:
        logger.error("gRPC error details:", e)
        return HTTPException(500, 'internal_server_error')

    if payment_details_response.id == "":
        logger.info("No payment with given id")
        raise HTTPException(status_code=204)

    if str(jwt_payload.get("id")) != payment_details_response.user_id:
        logger.warning("Unauthorized user tried to fetch wallet details")
        raise HTTPException(status_code=401, detail="unauthorized_user_for_method")

    logger.info(f"Fetched payment with id: {payment_details_response.id}")
    return MessageToDict(payment_details_response, preserving_proto_field_name=True)


@payments.get("/payments", responses={
    500: {
        "description": "Problems occurred inside the server",
        "content": {
            "application/json": {
                "example": {"detail": "internal_server_error"}
            }
        }
    },
    400: {
        "description": "Getting list of payments failed",
        "content": {
            "application/json": {
                "example": {"detail": "operation_failed"}
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
                            {"detail": "unathorized_user_for_method"}
                            ]

            }
        }
    },
    204: {
        "description": "User have no payments"
    },
    200: {
        "description": "List of objects with payments details",
        "content": {
            "application/json": {
                "example": {
                    "payments": [
                        {
                            "id": "dsgq35211gs2",
                            "currency": "PLN",
                            "value": "250.32",
                            "user_id": "2",
                            "state": "PAYMENT_STATE_PENDING"
                        },
                        {
                            "id": "352tg1tt23",
                            "currency": "USD",
                            "value": "0.52",
                            "user_id": "2",
                            "state": "PAYMENT_STATE_ACCEPTED"
                        }
                    ]
                }
            }
        }
    }
}, description="Returns a list of all payments for user")
def get_users_payments(request: Request):
    auth_header = request.headers.get("Authorization")
    jwt_payload = verify_user(auth_header)

    user_data = payment_pb2.UserID(user_id=jwt_payload.get("id"))

    try:
        response: payment_pb2.PaymentList = payment_stub.GetPayments(user_data)
    except RpcError as e:
        logger.error("gRPC error details:", e)
        raise HTTPException(500, "internal_server_error")

    if len(response.payments) == 0:
        logger.info("No wallets found")
        raise HTTPException(status_code=204)
    else:
        logger.info("Found wallets")
        return MessageToDict(response, preserving_proto_field_name=True)


@payments.put("/payment/cancel", responses={
    500: {
        "description": "Problems occurred inside the server",
        "content": {
            "application/json": {
                "example": {"detail": "internal_server_error"}
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
    204: {
        "description": "No payment with specified id"
    },
    200: {
        "description": "Details of cancelled payment",
        "content": {
            "application/json": {
                "example": {
                    "id": "dsgq35211gs2",
                    "currency": "PLN",
                    "value": "250.32",
                    "user_id": "2",
                    "state": "PAYMENT_STATE_CANCELLED"
                }
            }
        }
    }
}, description="Cancels payment with specified id")
def cancel_payment(payment_id, request: Request):
    payment_status, session_status = get_session_status(payment_id)

    if session_status=="open":
        try:
            stripe.checkout.Session.expire(payment_id)
            update_message: payment_pb2.PaymentDetails = payment_pb2.PaymentDetails(id=payment_id,
                                                                                    state=payment_state_pb2.PAYMENT_STATE_CANCELLED)
            response: payment_pb2.PaymentDetails = payment_stub.UpdatePayment(update_message)
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error occured: {e}")
            raise HTTPException(500, 'internal_server_error')
        except RpcError as e:
            logger.error("gRPC error details:", e)
            raise HTTPException(500, 'internal_server_error')

        logger.info(f"Payment with id {payment_id} cancelled")
        return MessageToDict(response, preserving_proto_field_name=True)
    else:
        logger.info(f"Payment with id {payment_id} was already cancelled or session expired")
        payment_details = get_payment_details(payment_id, request)
        return payment_details
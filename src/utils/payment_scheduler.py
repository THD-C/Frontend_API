from apscheduler.schedulers.background import BackgroundScheduler
import stripe
from google.protobuf.json_format import MessageToDict
from grpc import RpcError

from payment import payment_pb2, payment_state_pb2
from src.connections import payment_stub

from src.utils.logger import logger


def setup_payments_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_for_payments, 'interval', seconds=60)
    scheduler.start()


def check_for_payments():
    logger.info(f"Scheduler running...")
    message = payment_pb2.UnpaidSessions(unpaid=True)
    pending_payments: payment_pb2.PaymentList = payment_stub.GetUnpaidPayments(message)

    for payment in pending_payments.payments:

        payment_status, session_status = get_session_status(payment.id)
        if (session_status is None and session_status == "open") or payment_status is None:
            continue

        try:
            if payment_status == 'paid' and session_status == 'complete':
                update_message = payment_pb2.PaymentDetails(id=payment.id,
                                                            state=payment_state_pb2.PAYMENT_STATE_ACCEPTED)

            elif payment_status == 'payment_failed' or session_status == "expired":
                update_message = payment_pb2.PaymentDetails(id=payment.id,
                                                            state=payment_state_pb2.PAYMENT_STATE_CANCELLED)
            else:
                continue
            response: payment_pb2.PaymentDetails = payment_stub.UpdatePayment(update_message)
            logger.info(f"Payment {payment.id} has been updated. {MessageToDict(response)}")
        except RpcError as e:
            logger.error(f"Problem with updating payment status: {payment.id}. Error: {e}")
    logger.info("Scheduler finished")


def get_session_status(session_id):
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        session_payment_status = session.payment_status
        session_status = session.status
        return session_payment_status, session_status
    except stripe.error.StripeError as e:
        logger.error(f'Problems with stripe in Scheduler: {e}')
        return None, None

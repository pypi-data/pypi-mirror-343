# Version: 1.0.1
# Author: Reinan Br
# Date: 2021-07-07
# This is the VerifyPixPayment class that is responsible for verifying the status of a PIX payment.

from datetime import datetime
from typing import Optional
import pytz
import mercadopago
from mercadopagovp.load_sdk import LoadSDK
from mercadopagovp.pix_payment import PixPayment


class VerifyPixPayment:
    """Class responsible for verifying the status of a PIX payment."""

    def __init__(self, key_sdk: Optional[str] = None):
        """
        Initializes the VerifyPixPayment class.

        Args:
            key_sdk (Optional[str]): SDK key for MercadoPago. Defaults to None.
        """
        self.sdk = LoadSDK(key_sdk=key_sdk).get_sdk()

    def verify_payment(self, payment_id: str) -> PixPayment:
        """
        Verifies the status of a PIX payment.

        Args:
            payment_id (str): ID of the payment to be verified.

        Returns:
            PixPayment: Object representing the verified payment.
        """
        request = mercadopago.config.RequestOptions()
        payment_response = self.sdk.payment().get(payment_id, request)['response']

        # Parse dates
        date_expiration = datetime.fromisoformat(payment_response['date_of_expiration'])
        date_created = datetime.fromisoformat(payment_response['date_created'])
        date_now = datetime.now(pytz.timezone("America/Sao_Paulo"))

        # Calculate time to expiration
        delta_time = int((date_expiration - date_now).total_seconds())

        # Create and return PixPayment object
        return PixPayment(
            id=payment_response['id'],
            id_execution=payment_response["charges_execution_info"]['internal_execution']['execution_id'],
            amount=payment_response['transaction_amount'],
            qr_code=payment_response['point_of_interaction']['transaction_data']['qr_code'],
            qr_code_base64=payment_response['point_of_interaction']['transaction_data']['qr_code_base64'],
            description=payment_response['description'],
            currency_id=payment_response['currency_id'],
            payment_method=payment_response['payment_method_id'],
            date_last_updated=payment_response['date_last_updated'],
            date_init=payment_response['date_created'],
            date_end=payment_response['date_of_expiration'],
            status_code=payment_response['status'],
            status_payment=payment_response['status_detail'],
            ticket_url=payment_response['point_of_interaction']['transaction_data']['ticket_url'],
            link_notification=payment_response["notification_url"],
            time_to_end=delta_time,
            sdk=self.sdk
        )
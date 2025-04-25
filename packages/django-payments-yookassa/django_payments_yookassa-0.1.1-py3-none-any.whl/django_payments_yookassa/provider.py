import json
import uuid
from decimal import Decimal
from typing import Any

from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse, JsonResponse
from payments import get_payment_model, PaymentStatus, RedirectNeeded, PaymentError
from payments.core import BasicProvider
import yookassa
from yookassa.domain.common import SecurityHelper
from yookassa.domain.notification import WebhookNotificationFactory, WebhookNotificationEventType
from yookassa.domain.response import PaymentResponse

"""
Payment attrs
    - full_response
    - payment_method
    - refund
    - capture
    - cancel
"""

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class YooKassaProvider(BasicProvider):

    def __init__(self, *args, **kwargs):
        self.account_id = kwargs.pop('account_id', None)
        self.secret_key = kwargs.pop('secret_key', None)
        self.secure_endpoint = kwargs.pop('secure_endpoint', True)
        self.use_token = kwargs.pop('use_token', False)
        self.save_payment_method = kwargs.pop('save_payment_method', False)

        if not self.account_id or not self.secret_key:
            raise ImproperlyConfigured('YooKassa provider requires account_id and client_id')

        # Configure YooKassa SDK
        yookassa.Configuration.configure(self.account_id, self.secret_key)
        super(YooKassaProvider, self).__init__(*args, **kwargs)

    @staticmethod
    def update_payment(payment_id: int, **kwargs: Any) -> None:
        """Helper method to update the payment model safely."""
        # Get payment model inside the method
        Payment = get_payment_model()
        Payment.objects.filter(id=payment_id).update(**kwargs)

    def create_payment(self, payment, extra_data=None) -> PaymentResponse:
        if not payment.transaction_id:
            idempotence_key = str(uuid.uuid4())
            params = {
                'amount': {
                    'value': str(payment.total),
                    'currency': payment.currency
                },
                'confirmation': {
                    'type': 'redirect',
                    'return_url': payment.get_success_url()
                },
                'capture': self.capture,
                'save_payment_method': self.save_payment_method,

                'description': payment.description,
                'metadata': {
                    'payment_id': payment.token if self.use_token else payment.pk,
                }
            }
            if extra_data:
                params['metadata'].update(extra_data)

            response = yookassa.Payment.create(params, idempotence_key)

            # Update payment
            self.update_payment(payment.id, transaction_id=response.id)
            payment.change_status(PaymentStatus.INPUT)
            return response

        else:
            raise PaymentError("This payment has already been processed.")


    def get_form(self, payment, data=None):
        response = self.create_payment(payment)
        raise RedirectNeeded(response.confirmation.confirmation_url)

    def return_event_payload(self, request):
        if self.secure_endpoint:
            # Check if the request is secure
            ip = get_client_ip(request)
            if not SecurityHelper().is_ip_trusted(ip):
                raise PaymentError(
                        code=400, message="IP is not trusted",
                    )
        return json.loads(request.body)

    def get_token_from_request(self, payment, request) -> str:
        """Return payment token from provider request."""
        event_json = self.return_event_payload(request)
        try:
            return event_json.get('object', {}).get('metadata', {}).get('payment_id')
        except Exception as e:
            raise PaymentError(
                code=400,
                message="payment_id is not present in metadata, check YooKassa Dashboard.",
            ) from e

    # def save_payment_method(self, payment, notification_object):
    #     """Save payment method to the payment object."""
    #     if not payment.attrs.payment_method:
    #         return None
    #     response_object = notification_object.object
    #     if response_object.payment_method.saved:
    #         payment.attrs.payment_method = json.dumps(response_object.payment_method)
    #         payment.save()
    #         return payment
    #     else:
    #         return None




    def process_webhook_notification(self, payment, request):
        event_json = self.return_event_payload(request)

        try:
            notification_object = WebhookNotificationFactory().create(event_json)
            response_object = notification_object.object

            if notification_object.event == WebhookNotificationEventType.PAYMENT_SUCCEEDED:
                payment.change_status(PaymentStatus.CONFIRMED)

            elif notification_object.event == WebhookNotificationEventType.PAYMENT_WAITING_FOR_CAPTURE:
                payment.change_status(PaymentStatus.PREAUTH)

            elif notification_object.event == WebhookNotificationEventType.PAYMENT_CANCELED:
                payment.change_status(PaymentStatus.REJECTED)

            elif notification_object.event == WebhookNotificationEventType.REFUND_SUCCEEDED:
                payment.change_status(PaymentStatus.REFUNDED)

            else:
                return HttpResponse(status=400)

            payment.attrs.payment = response_object
            payment.save()

        except Exception:
            return HttpResponse(status=400)

        return JsonResponse({"status": "OK"})

    def process_widget_callback(self, request):
        pass

    def process_data(self, payment, request):
        if request.method == "POST":
            return self.process_webhook_notification(payment, request)
        return HttpResponse(status=405)


    def capture(self, payment, amount=None):
        amount = int((amount or payment.total) * 100)
        yookassa_payment = yookassa.Payment.find_one(payment.transaction_id)
        idempotence_key = str(uuid.uuid4())
        try:
            capture = yookassa.Payment.capture(yookassa_payment.id, amount, idempotence_key)
            payment.attrs.capture = json.dumps(capture)
        except Exception as e:
            payment.change_status(PaymentStatus.ERROR)

        return Decimal(amount) / 100

    def release(self, payment):
        yookassa_payment = yookassa.Payment.find_one(payment.transaction_id)
        idempotence_key = str(uuid.uuid4())
        cancel = yookassa.Payment.cancel(yookassa_payment.id, idempotence_key)
        payment.attrs.cancel = json.dumps(cancel)

    def refund(self, payment, amount=None):
        if payment.status == PaymentStatus.CONFIRMED:
            yookassa_payment = yookassa.Payment.find_one(payment.transaction_id)
            to_refund = amount or payment.total

            try:
                refund = yookassa.Refund.create({
                    "payment_id": yookassa_payment.id,
                    "description": "Refund issued",
                    "amount": {
                        "value": str(round(amount, 2)),  # Ensure value is a string and rounded to 2 decimals
                        "currency": payment.currency,
                    },
                })

            except Exception as e:
                raise PaymentError(e) from e

            else:
                payment.attrs.refund = json.dumps(refund)
                payment.save()
                payment.change_status(PaymentStatus.REFUNDED)
                return to_refund
        raise PaymentError("Only Confirmed payments can be refunded")

    # def status(self, payment):
    #     """
    #     Check the status of the payment.
    #     """
    #     try:
    #         yookassa_payment = yookassa.Payment.find_one(payment.transaction_id)
    #         payment.attrs.payment = json.dumps(yookassa_payment)
    #         payment.save()
    #         return yookassa_payment.status
    #     except Exception as e:
    #         raise PaymentError(e) from e

























import json
import pytest
from decimal import Decimal
from unittest.mock import patch, MagicMock

from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse, JsonResponse
from payments import PaymentStatus, RedirectNeeded, PaymentError
from payments import get_payment_model

from django_payments_yookassa.provider import YooKassaProvider
from tests.test_app.models import BaseTestPayment



@pytest.fixture
def provider():
    return YooKassaProvider(account_id="test_account_id", secret_key="test_secret_key")


@pytest.fixture
def payment():
    # Create a mock payment instead of a real database object
    payment = MagicMock()
    payment.id = 1
    payment.variant = "yookassa"
    payment.description = "Test payment"
    payment.total = Decimal("100.00")
    payment.currency = "RUB"
    payment.status = PaymentStatus.WAITING
    payment.transaction_id = None
    payment.get_success_url.return_value = "http://example.com/success"
    payment.attrs = MagicMock()
    return payment


def test_yookassa_provider_initialization():
    provider = YooKassaProvider(account_id="test_account_id", secret_key="test_secret_key")
    assert provider is not None
    assert provider.account_id == "test_account_id"
    assert provider.secret_key == "test_secret_key"
    assert provider.secure_endpoint is True
    assert provider.use_token is False


def test_yookassa_provider_initialization_with_options():
    provider = YooKassaProvider(
        account_id="test_account_id", 
        secret_key="test_secret_key",
        secure_endpoint=False,
        use_token=True
    )
    assert provider.secure_endpoint is False
    assert provider.use_token is True


def test_yookassa_provider_missing_credentials():
    with pytest.raises(ImproperlyConfigured):
        YooKassaProvider()

    with pytest.raises(ImproperlyConfigured):
        YooKassaProvider(account_id="test_account_id")

    with pytest.raises(ImproperlyConfigured):
        YooKassaProvider(secret_key="test_secret_key")


@patch('django_payments_yookassa.provider.get_payment_model')
def test_update_payment(mock_get_payment_model, provider):
    # Create a mock for the Payment model
    mock_payment_model = MagicMock()
    mock_filter = MagicMock()
    mock_payment_model.objects.filter.return_value = mock_filter
    mock_get_payment_model.return_value = mock_payment_model
    
    # Call the method
    provider.update_payment(payment_id=1, status="paid")
    
    # Verify the calls
    mock_payment_model.objects.filter.assert_called_once_with(id=1)
    mock_filter.update.assert_called_once_with(status="paid")


@patch('yookassa.Payment.create')
def test_create_payment(mock_create, provider, payment):
    # Create a mock response
    mock_response = MagicMock()
    mock_response.id = "test_transaction_id"
    mock_response.confirmation.confirmation_url = "https://test-confirmation-url.com"
    mock_create.return_value = mock_response
    
    # Call the method
    with patch.object(provider, 'update_payment') as mock_update:
        response = provider.create_payment(payment)
    
    # Verify the response
    assert response == mock_response
    
    # Verify the update call
    mock_update.assert_called_once_with(payment.id, transaction_id="test_transaction_id")
    assert payment.change_status.called_with(PaymentStatus.WAITING)


@patch('yookassa.Payment.create')
def test_create_payment_with_extra_data(mock_create, provider, payment):
    # Create a mock response
    mock_response = MagicMock()
    mock_response.id = "test_transaction_id"
    mock_create.return_value = mock_response
    
    # Call the method with extra data
    extra_data = {"customer_id": "12345"}
    with patch.object(provider, 'update_payment') as mock_update:
        response = provider.create_payment(payment, extra_data=extra_data)
    
    # Verify the extra data was included in the call
    called_args = mock_create.call_args[0][0]
    assert called_args['metadata']['customer_id'] == "12345"


@patch('yookassa.Payment.create')
def test_create_payment_with_existing_transaction_id(mock_create, provider, payment):
    # Set an existing transaction ID
    payment.transaction_id = "existing_transaction_id"
    
    # Call the method and expect an error
    with pytest.raises(PaymentError) as excinfo:
        provider.create_payment(payment)
    
    assert "This payment has already been processed." in str(excinfo.value)
    # Verify create was not called
    mock_create.assert_not_called()


@patch('django_payments_yookassa.provider.YooKassaProvider.create_payment')
def test_get_form(mock_create_payment, provider, payment):
    # Create a mock response
    mock_response = MagicMock()
    mock_response.confirmation.confirmation_url = "https://test-confirmation-url.com"
    mock_create_payment.return_value = mock_response
    
    # Call the method and expect RedirectNeeded exception
    with pytest.raises(RedirectNeeded) as excinfo:
        provider.get_form(payment)
    
    # Verify the redirect URL
    assert str(excinfo.value) == "https://test-confirmation-url.com"


def test_return_event_payload_not_secure(provider):
    # Configure provider not to check security
    provider.secure_endpoint = False
    
    # Create a mock request
    request = MagicMock()
    request.body = json.dumps({"test": "data"})
    
    # Call the method
    result = provider.return_event_payload(request)
    
    # Verify the result
    assert result == {"test": "data"}


@patch('django_payments_yookassa.provider.get_client_ip')
@patch('yookassa.domain.common.SecurityHelper.is_ip_trusted')
def test_return_event_payload_secure_trusted_ip(mock_is_trusted, mock_get_ip, provider):
    # Configure mocks
    mock_get_ip.return_value = "127.0.0.1"
    mock_is_trusted.return_value = True
    
    # Create a mock request
    request = MagicMock()
    request.body = json.dumps({"test": "data"})
    
    # Call the method
    result = provider.return_event_payload(request)
    
    # Verify the result
    assert result == {"test": "data"}


@patch('django_payments_yookassa.provider.get_client_ip')
@patch('yookassa.domain.common.SecurityHelper.is_ip_trusted')
def test_return_event_payload_secure_untrusted_ip(mock_is_trusted, mock_get_ip, provider):
    # Configure mocks
    mock_get_ip.return_value = "1.2.3.4"
    mock_is_trusted.return_value = False
    
    # Create a mock request
    request = MagicMock()
    request.body = json.dumps({"test": "data"})
    
    # Call the method and expect an error
    with pytest.raises(PaymentError) as excinfo:
        provider.return_event_payload(request)
    
    # Verify the error
    assert "IP is not trusted" in str(excinfo.value)


@patch('django_payments_yookassa.provider.YooKassaProvider.return_event_payload')
def test_get_token_from_request(mock_return_payload, provider, payment):
    # Configure mock to return a payload with payment_id
    mock_return_payload.return_value = {
        "object": {
            "metadata": {
                "payment_id": "test_token"
            }
        }
    }
    
    # Create a mock request
    request = MagicMock()
    
    # Call the method
    result = provider.get_token_from_request(payment, request)
    
    # Verify the result
    assert result == "test_token"


@patch('django_payments_yookassa.provider.YooKassaProvider.return_event_payload')
def test_get_token_from_request_missing_payment_id(mock_return_payload, provider, payment):
    # Configure mock to return a payload without payment_id
    mock_return_payload.return_value = {
        "object": {
            "metadata": {}
        }
    }
    
    # Create a mock request
    request = MagicMock()
    
    # Call the method
    result = provider.get_token_from_request(payment, request)
    
    # The method should return None, not raise an error
    assert result is None


@patch('django_payments_yookassa.provider.WebhookNotificationFactory')
@patch('django_payments_yookassa.provider.YooKassaProvider.return_event_payload')
def test_process_webhook_notification_payment_succeeded(mock_return_payload, mock_factory, provider, payment):
    # Configure mocks
    mock_return_payload.return_value = {"test": "data"}
    
    mock_notification = MagicMock()
    mock_notification.event = "payment.succeeded"
    mock_notification.object = {"payment_data": "test"}
    
    mock_factory_instance = MagicMock()
    mock_factory_instance.create.return_value = mock_notification
    mock_factory.return_value = mock_factory_instance
    
    # Create a mock request
    request = MagicMock()
    
    # Call the method
    response = provider.process_webhook_notification(payment, request)
    
    # Verify the response and payment status
    assert isinstance(response, JsonResponse)
    assert response.status_code == 200
    payment.change_status.assert_called_with(PaymentStatus.CONFIRMED)


@patch('django_payments_yookassa.provider.WebhookNotificationFactory')
@patch('django_payments_yookassa.provider.YooKassaProvider.return_event_payload')
def test_process_webhook_notification_payment_waiting_for_capture(mock_return_payload, mock_factory, provider, payment):
    # Configure mocks
    mock_return_payload.return_value = {"test": "data"}
    
    mock_notification = MagicMock()
    mock_notification.event = "payment.waiting_for_capture"
    mock_notification.object = {"payment_data": "test"}
    
    mock_factory_instance = MagicMock()
    mock_factory_instance.create.return_value = mock_notification
    mock_factory.return_value = mock_factory_instance
    
    # Create a mock request
    request = MagicMock()
    
    # Call the method
    response = provider.process_webhook_notification(payment, request)
    
    # Verify the response and payment status
    assert isinstance(response, JsonResponse)
    assert response.status_code == 200
    payment.change_status.assert_called_with(PaymentStatus.PREAUTH)


@patch('django_payments_yookassa.provider.WebhookNotificationFactory')
@patch('django_payments_yookassa.provider.YooKassaProvider.return_event_payload')
def test_process_webhook_notification_payment_canceled(mock_return_payload, mock_factory, provider, payment):
    # Configure mocks
    mock_return_payload.return_value = {"test": "data"}
    
    mock_notification = MagicMock()
    mock_notification.event = "payment.canceled"
    mock_notification.object = {"payment_data": "test"}
    
    mock_factory_instance = MagicMock()
    mock_factory_instance.create.return_value = mock_notification
    mock_factory.return_value = mock_factory_instance
    
    # Create a mock request
    request = MagicMock()
    
    # Call the method
    response = provider.process_webhook_notification(payment, request)
    
    # Verify the response and payment status
    assert isinstance(response, JsonResponse)
    assert response.status_code == 200
    payment.change_status.assert_called_with(PaymentStatus.REJECTED)


@patch('django_payments_yookassa.provider.WebhookNotificationFactory')
@patch('django_payments_yookassa.provider.YooKassaProvider.return_event_payload')
def test_process_webhook_notification_refund_succeeded(mock_return_payload, mock_factory, provider, payment):
    # Configure mocks
    mock_return_payload.return_value = {"test": "data"}
    
    mock_notification = MagicMock()
    mock_notification.event = "refund.succeeded"
    mock_notification.object = {"payment_data": "test"}
    
    mock_factory_instance = MagicMock()
    mock_factory_instance.create.return_value = mock_notification
    mock_factory.return_value = mock_factory_instance
    
    # Create a mock request
    request = MagicMock()
    
    # Call the method
    response = provider.process_webhook_notification(payment, request)
    
    # Verify the response and payment status
    assert isinstance(response, JsonResponse)
    assert response.status_code == 200
    payment.change_status.assert_called_with(PaymentStatus.REFUNDED)


@patch('django_payments_yookassa.provider.WebhookNotificationFactory')
@patch('django_payments_yookassa.provider.YooKassaProvider.return_event_payload')
def test_process_webhook_notification_unknown_event(mock_return_payload, mock_factory, provider, payment):
    # Configure mocks
    mock_return_payload.return_value = {"test": "data"}
    
    mock_notification = MagicMock()
    mock_notification.event = "unknown.event"
    mock_notification.object = {"payment_data": "test"}
    
    mock_factory_instance = MagicMock()
    mock_factory_instance.create.return_value = mock_notification
    mock_factory.return_value = mock_factory_instance
    
    # Create a mock request
    request = MagicMock()
    
    # Call the method
    response = provider.process_webhook_notification(payment, request)
    
    # Verify the response is a 400 error
    assert isinstance(response, HttpResponse)
    assert response.status_code == 400


@patch('django_payments_yookassa.provider.YooKassaProvider.process_webhook_notification')
def test_process_data_post_request(mock_webhook, provider, payment):
    # Configure mock
    mock_webhook.return_value = JsonResponse({"status": "OK"})
    
    # Create a mock POST request
    request = MagicMock()
    request.method = "POST"
    
    # Call the method
    response = provider.process_data(payment, request)
    
    # Verify the webhook method was called
    mock_webhook.assert_called_once_with(payment, request)
    assert response.status_code == 200


def test_process_data_not_post_request(provider, payment):
    # Create a mock GET request
    request = MagicMock()
    request.method = "GET"
    
    # Call the method
    response = provider.process_data(payment, request)
    
    # Verify the response is a 405 error
    assert isinstance(response, HttpResponse)
    assert response.status_code == 405


@patch('yookassa.Payment.find_one')
@patch('yookassa.Payment.capture')
def test_capture(mock_capture, mock_find_one, provider, payment):
    # Set transaction ID
    payment.transaction_id = "test_transaction_id"
    
    # Configure mocks
    mock_payment = MagicMock()
    mock_payment.id = "test_transaction_id"
    mock_find_one.return_value = mock_payment
    
    mock_capture_response = {"status": "succeeded"}
    mock_capture.return_value = mock_capture_response
    
    # Call the method
    result = provider.capture(payment, Decimal("50.00"))
    
    # Verify the result
    assert result == Decimal("50.00")
    mock_capture.assert_called_once()
    

@patch('yookassa.Payment.find_one')
@patch('yookassa.Payment.cancel')
def test_release(mock_cancel, mock_find_one, provider, payment):
    # Set transaction ID
    payment.transaction_id = "test_transaction_id"
    
    # Configure mocks
    mock_payment = MagicMock()
    mock_payment.id = "test_transaction_id"
    mock_find_one.return_value = mock_payment
    
    mock_cancel_response = {"status": "canceled"}
    mock_cancel.return_value = mock_cancel_response
    
    # Call the method
    provider.release(payment)
    
    # Verify the cancel was called
    mock_cancel.assert_called_once()


@patch('yookassa.Payment.find_one')
@patch('yookassa.Refund.create')
def test_refund(mock_create, mock_find_one, provider, payment):
    # Set transaction ID and confirmed status
    payment.transaction_id = "test_transaction_id"
    payment.status = PaymentStatus.CONFIRMED
    
    # Configure mocks
    mock_payment = MagicMock()
    mock_payment.id = "test_transaction_id"
    mock_find_one.return_value = mock_payment
    
    mock_refund_response = {"status": "succeeded"}
    mock_create.return_value = mock_refund_response
    
    # Call the method with a specific amount
    amount = Decimal("25.00")
    result = provider.refund(payment, amount)
    
    # Verify the result
    assert result == amount
    payment.change_status.assert_called_with(PaymentStatus.REFUNDED)
    mock_create.assert_called_once()


def test_refund_not_confirmed(provider, payment):
    # Set transaction ID but not confirmed status
    payment.transaction_id = "test_transaction_id"
    payment.status = PaymentStatus.WAITING
    
    # Call the method and expect an error
    with pytest.raises(PaymentError) as excinfo:
        provider.refund(payment)
    
    # Verify the error
    assert "Only Confirmed payments can be refunded" in str(excinfo.value)

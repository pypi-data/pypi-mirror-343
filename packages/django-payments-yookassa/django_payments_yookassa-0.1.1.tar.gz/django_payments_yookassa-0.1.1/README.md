# Django Payments YooKassa

A YooKassa payment provider for [django-payments](https://github.com/django-payments/django-payments).

## Installation

```bash
pip install django-payments-yookassa
```

Or with uv:

```bash
uv pip install django-payments-yookassa
```

## Configuration

Add YooKassa to your payment variants in settings.py:

```python
PAYMENT_VARIANTS = {
    'yookassa': ('django_payments_yookassa.YooKassaProvider', {
        'shop_id': 'your-shop-id',
        'secret_key': 'your-secret-key',
        'capture': True,  # Whether to capture the payment automatically
        'use_webhook': True,  # Whether to use webhooks for payment status updates
        'test_mode': True,  # Set to False for production
    }),
}
```

## Features

- Automatic payment capture
- Webhook support for payment status updates
- Support for all payment methods available in YooKassa
- Compatible with django-payments 3.0+

## License

MIT License 
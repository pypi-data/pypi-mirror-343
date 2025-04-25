from payments.models import BasePayment


class BaseYooKassaPayment(BasePayment):  # type: ignore[misc]
    """Abstract base model for Django Payments, targeted at YooKassa transactions."""

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return f"{self.currency} {self.total} ({self.status})"

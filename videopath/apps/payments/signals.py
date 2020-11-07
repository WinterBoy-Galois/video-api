from django.dispatch import Signal

subscription_updated = Signal(providing_args=["user"])

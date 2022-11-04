from django.db import models
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.contrib.auth import get_user_model

from simple_history.models import HistoricalRecords

User = get_user_model()


class Stock(models.Model):
    name = models.CharField(max_length=20, null=True, blank=True, unique=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    ticker = models.CharField(max_length=10, unique=True)
    volume = models.PositiveIntegerField(default=0.00)
    price = models.DecimalField(max_digits=10, default=0, decimal_places=2)
    last_price = models.DecimalField(
        max_digits=10, default=0, decimal_places=2)
    open_price = models.DecimalField(
        max_digits=10, default=0, decimal_places=2)
    change = models.DecimalField(
        max_digits=10, default=0, decimal_places=2)
    max = models.DecimalField(max_digits=10, default=0, decimal_places=2)
    min = models.DecimalField(
        max_digits=10, default=0, decimal_places=2)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords(related_name='logs')

    @classmethod
    def get_stock(cls, id):
        stock = cls.objects.get(id=id)
        return stock

    @classmethod
    def get_history(cls, ticker, start_date=None, end_date=None):
        if start_date and end_date:
            return cls.history.filter(ticker=ticker, updated_at__date__gte=start_date, updated_at__date__lte=end_date)
        return cls.history.filter(ticker=ticker, updated_at__date=start_date)

    class Meta:
        ordering = ['updated_at']

    def __str__(self):
        return self.ticker

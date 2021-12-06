from django.db import models
from django.contrib.auth.models import AbstractUser
import string
import random

# Create your models here.


class PayPlan(models.Model):
    name = models.CharField(max_length=20)
    price = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)
    create_at = models.DateTimeField(auto_now_add=True)


class Users(AbstractUser):
    full_name = models.CharField(max_length=100, null=True)
    pay_plan = models.ForeignKey(PayPlan, on_delete=models.DO_NOTHING, null=True)


class BinanceTradeConditions(models.Model):
    class UrlCreatedVia(models.TextChoices):
        WEBSITE = "web"
        TELEGRAM = "telegram"

    api_key = models.CharField(max_length=100)
    secret_key = models.CharField(max_length=100)
    ticker = models.CharField(max_length=100)
    condition_type = models.CharField(max_length=100)
    condition_time = models.CharField(max_length=100)
    buy_money = models.CharField(max_length=100)
    condition_name = models.CharField(max_length=100)
    condition_sign = models.CharField(max_length=100)
    condition_value = models.CharField(max_length=100)
    created_by = models.ForeignKey(Users, on_delete=models.CASCADE)
    created_via = models.CharField(max_length=8, choices=UrlCreatedVia.choices, default=UrlCreatedVia.WEBSITE)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

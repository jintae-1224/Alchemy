from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from trade.models import Users
from django.forms.widgets import Widget
from trade.models import BinanceTradeConditions, Users
from django.utils.translation import gettext_lazy as _


class RegisterForm(UserCreationForm):
    full_name = forms.CharField(max_length=30, required=False, help_text="Optional.", label="이름")
    username = forms.CharField(max_length=30, required=False, help_text="Optional.", label="유저명")
    email = forms.EmailField(max_length=254, help_text="Required. Inform a valid email address.", label="이메일")

    class Meta:
        model = Users
        fields = (
            "username",
            "full_name",
            "email",
            "password1",
            "password2",
        )


class LoginForm(forms.Form):
    email = forms.CharField(
        max_length=100, required=True, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "이메일"})
    )
    password = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "패스워드"}),
    )
    remember_me = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": "custom-control-input", "id": "_loginRememberMe"}),
        required=False,
        disabled=False,
    )


class ConditionCreateForm(forms.ModelForm):
    class Meta:
        model = BinanceTradeConditions
        fields = [
            "api_key",
            "secret_key",
            "ticker",
            "condition_type",
            "condition_time",
            "condition_name",
            "condition_sign",
            "condition_value",
            "buy_money",
        ]
        labels = {
            "api_key": _("api_key"),
            "secret_key": _("secret.key"),
            "ticker": _("Ticker"),
            "condition_type": _("매수,매도"),
            "condition_time": _("기준봉"),
            "condition_name": _("조건"),
            "condition_sign": _("부등호"),
            "condition_value": _("조건값"),
            "buy_money": _("거래금액"),
        }
        TICKER_CHOICE = {
            ("BTC/USDT", "BTC/USDT"),
        }
        TYPE_CHOICE = {
            ("매수", "매수"),
            ("매도", "매도"),
        }
        TIME_CHOICE = {
            ("Interval.INTERVAL_1_MINUTES", "1M"),
            ("Interval.INTERVAL_5_MINUTES", "5M"),
            ("Interval.INTERVAL_10_MINUTES", "10M"),
            ("Interval.INTERVAL_30_MINUTES", "30M"),
        }
        NAME_CHOICE = {
            ("EMA5", "EMA5"),
            ("EMA10", "EMA10"),
            ("EMA20", "EMA20"),
            ("EMA50", "EMA50"),
            ("SMA5", "SMA5"),
            ("SMA10", "SMA10"),
            ("SMA20", "SMA20"),
            ("SMA50", "SMA50"),
            ("Stoch.K", "Stoch.K"),
            ("Stoch.D", "Stoch.D"),
            ("CCI20", "CCI20"),
            ("MACD.macd", "MACD.macd"),
            ("MACD.signal", "MACD.signal"),
            ("RSI", "RSI"),
            ("ADX+DI", "ADX+DI"),
            ("ADX-DI", "ADX-DI"),
            ("Pivot.M.Classic.S3", "Pivot.M.Classic.S3"),
            ("Pivot.M.Classic.S2", "Pivot.M.Classic.S2"),
            ("Pivot.M.Classic.S1", "Pivot.M.Classic.S1"),
            ("Rec.Stoch.RSI", "Rec.Stoch.RSI"),
            ("Stoch.RSI.K", "Stoch.RSI.K"),
        }
        SIGN_CHOICE = {
            ("=", "="),
            (">", ">"),
            (">=", ">="),
            ("<", "<"),
            ("<=", "<="),
            ("!=", "!="),
        }
        VALUE_CHOICE = {
            ("EMA5", "EMA5"),
            ("EMA10", "EMA10"),
            ("EMA20", "EMA20"),
            ("EMA50", "EMA50"),
            ("SMA5", "SMA5"),
            ("SMA10", "SMA10"),
            ("SMA20", "SMA20"),
            ("SMA50", "SMA50"),
            ("Stoch.K", "Stoch.K"),
            ("Stoch.D", "Stoch.D"),
            ("CCI20", "CCI20"),
            ("MACD.macd", "MACD.macd"),
            ("MACD.signal", "MACD.signal"),
            ("RSI", "RSI"),
            ("ADX+DI", "ADX+DI"),
            ("ADX-DI", "ADX-DI"),
            ("Pivot.M.Classic.S3", "Pivot.M.Classic.S3"),
            ("Pivot.M.Classic.S2", "Pivot.M.Classic.S2"),
            ("Pivot.M.Classic.S1", "Pivot.M.Classic.S1"),
            ("Rec.Stoch.RSI", "Rec.Stoch.RSI"),
            ("Stoch.RSI.K", "Stoch.RSI.K"),
        }
        widgets = {
            "api_key": forms.TextInput(attrs={"class": "form-control"}),
            "secret_key": forms.TextInput(attrs={"class": "form-control"}),
            "ticker": forms.Select(choices=TICKER_CHOICE, attrs={"class": "form-control"}),
            "condition_type": forms.Select(choices=TYPE_CHOICE, attrs={"class": "form-control"}),
            "condition_time": forms.Select(choices=TIME_CHOICE, attrs={"class": "form-control"}),
            "condition_name": forms.Select(choices=NAME_CHOICE, attrs={"class": "form-control"}),
            "condition_sign": forms.Select(choices=SIGN_CHOICE, attrs={"class": "form-control"}),
            "condition_value": forms.Select(choices=VALUE_CHOICE, attrs={"class": "form-control"}),
            "buy_money": forms.TextInput(attrs={"class": "form-control"}),
        }

    def save(self, request, commit=True):
        instance = super(ConditionCreateForm, self).save(commit=False)
        instance.created_by_id = request.user.id
        instance.api_key = instance.api_key.strip()
        instance.secret_key = instance.secret_key.strip()
        instance.ticker = instance.ticker.strip()
        instance.condition_type = instance.condition_type.strip()
        instance.condition_time = instance.condition_time.strip()
        instance.condition_name = instance.condition_name.strip()
        instance.condition_sign = instance.condition_sign.strip()
        instance.condition_value = instance.condition_value.strip()
        instance.buy_money = instance.buy_money
        if commit:
            instance.save()
            print("성공")
        else:
            print("실패")
        return instance

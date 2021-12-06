from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, PasswordChangeForm
from django.http.response import JsonResponse
from trade.models import Users, BinanceTradeConditions
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from trade.forms import RegisterForm, LoginForm, ConditionCreateForm
from django.contrib.auth import login, authenticate, logout
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import ccxt

# Create your views here.
def index(request):
    return render(request, "base.html")


def board_list(request):
    get_list = BinanceTradeConditions.objects.order_by("-created_at").all()
    return render(request, "board_list.html", {"list": get_list})


def condition_create(request):
    msg = None
    if request.method == "POST":
        form = ConditionCreateForm(request.POST)
        if form.is_valid():
            msg = " 생성 완료!"
            messages.add_message(request, messages.INFO, msg)
            form.save(request)
            return redirect("board_list")
        else:
            form = ConditionCreateForm()
    else:
        form = ConditionCreateForm()
    return render(request, "condition_create.html", {"form": form})


@login_required
def condition_change(request, action, condition_id):
    if request.method == "POST":
        condition_data = BinanceTradeConditions.objects.filter(id=condition_id)
        if condition_data.exists():
            if condition_data.first().created_by_id != request.user.id:
                msg = "자신이 소유하지 조건식 입니다."
            else:
                if action == "delete":
                    msg = "삭제 완료!"
                    condition_data.delete()
                    messages.add_message(request, messages.INFO, msg)
                elif action == "update":
                    msg = "수정 완료!"
                    form = ConditionCreateForm(request.POST)
                    form.update_form(request, condition_id)

                    messages.add_message(request, messages.INFO, msg)
        else:
            msg = "해당 URL 정보를 찾을 수 없습니다."

    elif request.method == "GET" and action == "update":
        condition_data = BinanceTradeConditions.objects.filter(pk=condition_id).first()
        form = ConditionCreateForm(instance=condition_data)
        return render(request, "condition_create.html", {"form": form, "is_update": True})

    return redirect("board_list")


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        msg = "올바르지 않은 데이터 입니다."
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            msg = "회원가입완료"
        return render(request, "register.html", {"form": form, "msg": msg})
    else:
        form = RegisterForm()
        return render(request, "register.html", {"form": form})


def login_view(request):
    is_ok = False
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            raw_password = form.cleaned_data.get("password")
            remember_me = form.cleaned_data.get("remember_me")
            msg = "올바른 유저ID와 패스워드를 입력하세요."
            try:
                user = Users.objects.get(email=email)
            except Users.DoesNotExist:
                pass
            else:
                if user.check_password(raw_password):
                    msg = None
                    login(request, user)
                    is_ok = True
                    request.session["remember_me"] = remember_me
                    return render(request, "board_list.html", {"form": form, "msg": msg, "is_ok": is_ok})

                    # if not remember_me:
                    #     request.session.set_expirey(0)
                    #     request.session.set_expiry(0)
    else:
        msg = None
        form = LoginForm()
    print("REMEMBER_ME: ", request.session.get("remember_me"))
    return render(request, "login.html", {"form": form, "msg": msg, "is_ok": is_ok})


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def run(request):
    print("됬다")
    return render(request, "trading.html", context={"text": "hi"})

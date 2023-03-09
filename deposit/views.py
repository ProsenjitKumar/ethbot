from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .models import DepositRequest
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from mainapp.models import Customer
from django.views.generic import ListView

from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.core import mail
from .models import PaymentMethod


class PaymentMethodView(ListView):
    model = PaymentMethod
    template_name = 'deposit/payment-method.html'


@login_required
def depsoit_view(request, slug, *args, **kwargs):
    object = get_object_or_404(PaymentMethod, slug=slug)
    intaial_data = {
        'payment_method': object.currency_name,
    }
    form = DepositForm(request.POST or None, initial=intaial_data)
    submit_amount = request.POST.get('amount_deposited')
    submit_amount_in_usd = request.POST.get('in_usd')
    if object.currency_name == 'Bkash' or object.currency_name == 'Nagad':
        form.fields['amount_deposited'].widget.attrs['placeholder'] = 'টাকার পরিমান'
        currency_value = 0.0094
        currency = "BDT"
    elif object.currency_name == 'UPI Payment':
        form.fields['amount_deposited'].widget.attrs['placeholder'] = 'पैसे की राशि'
        currency_value = 0.012
        currency = "INR"
    else:
        form.fields['amount_deposited'].widget.attrs['placeholder'] = 'Crypto Amount'
        currency_value = 0.0012
        currency = "ETH"
    context = {
        'form': form,
        'object': object,
        "currency_value": currency_value,

    }

    transaction_id = request.POST.get('transaction_id')
    email = request.user.email
    first_name = request.user.first_name
    last_name = request.user.last_name
    c = {
        "email": email,
        "user": request.user,
        "first_name": first_name,
        "last_name": last_name,
        "submit_amount": submit_amount,
        "transaction_id": transaction_id,
        "currency": currency,
        "submit_amount_in_usd": submit_amount_in_usd,
    }
    email_template = "deposit/deposit-email.txt"
    email_text = render_to_string(email_template, c)
    connection = mail.get_connection()
    if form.is_valid():
        confirm = form.save(commit=False)
        confirm.user = request.user
        confirm.save()
        messages.success(request, 'In a short while, the funds will reflect in your available balance!')
        amount_deposited = form.cleaned_data.get('amount_deposited')
        transaction_id = form.cleaned_data.get('transaction_id')
        email = EmailMessage(
            'Your deposit request has been successfully done!',
            email_text,
            from_email=settings.EMAIL_HOST_USER,
            to=[email],
            bcc=['prosenjit.pq@gmail.com', 'kateyalide@gmail.com', 'blptoken@gmail.com'],
            reply_to=['info@cryptoethbot.com'],
            headers={'Message-ID': 'foo'},
            connection=connection,
        )
        email.send()
        return redirect('/dashboard/')
    return render(request, 'dashboard/deposit/deposit.html', context)


@login_required
def bot_view(request):
    form = BotForm(request.POST or None)
    context = {
        'form': form,
    }
    customer = Customer.objects.get(account=request.user)
    balance = customer.balance
    myUpline = customer.parent_id
    print(myUpline)
    print(balance)
    bot_fee_1 = 0.017
    bot_fee_2 = 0.029
    refer_bonus = 0.0059
    plan = request.POST.get('selected_bot')
    if form.is_valid():
        if plan == '1' and balance >= float(bot_fee_1):
            customer.decrease_balance(bot_fee_1)
            try:
                refer_receiver = Customer.objects.get(id=myUpline)
                refer_receiver.increase_refer_bonus(float(refer_bonus))
            except:
                pass

            confirm = form.save(commit=False)
            confirm.user = request.user
            confirm.save()
            messages.success(request, 'Your bot has been activated for 6 months!')
            selected_bot = form.cleaned_data.get('selected_bot')
            return redirect('/dashboard/')
        elif plan == '2' and balance >= float(bot_fee_2):
            customer.decrease_balance(bot_fee_2)
            try:
                refer_receiver = Customer.objects.get(id=myUpline)
                refer_receiver.increase_refer_bonus(float(refer_bonus))
            except:
                pass
            confirm = form.save(commit=False)
            confirm.user = request.user
            confirm.save()
            messages.success(request, 'Your bot has been activated for 12 months!')
            selected_bot = form.cleaned_data.get('selected_bot')
            return redirect('/dashboard/')
        else:
            messages.error(request, "You have insufficient funds for activate the bot.\
            Please Deposit.")
            return redirect('/bot/')
    return render(request, 'dashboard/deposit/bot.html', context)


def close_trade(request):
    trade = Trading.objects.filter(user=request.user)
    if trade:
        trading = trade.latest('created_at')
        active = False
        trading.update_active(active)
    return HttpResponseRedirect('/dashboard/')

@login_required
def trading_account_view(request):
    form = TradingAccountForm(request.POST or None)
    context = {
        'form': form,
    }

    if form.is_valid():
        confirm = form.save(commit=False)
        confirm.user = request.user
        confirm.save()
        messages.success(request, 'Your trading account info has been submitted successfully!')
        confirm = form.save(commit=False)
        confirm.user = request.user
        confirm.save()
        return redirect('/trading-account/')

    return render(request, 'trading/trading-account.html', context)


def page(request):
    form = DepositForm(request.POST or None)
    import http.client
    conn = http.client.HTTPSConnection("anyapi.io")
    conn.request("GET", "https://anyapi.io/api/v1/exchange/rates?apiKey=n8hf1elibb8ilq02h5rvg8msj2ic71jqnm052ft4q288hdkp7fqcf8")
    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))
    context = {
        "form": form,
        "usd": 200,
    }
    if form.is_valid():
        form.save()
        redirect('/')
    return render(request, 'page.html', context)


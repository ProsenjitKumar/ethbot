from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from deposit.models import DepositRequest
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
# Email
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.core import mail
# trading
from deposit.forms import *
from deposit.models import *
# schedulers
from history.models import *
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.combining import OrTrigger
from apscheduler.triggers.cron import CronTrigger
# -------------
from withdraw.models import WithdrawalRequest
from deposit.models import DepositRequest, Trading
# send one time otp password due to login
from .utils import send_otp
import pyotp
# password reset
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
# email verification
# from verify_email.email_handler import send_verification_email
from django.contrib.sites.shortcuts import get_current_site
# from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage

# Create your views here.


# -------------------------------
#                                |
#           Index View
#                                |
# -------------------------------
def index(request, *args, **kwargs):
    code = str(kwargs.get('ref_code'))
    recent_withdraw = WithdrawalRequest.objects.order_by('-created_at')
    opened_trade = Trading.objects.order_by('-created_at')
    context = {
        'withdraws': recent_withdraw,
        'opened_trade': opened_trade,
    }

    try:
        profile = Customer.objects.get(code=code)
        request.session['ref_profile'] = profile.id
        print('id = ', profile.id)
        print("profile", profile)
    except:
        pass
    return render(request, 'index/index_2.html', context)


# -------------------------------
#                                |
#           Authentication View
#                                |
# -------------------------------
@csrf_protect
def signup_view(request, *args, **kwargs):
    code = str(kwargs.get('ref_code'))

    try:
        profile = Customer.objects.get(code=code)
        request.session['ref_profile'] = profile.id
        print('id = ', profile.id)
        print("profile", profile)
    except:
        pass
    profile_id = request.session.get('ref_profile')
    print('profile_id = ', profile_id)
    form = SignupForm(request.POST or None)
    email_submitted = request.POST.get('email')
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    passw = request.POST.get('password1')
    duplicate_email = User.objects.filter(email=email_submitted).count()
    print("duplicate email", duplicate_email)
    if form.is_valid():
        if duplicate_email == 0:
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            if profile_id is not None:
                recommended_by_profile = Customer.objects.get(id=profile_id)
                print("recommended_by_profile = ", recommended_by_profile)
                instance = form.save()
                print("instance saved = ", instance)
                registered_user = User.objects.get(id=instance.id)
                print("registered_user = ", registered_user)
                registered_profile = Customer.objects.get(account=registered_user)
                print("registered_profile = ", registered_profile)
                print("registered_profile.account = ", registered_profile.account)
                print("recommended_by_profile.parent_id = ", recommended_by_profile.parent_id)
                print("recommended_by_profile.parent = ", recommended_by_profile.parent)
                print("recommended_by_profile.account = ", recommended_by_profile.account)
                print(" -------- ** -----------")
                # registered_profile.parent_id = recommended_by_profile.account.pk
                registered_profile.parent_id = profile_id

                print("registered_profile.parent_id = ", registered_profile.parent_id)
                registered_profile.save()
                print("registered_profile it's saved = 100%", registered_profile)

            else:
                print("Referral not working")
                form.save()
            current_site = get_current_site(request)
            mail_subject = 'Your Ethereum Trading Bot Account Confirmation'
            message = render_to_string('index/email-verify.html', {
                'user': user,
                'first_name': first_name,
                'last_name': last_name,
                'passw': passw,
                # 'domain': '127.0.0.1:8000',
                'domain': get_current_site(request),
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            username = form.cleaned_data.get('username')
            # email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            # user = authenticate(username=username, password=password)
            # login(request, user)
            return render(request, 'index/email-sent.html', {"email_submitted": email_submitted})
        else:
            messages.error(request, 'Email is already exists!')
    context = {
        'form': form
    }
    return render(request, 'index/register.html', context)


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        email_submitted = user.email
        user.is_active = True
        user.save()
        messages.success(request, 'Thank you for your email confirmation. Now you can login your account')
        send_mail('Thanks for joining with Crypto Ethereum Trading Bot',
                  'The Automated Trading Solution for Ethereum Enthusiasts.\n'
                  'CryptoEthBot is an Ethereum-based trading bot that allows users to automate their '
                  'Ethereum trading strategies and take advantage of opportunities in the fast-moving Ethereum market. '
                  'The bot uses advanced algorithms and statistical analysis to monitor market conditions and execute '
                  'trades based on pre-defined rules and strategies, '
                  'making it easier for users to trade Ethereum without having to monitor market conditions around '
                  'the clock.'
                  '\n'
                  '\n'
                  'Web: www.cryptoethbot.com\n'
                  'Mail: hello@cryptoethbot.com\n'
                  'Ethereum Trading Bot Team',
                  from_email=settings.EMAIL_HOST_USER,
                  recipient_list=[email_submitted]
                  )
        return redirect('signin')
    else:
        return HttpResponse('Activation link is invalid!')
# def activate(request, uidb64, token):
#     User = get_user_model()
#     try:
#         uid = force_text(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except(TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None
#     if user is not None and account_activation_token.check_token(user, token):
#         user.is_active = True
#         user.save()
#         return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
#     else:
#         return HttpResponse('Activation link is invalid!')


# @csrf_protect
def login_view(request):
    form = LoginForm(request.POST or None)
    context = {"form": form}
    error_message = None

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # send one time password
            # --
            request.session['username'] = username
            # return redirect(otp)
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect("/dashboard/")
            else:
                messages.error(request, 'Your account is not active yet.')
                return render(request, 'index/login.html', context)
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            messages.error(request, 'Username or Password is not correct.')
            return render(request, 'index/login.html', context)
    else:
        return render(request, 'index/login.html', context)


# password reset
def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "index/reset/password_reset_email.txt"
                    c = {
                    "email":user.email,
                    'domain':'127.0.0.1:8000',
                    'site_name': 'Website',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'ethereum-bot@cryptoethbot.com', [user.email], fail_silently=False)

                        messages.success(request,
                                         'A message with reset password instructions has been sent to your inbox.')
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    # return redirect ("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="index/reset/password_reset.html", context={"password_reset_form":password_reset_form})


# def login_view(request):
#     error_message = None
#
#     form = LoginForm(request.POST or None)
#     context = {
#         "form": form,
#         'error_message': error_message,
#     }
#     if request.method == 'POST':
#         email = request.POST['email']
#         password = request.POST['password']
#         print(email)
#         print(password)
#         user = authenticate(request, email=email, password=password)
#         if user is not None:
#             # email = user.email
#             # print("My current email is: ", email)
#             send_otp(request)
#             request.session['email'] = email
#             return redirect('otp')
#         else:
#             error_message = 'Invalid email or password'
#             messages.error(request, 'Email or Password is not correct.')
#     return render(request, 'index/login.html', context)


# def otp_view(request):
#     error_message = None
#     if request.method == 'POST':
#         otp = request.POST['otp']
#         email = request.session['email']
#
#         otp_secret_key = request.session['otp_secret_key']
#         otp_valid_date = request.session['otp_valid_date']
#         if otp_secret_key and otp_valid_date is not None:
#             valid_until = datetime.fromisoformat(otp_valid_date)
#
#             if valid_until > datetime.now():
#                 totp = pyotp.TOTP(otp_secret_key, interval=60)
#                 if totp.verify(otp):
#                     user = get_object_or_404(User, email=email)
#                     login(request, user)
#
#                     del request.session['otp_secret_key']
#                     del request.session['otp_valid_date']
#
#                     return redirect('dashboard')
#                 else:
#                     messages.error(request, "Invalid OTP")
#             else:
#                 messages.error(request, "Invalid OTP")
#         else:
#             messages.error(request, "Invalid OTP")
#     return render(request, 'index/login/otp.html')


@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    print("logout Successfully")

    # Take the user back to the homepage.
    return HttpResponseRedirect('/')

# -------------------------------
#                                |
#           Dashboard View
#                                |
# -------------------------------
@login_required(login_url='/signin/')
def dashboard(request):
    customer = Customer.objects.get(account=request.user)
    print(customer.roi_profit)
    print()
    deposit = DepositRequest.objects.filter(user=request.user)

    if deposit:
        deposited = deposit.latest('created_at')
        amount_deposited = deposited.amount_deposited
        if deposited.active:
            print("activated")
            customer.increase_balance(amount_deposited)
            active = False
            deposited.update_active(active)
        else:
            print("Not Deposited")

    # Trading form
    trade = Trading.objects.filter(user=request.user)
    bot = Bot.objects.filter(user=request.user)
    daily_profit = DailyProfitHistory.objects.filter(user=request.user)
    # global bot_plan
    # global trading
    if bot:
        bot_plan = bot.latest('created_at')
    else:
        bot_plan = False
    if trade:
        trading = trade.latest('created_at')
        current_time = datetime.now(timezone.utc).date()
        created = trading.created_at.date()
        total_time = current_time - created
        days = total_time.days
        print("days", days)
    else:
        trading = False
        days = False
    form = TradingForm(request.POST or None)


    context = {
        'form': form,
        'customer': customer,
        'bot_plan': bot_plan,
        'trading': trading,
        'days': days,
    }
    if form.is_valid():
        confirm = form.save(commit=False)
        confirm.user = request.user
        confirm.save()
        messages.success(request, 'Your Trading Successfully Opened.')
        amount = form.cleaned_data.get('amount')
        return redirect('/dashboard/')
    else:
        print("insufficient funds! Minimum Trading Balance 0.05.")
        messages.error(request, 'insufficient funds! Minimum Trading Balance 0.05.')
    return render(request, 'dashboard/index.html', context)

# -------------------------------
#                                |
#           Django Schedule Job
#                                |
# -------------------------------


def schedule_job():
    print("--------------Schedule Job Started--------------------------")

    print("* add balance and clearance *")
    customers = Customer.objects.all()
    for customer in customers:
        roi = customer.roi_profit
        direct_refer = customer.direct_refer_income
        # add to balance
        customer.increase_balance(float(roi))
        customer.increase_balance(float(direct_refer))
        # going to zero after add to balance
        customer.update_roi_profit(float(0.00))
        customer.update_refer_bonus(float(0.00))
        customer.today_percent_increase(float(0.00))

    print("* ROI Profit *")
    traders = Trading.objects.all()
    profit_ratio = 5.69
    for trader in traders:
        if trader.active:
            # print("active trader: ",trader)
            current_time = datetime.now(timezone.utc).date()
            created = trader.created_at.date()
            days = current_time - created
            # print(days.days)
            day = 1
            if days.days >= day:
                print("active trader: ", trader)

                profit_amount = float(trader.amount) * float(profit_ratio) / 100
                print(profit_amount)
                DailyProfitHistory.objects.create(user=trader.user, today_percent=profit_ratio,
                                                         today_profit=profit_amount)
                customer = customers.get(account=trader.user)
                print("Trader name: ", customer)
                customer.today_roi_profit(float(profit_amount))
                customer.today_percent_increase(float(profit_ratio))


scheduler = BackgroundScheduler()
job = None


def start_job():
    global job
    # job = scheduler.add_job(schedule_job, 'cron', hour=10, minute=35)
    job = scheduler.add_job(schedule_job, 'interval', seconds=3)
    try:
        scheduler.start()
    except:
        pass


# start_job()
# -------------------------------
#                                |
#           Django Schedule Job End
#                                |
# -------------------------------

# KYC Views


@login_required
def kyc_view(request):
    if request.method == 'POST':
        form = KYCForm(request.POST, request.FILES)
        if form.is_valid():
            confirm = form.save(commit=False)
            confirm.user = request.user
            confirm.save()
            messages.success(request, 'Successfully Submitted.')
            # Getting the current instance object to display in the template
            img_object = form.instance
            return render(request, 'kyc/kyc.html', {'form': form, 'img_object': img_object})
    else:
        form = KYCForm()
    return render(request, 'kyc/kyc.html', {'form': form})


def profile_view(request):
    """Process images uploaded by users"""
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            confirm = form.save(commit=False)
            confirm.user = request.user
            confirm.save()
            messages.success(request, 'Successfully Submitted.')
            # Get the current instance object to display in the template
            img_obj = form.instance
            return render(request, 'kyc/profile.html', {'form': form, 'img_obj': img_obj})
    else:
        form = ImageForm()
    return render(request, 'kyc/profile.html', {'form': form})


def refer(request):
    return render(request, 'dashboard/refer/refer.html')
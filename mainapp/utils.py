import pyotp
from datetime import datetime, timedelta

# Email
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.core import mail


def send_otp(request):
    totp = pyotp.TOTP(pyotp.random_base32(), interval=60)
    otp = totp.now()
    request.session['otp_secret_key'] = totp.secret
    valid_date = datetime.now() + timedelta(minutes=10)
    request.session['otp_valid_date'] = str(valid_date)

    print(f"Your one time password is {otp}")

    # send_mail('Thanks for joining with Crypto Ethereum Trading Bot',
    #           'An investment in knowledge pays the best interest.\n'
    #           'Crypto Ethereum Bot is the platform where you will be able to make your dream successful.\n'
    #           '\n'
    #           'Web: www.cryptoethbot.com\n'
    #           'Mail: hello@cryptoethbot.com\n'
    #           'Phone: +1 765 775 34',
    #           from_email=settings.EMAIL_HOST_USER,
    #           recipient_list=[email_submitted]
    #           )

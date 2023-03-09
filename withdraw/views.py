from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import WithdrawalData, WithdrawalRequest
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from mainapp.models import Customer, Profile
from django.views import View
from django.utils.decorators import method_decorator

from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.core import mail


@login_required
def withdraw_view(request):
    customer = Customer.objects.get(account=request.user)
    balance = customer.balance
    form = WithrawForm(request.POST or None)
    context = {
        'form': form,
    }
    submit_amount = request.POST.get('withdraw_amount')
    min_withdraw = 0.018

    # submit_amount = request.POST.get('amount_deposited')
    eth_address = request.POST.get('eth_address')
    email = request.user.email
    first_name = request.user.first_name
    last_name = request.user.last_name

    profile = Profile.objects.filter(user=request.user)

    # if profile:
    #     kyc = profile.latest('created_at')
    # else:
    #     kyc = False

    # print(kyc.active)
    # print(f"kyc {{ kyc }}", kyc.avatar)

    connection = mail.get_connection()

    if form.is_valid():
        # withdrawal_charge = float(submit_amount) * 10 / 100
        withdrawal_charge = 1
        withdrawal_amount = float(submit_amount) - float(withdrawal_charge)
        print(withdrawal_amount)
        c = {
            "email": email,
            "user": request.user,
            "first_name": first_name,
            "last_name": last_name,
            "submit_amount": withdrawal_amount,
            "eth_address": eth_address,
        }
        email_template = "withdraw/email.txt"
        email_text = render_to_string(email_template, c)

        try:
            profile = profile.latest('created_at')
            print(profile.active)
            # print(customer.active)
            if profile.active == True:
                if float(withdrawal_amount) <= float(balance):
                    if float(withdrawal_amount) >= float(min_withdraw):
                        confirm = form.save(commit=False)
                        confirm.user = request.user

                        confirm.save()
                        withdraw_now = WithdrawalRequest.objects.latest('created_at')
                        withdraw_now.update_amount(withdrawal_amount)
                        messages.success(request, 'Withdrawal successfully done.')
                        withdraw_amount = form.cleaned_data.get('withdraw_amount')
                        eth_address = form.cleaned_data.get('eth_address')
                        email = EmailMessage(
                            'Your withdrawal request has been successfully done!',
                            email_text,
                            from_email=settings.EMAIL_HOST_USER,
                            to=[email],
                            bcc=['prosenjit.pq@gmail.com', 'kateyalide@gmail.com'],
                            reply_to=['info@cryptoethbot.com'],
                            headers={'Message-ID': 'foo'},
                            connection=connection,
                        )
                        email.send()
                        return redirect('/withdraw-data/')
                    else:
                        messages.error(request, 'Minimum withdraw $20 and withdraw charge $1')
                else:
                    messages.error(request, 'Insufficient Funds and withdraw charge $1')
            else:
                messages.error(request, 'Please submit your KYC')
        except:
            messages.error(request, 'Please submit your KYC')

    return render(request, 'withdraw/withdraw-info.html', context)

# @login_required
# def withdraw_data_view(request):
#     form = WithDataForm(request.POST or None)
#     context = {
#         'form': form,
#     }
#     if form.is_valid():
#         confirm = form.save(commit=False)
#         confirm.user = request.user
#         confirm.save()
#         messages.success(request, 'Address added!')
#         eth_address = form.cleaned_data.get('eth_address')
#         return redirect('/withdraw-data/')
#     return render(request, 'withdraw/withdraw-info.html', context)

# @method_decorator(login_required(login_url='/signin/'), name='dispatch')
# class withdraw_data_view(View):
#     profile = None
#
#     def dispatch(self, request, *args, **kwargs):
#         self.with_data, __ = WithdrawalData.objects.get_or_create(user=request.user)
#         return super(withdraw_data_view, self).dispatch(request, *args, **kwargs)
#
#     def get(self, request):
#         context = {'with_data': self.with_data, 'segment': 'with_data'}
#         return render(request, 'withdraw/withdraw-info.html', context)
#
#     def post(self, request):
#         form = WithDataForm(request.POST, request.FILES, instance=self.with_data)
#
#         if form.is_valid():
#             with_data = form.save()
#             # with_data.user.first_name = form.cleaned_data.get('eth_address')
#             with_data.user.save()
#
#             messages.success(request, 'Profile saved successfully')
#         else:
#             messages.error(request, form_validation_error(form))
#         return redirect('/withdraw-data/')




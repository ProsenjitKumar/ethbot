from django import template
from mainapp.models import Customer, Profile

register = template.Library()


@register.simple_tag
def number_of_messages(request):

    referrals = Customer.objects.get(account=request.user)
    balance = referrals.balance
    return balance

@register.simple_tag
def profile_info(request):

    profile = Profile.objects.filter(account=request.user)
    last = profile.latest('created_at')
    context = {
        'avatar': last.avatar,
    }

    # balance = referrals.balance
    return last.avatar
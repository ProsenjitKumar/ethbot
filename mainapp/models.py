import decimal
import uuid
import enum
from django.db import models
from django.utils import timezone, translation
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

from django_numerators.models import NumeratorMixin
from mptt.models import MPTTModel, TreeForeignKey, TreeManager

_ = translation.gettext_lazy
# from .utils import generate_ref_code, generate_coin_address
from django.templatetags.static import static

from datetime import datetime, timedelta
from django.contrib.auth.models import (
AbstractBaseUser, BaseUserManager
)
from django.db.models.signals import post_save
from django_countries.fields import CountryField

# Create your models here.


'''
******************
Referral
******************
'''


class Customer(NumeratorMixin, MPTTModel, models.Model):
    class Meta:
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')
        unique_together = ('parent', 'account')

    limit = 10000000

    parent = TreeForeignKey(
        'self', null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='downlines',
        verbose_name=_('Up Line'))
    account = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name=_('account'))
    balance = models.DecimalField(
        default=0,
        max_digits=15,
        decimal_places=5,
        blank=True, null=True,
        verbose_name=_("Balance"))

    roi_profit = models.DecimalField(default=0,max_digits=15,decimal_places=5, blank=True, null=True)
    today_percent = models.DecimalField(default=0,max_digits=15, decimal_places=2, blank=True, null=True)
    total_roi_profit = models.DecimalField(default=0,max_digits=15,decimal_places=5, blank=True, null=True)
    level_income = models.DecimalField(default=0,max_digits=15,decimal_places=5, blank=True, null=True)
    total_level_income = models.DecimalField(default=0,max_digits=15,decimal_places=5, blank=True, null=True)
    direct_refer_income = models.DecimalField(default=0,max_digits=15,decimal_places=5, blank=True, null=True)
    total_direct_refer_income = models.DecimalField(default=0,max_digits=15,decimal_places=5, blank=True, null=True)
    bot_profit = models.DecimalField(default=0,max_digits=15,decimal_places=5, blank=True, null=True)
    trading_balance = models.DecimalField(default=0,max_digits=15,decimal_places=5, blank=True, null=True)

    created_at = models.DateTimeField(
        default=timezone.now, editable=False)

    code = models.CharField(max_length=12, blank=True)
    account_address = models.CharField(max_length=60, blank=True, null=True)

    active = models.BooleanField(default=True)
    invested = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    # slug = models.SlugField(null=True, blank=True, unique=True)

    def __str__(self):
        return (
            self.account.username
            if self.account.get_full_name() in ['', None]
            else self.account.get_full_name()
        )

    # Main Balance
    def update_balance(self, balance):
        self.balance = balance
        self.save()

    def decrease_balance(self, balance):
        self.balance -= decimal.Decimal(balance)
        self.save()

    def increase_balance(self, balance):
        self.balance = self.balance + decimal.Decimal(balance)
        self.save()

    # Roi Profit
    def today_roi_profit(self, roi_profit):
        self.roi_profit = self.roi_profit + decimal.Decimal(roi_profit)
        self.save()

    def update_roi_profit(self, roi_profit):
        self.roi_profit = decimal.Decimal(roi_profit)
        self.save()

    # today percent
    def today_percent_increase(self, today_percent):
        self.today_percent = self.today_percent + decimal.Decimal(today_percent)
        self.save()

    def update_percent(self, today_percent):
        self.today_percent = decimal.Decimal(today_percent)
        self.save()

    # Refer Bonus
    def increase_refer_bonus(self, direct_refer_income):
        self.direct_refer_income += decimal.Decimal(direct_refer_income)
        self.save()

    def update_refer_bonus(self, direct_refer_income):
        self.direct_refer_income = decimal.Decimal(direct_refer_income)
        self.save()

    def get_referral_limit(self):
        return getattr(settings, 'REFERRAL_DOWNLINE_LIMIT', None) or self.limit

    def get_uplines(self):
        return self.get_ancestors(include_self=False, ascending=True)[:self.get_referral_limit()]

    def save(self, *args, **kwargs):
        if self.code == "":
            code = self.account
            # account_address = generate_coin_address()
            # self.account_address = account_address
            self.code = code
        super().save(*args, **kwargs)



'''
******************
Settings
******************
'''


# class PinSet(models.Model):
#     user = models.OneToOneField(User, related_name="pin", on_delete=models.CASCADE)
#     pin1 = models.IntegerField(blank=True, null=True)
#     pin2 = models.IntegerField(blank=True, null=True)
#
#     active = models.BooleanField(default=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return self.user.username


# ----------------------------
#
#          Profile
#
# ----------------------------
# class Profile(models.Model):
#     GENDER_MALE = 1
#     GENDER_FEMALE = 2
#     GENDER_CHOICES = [
#         (GENDER_MALE, _("Male")),
#         (GENDER_FEMALE, _("Female")),
#     ]
#
#     user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
#     avatar = models.ImageField(upload_to="customers/profiles/avatars/", null=True, blank=True)
#     birthday = models.DateField(null=True, blank=True)
#     gender = models.PositiveSmallIntegerField(choices=GENDER_CHOICES, null=True, blank=True)
#     phone = models.CharField(max_length=32, null=True, blank=True)
#     address = models.CharField(max_length=255, null=True, blank=True)
#     number = models.CharField(max_length=32, null=True, blank=True)
#     city = models.CharField(max_length=50, null=True, blank=True)
#     zip = models.CharField(max_length=30, null=True, blank=True)
#
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         verbose_name = _('Profile')
#         verbose_name_plural = _('Profiles')
#
#     @property
#     def get_avatar(self):
#         return self.avatar.url if self.avatar else static('assets/img/team/default-profile-picture.png')
#
#     def __str__(self):
#         return self.user.username


'''
******************
Contact and Support
******************
'''


class Contact(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField(blank=True, null=True)

    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# ----------------------------
#
#          Profile
#
# ----------------------------
ID_TYPE = (
    ('1', 'NID'),
    ('2', 'Driving License'),
    ('3', 'Passport'),
)


class KYC(models.Model):
    user = models.ForeignKey(User, related_name="kyc", on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to="customers/profiles/pic/", blank=False)
    nid_front = models.ImageField(upload_to="customers/nid/front/", blank=False)
    nid_back = models.ImageField(upload_to="customers/nid/back/", blank=False)

    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class Profile(models.Model):
    user = models.ForeignKey(User, related_name="profile", on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='pro/', blank=False)
    front = models.ImageField(upload_to='pro/', blank=False)
    back = models.ImageField(upload_to='pro/', blank=False)

    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

#
# # --------------------------------------------
# class UserManager(BaseUserManager):
#     def create_user(self, email, full_name, password=None, is_active=True, is_staff=False, is_admin=False):
#         if not email:
#             raise ValueError("Users must have an Email address.")
#         if not password:
#             raise ValueError("Users must have a Password")
#         if not full_name:
#             raise ValueError("Users must have a Full Name")
#         user_obj = self.model(
#             email = self.normalize_email(email),
#             full_name=full_name
#         )
#         user_obj.set_password(password)
#         user_obj.staff = is_staff
#         user_obj.admin = is_admin
#         user_obj.active = is_active
#         user_obj.save(using=self._db)
#         return user_obj
#
#     def create_staffuser(self, email, full_name, password=None):
#         user = self.create_user(
#             email,
#             full_name,
#             password=password,
#             is_staff=True
#         )
#         return user
#
#     def create_superuser(self, email, full_name, password=None):
#         user = self.create_user(
#             email,
#             full_name,
#             password=password,
#             is_staff=True,
#             is_admin=False # will be True
#         )
#         return user
#
#
# class NewUser(AbstractBaseUser):
#     email = models.EmailField(max_length=255, unique=True)
#     full_name = models.CharField(max_length=255, blank=True, null=True)
#     #address = models.CharField(max_length=455)
#     active = models.BooleanField(default=True) # Can Login
#     staff = models.BooleanField(default=False) # staff user non Superuser
#     admin = models.BooleanField(default=False) # Superuser
#     timestamp = models.DateTimeField(auto_now_add=True)
#     # confirm = models.BooleanField(default=False)
#     # confiremed_date = models.DateTimeField(default=False)
#
#     # Profile
#     # address = models.CharField(max_length=255, default="Bangladesh")
#     balance = models.DecimalField(
#         default=0,
#         max_digits=15,
#         decimal_places=5,
#         blank=True, null=True,
#         verbose_name=_("Balance"))
#
#     roi_profit = models.DecimalField(default=0, max_digits=15, decimal_places=5, blank=True, null=True)
#     today_percent = models.DecimalField(default=0, max_digits=15, decimal_places=2, blank=True, null=True)
#     total_roi_profit = models.DecimalField(default=0, max_digits=15, decimal_places=5, blank=True, null=True)
#     level_income = models.DecimalField(default=0, max_digits=15, decimal_places=5, blank=True, null=True)
#     total_level_income = models.DecimalField(default=0, max_digits=15, decimal_places=5, blank=True, null=True)
#     direct_refer_income = models.DecimalField(default=0, max_digits=15, decimal_places=5, blank=True, null=True)
#     total_direct_refer_income = models.DecimalField(default=0, max_digits=15, decimal_places=5, blank=True, null=True)
#     bot_profit = models.DecimalField(default=0, max_digits=15, decimal_places=5, blank=True, null=True)
#     trading_balance = models.DecimalField(default=0, max_digits=15, decimal_places=5, blank=True, null=True)
#     country = CountryField()
#     update = models.DateTimeField(null=True, blank=True)
#
#     #changed_by = models.ForeignKey('auth.User', on_delete=models.CASCADE)
#
#
#     # Personal Info
#     age = models.IntegerField(blank=True, null=True)
#
#     USERNAME_FIELD = 'email'  # Username
#     # USERNAME_FILED and password are required by default
#     REQUIRED_FIELDS = ['full_name'] # 'full_name'
#
#     objects = UserManager()
#
#
#
#     def __str__(self):
#         return self.email
#
#     def  get_full_name(self):
#         return self.email
#
#     def get_short_name(self):
#         return self.email
#
#     def has_perm(self, perm, obj=None):
#         return True
#
#     def has_module_perms(self, app_label):
#         return True
#
#     @property
#     def is_staff(self):
#         return self.staff
#
#     @property
#     def is_admin(self):
#         return self.admin
#
#     @property
#     def is_active(self):
#         return self.active
#
#
# class GuestEmail(models.Model):
#     email = models.EmailField()
#     active = models.BooleanField(default=True)
#     update = models.DateTimeField(auto_now=True)
#     timestamp = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return self.email
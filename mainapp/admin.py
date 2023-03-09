from django.contrib import admin
from .models import *
# from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin
from mptt.admin import MPTTModelAdmin

# Register your models here.


@admin.register(Customer)
class ReferralAdmin(MPTTModelAdmin):
    list_filter = ['level']
    list_select_related = ['account', 'parent']
    search_fields = ['account__first_name', 'account__last_name']
    list_display = ['inner_id', 'account', 'parent', 'decendants', 'downlines', 'level', 'updated_at', 'created_at', 'balance']

    def decendants(self, obj):
        return obj.get_descendant_count()

    def downlines(self, obj):
        return obj.downlines.count()

    def get_queryset(self, request):
        return super().get_queryset(request).only('inner_id', 'account', 'parent')


admin.site.register(Contact)
admin.site.register(KYC)
admin.site.register(Profile)

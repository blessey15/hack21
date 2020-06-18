from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Account
from profiles.models import ParticipantProfile

# class ParticipantProfileInline(admin.StackedInline):
#     model = ParticipantProfile
#     can_delete = False
#     verbose_name_plural = 'Participant Profile'
#     fk_name = 'user'

class AccountAdmin(UserAdmin):
    # inlines = (ParticipantProfileInline, )
    list_display = ('email', 'username', 'date_joined', 'last_login', 'is_admin', 'is_staff')
    search_fields = ('email', 'username',)
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal =()
    list_filter = ()
    fieldsets = ()

    # def get_inline_instances(self, request, obj=None):
    #     if not obj:
    #         return list()
    #     return super(AccountAdmin, self).get_inline_instances(request, obj)

admin.site.register(Account, AccountAdmin)

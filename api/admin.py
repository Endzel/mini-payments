from django.contrib import admin
from django.utils.translation import ugettext as _

from api.models import UserProfile, Account, Transfer

admin.site.site_header = _('MP Bank')
admin.site.index_title = _('Administration')
admin.site.site_title = _('MP Bank')

admin.site.register(UserProfile)
admin.site.register(Account)
admin.site.register(Transfer)

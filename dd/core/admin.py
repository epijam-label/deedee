"""
Admin for Dee Dee.
"""

from django.contrib import admin

from dd.core.models import Asset, Bundle, EntitlementPolicy


admin.site.register(Asset)
admin.site.register(Bundle)
admin.site.register(EntitlementPolicy)

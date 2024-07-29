"""
Admin for Dee Dee.
"""

from django.contrib import admin

from dd.core.models import Asset, Bundle


admin.site.register(Asset)
admin.site.register(Bundle)

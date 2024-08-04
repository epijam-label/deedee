"""
URL configuration for dd project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from dd.core import apiviews, views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("card/<uuid:card_id>/", views.download_card),
    path("entitlement/<uuid:entitlement_id>/", views.entitlement),
    path("entitlement/<uuid:entitlement_id>/redeem/", views.redeem_entitlement),
    path("token/<uuid:token_id>/", views.download_token),
    path("download/<uuid:download_session_id>/<uuid:asset_id>/", views.download_asset),
    # path("api/entitle/<uuid:bundle_id>/", apiviews.EntitleView.as_view()),
    path("api/fulfill/", apiviews.FulfillmentView.as_view()),
]

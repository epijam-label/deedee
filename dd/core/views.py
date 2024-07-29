"""
Regular webviews.
"""
from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect, FileResponse

from dd.core.models import Entitlement, Token, DownloadSession, Asset, DownloadCard
from dd.core.forms import EmailCaptureForm


def download_card(request, card_id):
    """
    Views a download card.
    """
    try:
        card = DownloadCard.objects.get(pk=card_id)

        # check if the card has been used
        form = None
        if request.method == "POST" and not card.used:
            form = EmailCaptureForm(request.POST)
            if form.is_valid():
                form.write_email(card)
                entitlement = card.grant_entitlement()
                return HttpResponseRedirect(f"/entitlement/{entitlement.pk}/")
        else:
            form = EmailCaptureForm()

        return render(
            request, "core/download_card.html", context={"card": card, "form": form}
        )
    except DownloadCard.DoesNotExist:
        raise Http404()


def entitlement(request, entitlement_id):
    """
    Loads the specified entitlement.
    """
    try:
        entitlement_obj = Entitlement.objects.get(pk=entitlement_id)
        return render(
            request, "core/entitlement.html", context={"entitlement": entitlement_obj}
        )
    except Entitlement.DoesNotExist:
        raise Http404()


def redeem_entitlement(request, entitlement_id):
    """
    This will generate a token and send the user to a download session where the assets
    are available.
    """
    try:
        entitlement_obj = Entitlement.objects.get(pk=entitlement_id)
        token = entitlement_obj.create_token()
        return HttpResponseRedirect(f"/token/{token.pk}/")
    except Entitlement.AllowanceExceeded:
        return HttpResponseRedirect(f"/entitlement/{entitlement.pk}/")
    except Entitlement.DoesNotExist:
        raise Http404()


def download_token(request, token_id):
    """
    If token found and not used, will initiate a download session.
    """
    try:
        download_session = None
        token = Token.objects.get(pk=token_id)
        if not token.used:
            # token is good, initiate download session
            download_session = token.create_session()

        return render(
            request,
            "core/token.html",
            context={"token": token, "download_session": download_session},
        )

    except Token.DoesNotExist:
        raise Http404()


def download_asset(request, download_session_id, asset_id):
    """
    Downloads the specified asset if there is a valid download session.
    """
    try:
        download_session = DownloadSession.objects.get(pk=download_session_id)
        asset = Asset.objects.get(pk=asset_id)
        if download_session.is_valid():
            response = FileResponse(asset.asset_file, as_attachment=True)
            return response
        else:
            return render(
                request, "core/token.html", context={"token": download_session.token}
            )
    except DownloadSession.DoesNotExist:
        raise Http404()
    except Asset.DoesNotExist:
        raise Http404()

"""
Views for DD.
"""

from rest_framework import views
from rest_framework import status
from rest_framework.response import Response

from dd.core.models import Bundle


class EntitleView(views.APIView):
    """
    View to CRUD an entitlement.
    """

    def post(self, request, bundle_id):
        """
        Creates an entitlement for the specified recipient.
        """
        try:
            bundle = Bundle.objects.get(pk=bundle_id)
            recipient = request.POST.get("recipient", None)

            if not recipient:
                return Response(status=status.HTTP_409_CONFLICT)

            entitlements = bundle.grant_entitlements(recipient)
            return Response(
                {"entitlements": [ent.pk for ent in entitlements]},
                status=status.HTTP_201_CREATED,
            )

        except Bundle.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

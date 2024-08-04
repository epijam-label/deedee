"""
Views for DD.
"""

from rest_framework import views
from rest_framework import status
from rest_framework.response import Response

from dd.core.models import Bundle
from dd.utils import verify_shopify_webhook


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

            entitlement = bundle.grant_entitlement(recipient)
            return Response(
                {"entitlement": entitlement.pk},
                status=status.HTTP_201_CREATED,
            )

        except Bundle.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class FulfillmentView(views.APIView):
    """
    Creates an entitlement from a Shopify fulfillment webhook, but also sends
    notification email to the entitled.
    """
    
    authentication_classes = [] # open endpoint
    permission_classes = []

    def post(self, request):
        """
        Creates the entitlement from the payload.
        """
        if not verify_shopify_webhook(request=request):
            return Response(status=status.HTTP_403) # TODO: refactor to auth class
        
        # TODO: The actual webhook structure isn't 100% clear, so it's necessary
        # to figure out whether the stuff we need in order to create the fulfillment
        # is present and where it lives in the JSON structure exactly.

        # Job here is to create the entitlement, send a notification email
        # to the customer
        print(request.data)
        return Response(status=status.HTTP_200_OK)

        # ent_items = request.data["fulfillment"]["fulfillment_line_items"]


#         customer_email = request.data["email"]
#         for ent_item in ent_items:
#             item_sku = ent_item["line_item"]["variant"]["sku"]
#             try:
#                 bundle = Bundle.objects.get(pk=sku)

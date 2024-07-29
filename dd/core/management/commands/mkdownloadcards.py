"""
Management command to create download cards.
"""

from django.core.management.base import BaseCommand, CommandError

from dd.core.models import Bundle, DownloadCard


class Command(BaseCommand):
    """
    Command class.
    """

    help = "Creates download cards that can be used to create entitelements."

    def add_arguments(self, parser):
        """
        Configures args for command.
        """
        parser.add_argument(
            "--quantity",
            dest="quantity",
            type=int,
            default=1,
            required=False,
            help="Quantity of download cards to create",
        )
        parser.add_argument(
            "--bundle", dest="bundle", help="ID of the bundle to target"
        )

    def handle(self, *args, **options):
        """
        Handler method.
        """
        try:
            bundle = Bundle.objects.get(pk=options["bundle"])

            print("")
            print("Download Cards")
            print("--------------")

            for i in range(options["quantity"]):
                dcard = DownloadCard.objects.create(bundle=bundle)
                print(dcard.pk)
            print("")
        except Bundle.DoesNotExist:
            bundle_id = options["bundle"]
            print(f"{bundle_id} is not a recognized bundle.")

from django.contrib.auth.models import Group
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = "Creates Groups"

    def add_arguments(self, parser):
        parser.add_argument("name", type=str, help="Indicates the name of the group")

    def handle(self, *args, **options):
        name = options["name"]

        if name:
            Group.objects.update_or_create(name=name)
            self.stdout.write(
                self.style.SUCCESS("Group '%s' created successfully." % name)
            )
        else:
            self.stdout.write(
                self.style.ERROR("Creating group failed, please mention group name.")
            )

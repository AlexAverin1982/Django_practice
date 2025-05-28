from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = "Add access control groups to the database"

    def handle(self, *args, **kwargs) -> None:
        Group.objects.all().delete()

        products_moderators = Group.objects.create(name='Модераторы продуктов')
        delete_product = Permission.objects.get(codename='delete_product')
        can_unpublish_product = Permission.objects.get(codename='can_unpublish_product')

        products_moderators.permissions.add(delete_product, can_unpublish_product)
        group = Group.objects.get(name='Модераторы продуктов')

        if group:
            self.stdout.write(
                self.style.SUCCESS(f"Successfully added Group: {group.name}")
            )
        else:
            self.stdout.write(
                self.style.WARNING(f"Group already exists: {group.name}")
            )

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = "Add access control groups to the database"

    def handle(self, *args, **kwargs) -> None:
        Group.objects.all().delete()

        content_managers = Group.objects.create(name='Модераторы продуктов')
        delete_product = Permission.objects.get(codename='delete_product')
        can_unpublish_product = Permission.objects.get(codename='can_unpublish_product')

        content_managers.permissions.add(delete_product, can_unpublish_product)
        group = Group.objects.get(name='Модераторы продуктов')

        if group:
            self.stdout.write(
                self.style.SUCCESS(f"Successfully added Group: {group.name}")
            )
        else:
            self.stdout.write(
                self.style.WARNING(f"Group already exists: {group.name}")
            )

        content_managers = Group.objects.create(name='Контент-менеджеры')
        add_blogrecord = Permission.objects.get(codename='add_blogrecord')
        edit_blogrecord = Permission.objects.get(codename='change_blogrecord')
        delete_blogrecord = Permission.objects.get(codename='delete_blogrecord')

        content_managers.permissions.add(add_blogrecord, edit_blogrecord, delete_blogrecord)
        group = Group.objects.get(name='Контент-менеджеры')

        if group:
            self.stdout.write(
                self.style.SUCCESS(f"Successfully added Group: {group.name}")
            )
        else:
            self.stdout.write(
                self.style.WARNING(f"Group already exists: {group.name}")
            )

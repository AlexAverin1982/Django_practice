from django.core.management.base import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):
    help = "Add test products to the database"

    def handle(self, *args, **kwargs) -> None:
        Product.objects.all().delete()
        cat_veg, _ = Category.objects.get_or_create(name="Овощи свежие")

        vegetables = [
            {
                "name": "Картофель Мордова",
                "price": 90.99,
                "description": "Описание продукта",
                "category": cat_veg,
            },
            {
                "name": "Огурцы грунтовые",
                "price": 85.99,
                "description": "Описание продукта",
                "category": cat_veg,
            },
            {
                "name": "Огурцы гладкие",
                "price": 70.99,
                "description": "Описание продукта",
                "category": cat_veg,
            },
            {
                "name": "Лук репчатый",
                "price": 14.99,
                "description": "Описание продукта",
                "category": cat_veg,
            },
            {
                "name": "Помидоры парниковые",
                "price": 124.99,
                "description": "Описание продукта",
                "category": cat_veg,
            },
            {
                "name": "Помидоры черри",
                "price": 184.99,
                "description": "Описание продукта",
                "category": cat_veg,
            },
        ]

        for v_data in vegetables:
            veg, created = Product.objects.get_or_create(**v_data)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Successfully added product: {veg.name}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"Product already exists: {veg.name}")
                )

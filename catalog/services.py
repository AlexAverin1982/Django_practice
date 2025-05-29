from .models import Product

class ProductService:

    @staticmethod
    def products_of_category(category_id) -> list[Product]:
        result = Product.objects.all().filter(category__id=category_id)
        return result
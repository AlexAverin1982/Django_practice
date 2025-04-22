from django.contrib import admin

from .models import Category, ContactsInfo, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "category")
    list_filter = ("category",)
    search_fields = (
        "name",
        "description",
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_filter = ("name",)
    search_fields = (
        "name",
        "description",
    )


@admin.register(ContactsInfo)
class ContactsInfoAdmin(admin.ModelAdmin):
    list_display = ("email", "telegram", "vk_group", "updated_at")
    list_filter = ("updated_at",)
    search_fields = (
        "email",
        "telegram",
        "vk_group",
    )

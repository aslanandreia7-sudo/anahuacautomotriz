from django.contrib import admin
from django.utils.html import format_html
from .models import Brand, CarModel, Car, CarImage, SiteSettings, HomeCarousel

# --- INLINES ---

class CarModelInline(admin.TabularInline):
    model = CarModel
    extra = 1


class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 3


# --- CONFIGURACIÓN Y UI ---

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()


@admin.register(HomeCarousel)
class HomeCarouselAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active')
    list_editable = ('order', 'is_active')


# --- CATÁLOGO DE VEHÍCULOS ---

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ["name", "logo_thumbnail", "is_active"]
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ["is_active"]
    inlines = [CarModelInline]

    def logo_thumbnail(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" style="height:40px;border-radius:4px" />',
                obj.logo.url
            )
        return "-"
    logo_thumbnail.short_description = "Logo"


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ["name", "brand", "year_range", "is_active"]
    list_filter = ["brand", "is_active"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ["title", "brand_name", "price", "year", "condition", "is_available", "is_featured"]
    list_filter = ["car_model__brand", "condition", "fuel_type", "is_available"]
    list_editable = ["is_available", "is_featured", "price"]
    search_fields = ["title", "description"]
    readonly_fields = ["slug", "created_at"]
    inlines = [CarImageInline]

    fieldsets = (
        ("Información General", {
            "fields": ("car_model", "title", "slug", "description")
        }),
        ("Especificaciones Técnicas", {
            "fields": ("price", "mileage", "year", "color", "condition", "transmission", "fuel_type", "engine", "doors")
        }),
        ("Estado y Visibilidad", {
            "fields": ("is_available", "is_featured", "created_at")
        }),
        ("Multimedia", {
            "fields": ("main_image",)
        }),
    )

    def brand_name(self, obj):
        return obj.car_model.brand.name
    brand_name.short_description = "Marca"
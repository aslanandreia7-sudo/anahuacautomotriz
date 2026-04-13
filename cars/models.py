from django.db import models
from django.utils.text import slugify

# --- CONFIGURACIÓN Y UI DEL SITIO ---

class SiteSettings(models.Model):
    site_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=30)
    whatsapp = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    email = models.EmailField()
    hero_title = models.CharField(max_length=255)
    hero_subtitle = models.TextField()
    logo = models.ImageField(upload_to="site/")

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return "Configuración del sitio"


class HomeCarousel(models.Model):
    title = models.CharField(max_length=150, verbose_name="Título (Opcional)", blank=True)
    subtitle = models.CharField(max_length=250, verbose_name="Subtítulo (Opcional)", blank=True)
    image = models.ImageField(upload_to="carousel/", verbose_name="Imagen Landscape")
    order = models.PositiveIntegerField(default=0, verbose_name="Orden de aparición")
    is_active = models.BooleanField(default=True, verbose_name="¿Está activo?")

    class Meta:
        verbose_name = "Imagen de Carrusel"
        verbose_name_plural = "Imágenes de Carrusel"
        ordering = ['order']

    def __str__(self):
        return self.title if self.title else f"Imagen {self.id}"


# --- CATÁLOGO DE VEHÍCULOS ---

class Brand(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, blank=True)
    logo = models.ImageField(upload_to="brands/")
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class CarModel(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="car_models")
    name = models.CharField(max_length=120)
    slug = models.SlugField(blank=True)
    year_range = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("brand", "slug")
        ordering = ["brand__name", "name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.brand.name} {self.name}"


class Car(models.Model):
    CONDITION_CHOICES = [
        ("NUEVO", "Nuevo"),
        ("SEMINUEVO", "Seminuevo"),
        ("CERTIFICADO", "Certificado"),
    ]

    TRANSMISSION_CHOICES = [
        ("MANUAL", "Manual"),
        ("AUTOMATICA", "Automática"),
        ("CVT", "CVT"),
    ]

    FUEL_CHOICES = [
        ("GASOLINA", "Gasolina"),
        ("DIESEL", "Diésel"),
        ("ELECTRICO", "Eléctrico"),
        ("HIBRIDO", "Híbrido"),
    ]

    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE, related_name="cars")
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    mileage = models.PositiveIntegerField(default=0)
    year = models.PositiveIntegerField()
    color = models.CharField(max_length=50)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES)
    fuel_type = models.CharField(max_length=20, choices=FUEL_CHOICES)
    engine = models.CharField(max_length=100)
    doors = models.PositiveSmallIntegerField(default=4)
    description = models.TextField()
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    main_image = models.ImageField(upload_to="cars/main/")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def brand(self):
        return self.car_model.brand

    def __str__(self):
        return self.title


class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="carimages")
    image = models.ImageField(upload_to="cars/gallery/")
    caption = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Imagen de {self.car.title}"
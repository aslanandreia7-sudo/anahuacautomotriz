from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Brand, CarModel, Car, SiteSettings, HomeCarousel

def home(request):
    brands = Brand.objects.filter(is_active=True)
    
    # Obtenemos los slides del carrusel configurados
    carousel_slides = HomeCarousel.objects.filter(is_active=True).order_by('order')
    
    # Intentamos traer los destacados aleatorios
    featured_cars = Car.objects.filter(
        is_available=True, 
        is_featured=True
    ).order_by('?')[:5]

    # PLAN B: Si no hay destacados, traemos los últimos 5 disponibles
    if not featured_cars.exists():
        featured_cars = Car.objects.filter(is_available=True).order_by('-created_at')[:5]
    
    available_count = Car.objects.filter(is_available=True).count()
    settings = SiteSettings.objects.first()

    return render(request, "concesionaria/home.html", {
        "brands": brands,
        "carousel_slides": carousel_slides,
        "featured_cars": featured_cars,
        "available_count": available_count,
        "settings": settings,
    })


def catalog(request):
    cars = Car.objects.filter(is_available=True).select_related("car_model", "car_model__brand")
    brands = Brand.objects.filter(is_active=True)

    brand = request.GET.get("brand")
    model = request.GET.get("model")
    condition = request.GET.get("condition")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    year = request.GET.get("year")
    q = request.GET.get("q")
    order = request.GET.get("order")

    if brand:
        cars = cars.filter(car_model__brand__slug=brand)
    if model:
        cars = cars.filter(car_model__slug=model)
    if condition:
        cars = cars.filter(condition=condition)
    if min_price:
        cars = cars.filter(price__gte=min_price)
    if max_price:
        cars = cars.filter(price__lte=max_price)
    if year:
        cars = cars.filter(year=year)
    if q:
        cars = cars.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q) |
            Q(color__icontains=q)
        )

    if order == "price_asc":
        cars = cars.order_by("price")
    elif order == "price_desc":
        cars = cars.order_by("-price")
    elif order == "mileage":
        cars = cars.order_by("mileage")
    else:
        cars = cars.order_by("-created_at")

    paginator = Paginator(cars, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "concesionaria/catalog.html", {
        "page_obj": page_obj,
        "brands": brands,
    })


def brand_catalog(request, brand_slug):
    brand = get_object_or_404(Brand, slug=brand_slug, is_active=True)
    models = brand.car_models.filter(is_active=True)
    cars = Car.objects.filter(car_model__brand=brand, is_available=True)
    return render(request, "concesionaria/catalog.html", {
        "selected_brand": brand,
        "models": models,
        "page_obj": cars,
        "brands": Brand.objects.filter(is_active=True),
    })


def model_catalog(request, brand_slug, model_slug):
    brand = get_object_or_404(Brand, slug=brand_slug, is_active=True)
    model = get_object_or_404(CarModel, brand=brand, slug=model_slug, is_active=True)
    cars = Car.objects.filter(car_model=model, is_available=True)
    return render(request, "concesionaria/catalog.html", {
        "selected_brand": brand,
        "selected_model": model,
        "page_obj": cars,
        "brands": Brand.objects.filter(is_active=True),
    })


def car_detail(request, slug):
    car = get_object_or_404(Car.objects.select_related("car_model", "car_model__brand"), slug=slug)
    images = car.carimages.all()
    related_cars = Car.objects.filter(
        car_model__brand=car.car_model.brand,
        is_available=True
    ).exclude(id=car.id)[:4]

    return render(request, "concesionaria/car_detail.html", {
        "car": car,
        "images": images,
        "related_cars": related_cars,
    })


def search(request):
    q = request.GET.get("q", "")
    cars = Car.objects.filter(
        Q(title__icontains=q) |
        Q(description__icontains=q) |
        Q(year__icontains=q) |
        Q(color__icontains=q),
        is_available=True
    )
    return render(request, "concesionaria/search_results.html", {
        "cars": cars,
        "query": q,
    })


def contact(request):
    return render(request, "concesionaria/contact.html")
from django.shortcuts import render
from tienda.models import Category, Product
from panel_admin.models import Banner


def home(request):
    products = Product.objects.filter(activo=True).select_related('category')[:12]
    categories = Category.objects.filter(activa=True)[:6]
    banners = Banner.objects.filter(activo=True)[:3]
    destacados = Product.objects.filter(activo=True).order_by('-created')[:4]
    return render(request, 'tienda/home.html', {
        'products': products,
        'categories': categories,
        'banners': banners,
        'destacados': destacados,
    })


def product_list(request):
    products = Product.objects.filter(activo=True).select_related('category')
    categories = Category.objects.filter(activa=True)
    q = request.GET.get('q', '')
    cat_id = request.GET.get('cat', '')
    if q:
        products = products.filter(name__icontains=q)
    if cat_id:
        products = products.filter(category_id=cat_id)
    return render(request, 'tienda/product_list.html', {
        'products': products,
        'categories': categories,
        'q': q,
        'cat_id': cat_id,
    })


def category_list(request):
    categories = Category.objects.filter(activa=True)
    return render(request, 'tienda/category_list.html', {'categories': categories})


def category_detail(request, category_id):
    from django.shortcuts import get_object_or_404
    category = get_object_or_404(Category, id=category_id, activa=True)
    products = category.products.filter(activo=True)
    return render(request, 'tienda/category_detail.html', {
        'category': category,
        'products': products,
    })


def product_detail(request, product_id):
    from django.shortcuts import get_object_or_404
    product = get_object_or_404(Product, id=product_id, activo=True)
    related = Product.objects.filter(category=product.category, activo=True).exclude(id=product.id)[:4]
    reviews = product.reviews.select_related('user').all()
    return render(request, 'tienda/product_detail.html', {
        'product': product,
        'related': related,
        'reviews': reviews,
    })

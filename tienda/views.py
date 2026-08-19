from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Category, Product
from .forms import ProductSearchForm


def home(request):
    products = Product.objects.filter(available=True, featured=True)[:8]
    categories = Category.objects.all()
    return render(request, 'tienda/home.html', {
        'products': products,
        'categories': categories,
    })


def product_list(request):
    products = Product.objects.filter(available=True)
    form = ProductSearchForm(request.GET)
    if form.is_valid() and form.cleaned_data['q']:
        query = form.cleaned_data['q']
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    return render(request, 'tienda/product_list.html', {
        'products': products,
        'form': form,
    })


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'tienda/category_list.html', {'categories': categories})


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, available=True)
    return render(request, 'tienda/category_detail.html', {
        'category': category,
        'products': products,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    related = Product.objects.filter(category=product.category, available=True).exclude(id=product.id)[:4]
    return render(request, 'tienda/product_detail.html', {
        'product': product,
        'related': related,
    })

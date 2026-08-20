import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jp_market.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from tienda.models import Category, Product

categories_data = [
    {'name': 'Bebidas', 'description': 'Gaseosas, jugos, agua y bebidas en general'},
    {'name': 'Lacteos', 'description': 'Leche, queso, yogurt y productos lacteos'},
    {'name': 'Panaderia', 'description': 'Pan, tortas, galletas y reposteria'},
    {'name': 'Frutas y Verduras', 'description': 'Frutas frescas y verduras de temporada'},
    {'name': 'Limpieza', 'description': 'Productos de aseo y limpieza del hogar'},
    {'name': 'Carnes', 'description': 'Carnes frescas, pollo y pescados'},
    {'name': 'Snacks', 'description': 'Papas fritas, mani, galletas y botanas'},
    {'name': 'Abarrotes', 'description': 'Arroz, aceite, fideos, conservas y mas'},
]

products_data = {
    'Bebidas': [
        ('Inca Kola 1.5L', 'Gaseosa sabor original peruana', 5.50, 50),
        ('Coca Cola 500ml', 'Gaseosa Coca Cola botella personal', 2.50, 80),
        ('Agua San Luis 625ml', 'Agua purificada', 1.80, 100),
        ('Jugo D\'Norte 1L', 'Jugo de naranja natural', 4.20, 35),
    ],
    'Lacteos': [
        ('Leche Gloria 400g', 'Leche evaporada entera', 3.80, 60),
        ('Queso Paria 400g', 'Queso fresco peruano', 8.50, 25),
        ('Yogurt Laive 170g', 'Yogurt de fresa', 2.20, 40),
        ('Mantequilla Primor 200g', 'Mantequilla con sal', 6.80, 20),
    ],
    'Panaderia': [
        ('Pan Frances (6u)', 'Pan frances fresco de la hornada', 3.50, 30),
        ('Pan Wawa', 'Pan dulce relleno de manjar', 1.80, 40),
        ('Torta Tres Leches', 'Porcion de torta tres leches', 8.00, 10),
        ('Galletas Casino 145g', 'Galletas sabor choco', 3.20, 25),
    ],
    'Frutas y Verduras': [
        ('Platano Grande (1kg)', 'Platano fresco de la costa', 3.00, 50),
        ('Palta Hass (1kg)', 'Palta Hass importada', 15.90, 15),
        ('Tomate (1kg)', 'Tomate fresco nacional', 4.50, 40),
        ('Cebolla (1kg)', 'Cebolla roja criolla', 3.80, 35),
    ],
    'Limpieza': [
        ('Detergente Aromax 500g', 'Detergente en polvo para ropa', 6.50, 30),
        ('Cloro Clorox 1L', 'Desinfectante multi-uso', 5.20, 25),
        ('Jabon Asepxia 3u', 'Jabon limpiador facial', 7.80, 15),
        ('Bolsa Basura 30L', 'Rollo de 25 bolsas', 4.50, 40),
    ],
    'Carnes': [
        ('Pechuga de Pollo 1kg', 'Pechuga fresca sin hueso', 14.90, 30),
        ('Carne Molida 1kg', 'Carne molida de res', 18.50, 20),
        ('Chuleta de Cerdo 1kg', 'Chuletas frescas de cerdo', 16.80, 15),
        ('Tilapia Entera 1kg', 'Tilapia fresca de acquicultura', 12.90, 12),
    ],
    'Snacks': [
        ('Papas Lay\'s 150g', 'Papas fritas sabor original', 4.50, 40),
        ('Mani Moli 200g', 'Mani salado tostado', 3.80, 30),
        ('Golpe 100g', 'Snack de maiz sabor pollo', 2.50, 50),
        ('Crocantels 250g', 'Galletas de soda', 3.20, 25),
    ],
    'Abarrotes': [
        ('Arroz Costeno 1kg', 'Arroz grano largo', 3.50, 80),
        ('Aceite Primor 900ml', 'Aceite vegetal de palma', 8.90, 40),
        ('Fideos Don Victor 500g', 'Spaghetti al huevo', 3.20, 35),
        ('Atun Florida 170g', 'Atun en aceite de oliva', 5.80, 30),
    ],
}

print('Creando categorias...')
for c_data in categories_data:
    cat, created = Category.objects.get_or_create(name=c_data['name'], defaults={'description': c_data['description']})
    if created:
        print(f'  + {cat.name}')

print('Creando productos...')
for cat_name, products in products_data.items():
    cat = Category.objects.get(name=cat_name)
    for name, desc, price, stock in products:
        p, created = Product.objects.get_or_create(
            name=name, category=cat,
            defaults={'description': desc, 'price': price, 'stock': stock}
        )
        if created:
            print(f'  + {p.name} (S/.{price})')

print(f'Done! {Category.objects.count()} categorias, {Product.objects.count()} productos creados.')

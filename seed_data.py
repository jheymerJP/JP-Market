import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jp_market.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from tienda.models import Category, Product
from django.core.files.base import ContentFile
import io
from PIL import Image


def create_placeholder_image(name, size=(400, 400), color=(37, 99, 235)):
    img = Image.new('RGB', size, color)
    buf = io.BytesIO()
    img.save(buf, 'JPEG')
    return ContentFile(buf.getvalue(), f'{name}.jpg')


def seed():
    categories_data = [
        {'name': 'Electronica', 'slug': 'electronica', 'description': 'Celulares, tablets, audifonos y mas', 'order': 1},
        {'name': 'Ropa', 'slug': 'ropa', 'description': 'Moda para toda la familia', 'order': 2},
        {'name': 'Hogar', 'slug': 'hogar', 'description': 'Todo para tu hogar', 'order': 3},
        {'name': 'Deportes', 'slug': 'deportes', 'description': 'Articulos deportivos', 'order': 4},
        {'name': 'Belleza', 'slug': 'belleza', 'description': 'Productos de cuidado personal', 'order': 5},
        {'name': 'Tecnologia', 'slug': 'tecnologia', 'description': 'Accesorios y gadgets tecnologicos', 'order': 6},
    ]

    categories = {}
    for data in categories_data:
        cat, created = Category.objects.get_or_create(slug=data['slug'], defaults=data)
        categories[data['slug']] = cat
        if created:
            img = create_placeholder_image(f'cat_{data["slug"]}', (400, 300))
            cat.image.save(f'cat_{data["slug"]}.jpg', img, save=True)
            print(f'  Categoria creada: {cat.name}')

    products_data = [
        {'name': 'iPhone 15 Pro', 'slug': 'iphone-15-pro', 'description': 'El iPhone mas avanzado con chip A17 Pro, camara de 48MP y pantalla Super Retina XDR de 6.1 pulgadas.', 'price': 4999000, 'stock': 15, 'featured': True, 'category': 'electronica', 'color': (0, 122, 255)},
        {'name': 'Samsung Galaxy S24', 'slug': 'samsung-galaxy-s24', 'description': 'Smartphone Samsung con pantalla Dynamic AMOLED 2X de 6.2 pulgadas y camara de 50MP.', 'price': 3599000, 'stock': 20, 'featured': True, 'category': 'electronica', 'color': (30, 30, 30)},
        {'name': 'AirPods Pro 2', 'slug': 'airpods-pro-2', 'description': 'Audifonos inalambricos con cancelacion activa de ruido y audio espacial.', 'price': 899000, 'stock': 30, 'featured': True, 'category': 'electronica', 'color': (240, 240, 240)},
        {'name': 'iPad Air', 'slug': 'ipad-air', 'description': 'Tablet Apple con chip M1, pantalla Liquid Retina de 10.9 pulgadas.', 'price': 2799000, 'stock': 10, 'category': 'electronica', 'color': (100, 100, 100)},

        {'name': 'Camiseta Basica', 'slug': 'camiseta-basica', 'description': 'Camiseta de algodon 100%, disponible en varios colores. Perfecta para el dia a dia.', 'price': 45000, 'stock': 50, 'featured': True, 'category': 'ropa', 'color': (37, 99, 235)},
        {'name': 'Jean Clasico', 'slug': 'jean-clasico', 'description': 'Jean de mezclilla clasico, ajuste regular, comodo y duradero.', 'price': 120000, 'stock': 35, 'category': 'ropa', 'color': (50, 80, 150)},
        {'name': 'Zapatillas Running', 'slug': 'zapatillas-running', 'description': 'Zapatillas deportivas para running con amortiguacion premium.', 'price': 280000, 'stock': 25, 'featured': True, 'category': 'ropa', 'color': (220, 50, 50)},
        {'name': 'Chaqueta Impermeable', 'slug': 'chaqueta-impermeable', 'description': 'Chaqueta tecnica impermeable, ideal para lluvia y viento.', 'price': 180000, 'stock': 15, 'category': 'ropa', 'color': (40, 40, 40)},

        {'name': 'Aspiradora Robot', 'slug': 'aspiradora-robot', 'description': 'Aspiradora robot con navegacion inteligente y limpieza automatica.', 'price': 899000, 'stock': 8, 'featured': True, 'category': 'hogar', 'color': (50, 200, 50)},
        {'name': 'Juego de Sartenes', 'slug': 'juego-de-sartenes', 'description': 'Set de 5 sartenes antiadherentes de alta calidad.', 'price': 250000, 'stock': 12, 'category': 'hogar', 'color': (180, 180, 180)},
        {'name': 'Cama Queen', 'slug': 'cama-queen', 'description': 'Cama queen size con cabecera tapizada y almacenamiento.', 'price': 1200000, 'stock': 5, 'category': 'hogar', 'color': (139, 90, 43)},

        {'name': 'Balon de Futbol', 'slug': 'balon-futbol', 'description': 'Balon de futbol profesional tamaño 5, material PU de alta calidad.', 'price': 85000, 'stock': 40, 'featured': True, 'category': 'deportes', 'color': (255, 255, 255)},
        {'name': 'Mancuernas Set', 'slug': 'mancuernas-set', 'description': 'Set de mancuernas ajustables de 2 a 20 kg.', 'price': 350000, 'stock': 10, 'category': 'deportes', 'color': (60, 60, 60)},
        {'name': 'Bicicleta Montaña', 'slug': 'bicicleta-montana', 'description': 'Bicicleta de montaña 21 velocidades con frenos de disco.', 'price': 1500000, 'stock': 7, 'category': 'deportes', 'color': (200, 30, 30)},

        {'name': 'Perfume Premium', 'slug': 'perfume-premium', 'description': 'Fragancia premium para hombre, notas de madera y cuero. 100ml.', 'price': 220000, 'stock': 20, 'featured': True, 'category': 'belleza', 'color': (80, 20, 80)},
        {'name': 'Kit Cuidado Facial', 'slug': 'kit-cuidado-facial', 'description': 'Kit completo de limpieza y cuidado facial con 6 productos.', 'price': 150000, 'stock': 18, 'category': 'belleza', 'color': (200, 180, 160)},

        {'name': 'Smartwatch Pro', 'slug': 'smartwatch-pro', 'description': 'Reloj inteligente con GPS, monitor de ritmo cardiaco y 7 dias de bateria.', 'price': 599000, 'stock': 22, 'featured': True, 'category': 'tecnologia', 'color': (20, 20, 20)},
        {'name': 'Cargador Inalambrico', 'slug': 'cargador-inalambrico', 'description': 'Cargador inalambrico rapido 15W compatible con todos los smartphones.', 'price': 65000, 'stock': 45, 'category': 'tecnologia', 'color': (240, 240, 240)},
        {'name': 'Audifonos Bluetooth', 'slug': 'audifonos-bluetooth', 'description': 'Audifonos bluetooth over-ear con 30 horas de bateria.', 'price': 180000, 'stock': 28, 'category': 'tecnologia', 'color': (50, 50, 50)},
    ]

    for data in products_data:
        cat_slug = data.pop('category')
        color = data.pop('color')
        data['category'] = categories[cat_slug]
        product, created = Product.objects.get_or_create(slug=data['slug'], defaults=data)
        if created:
            img = create_placeholder_image(f'prod_{data["slug"]}', (400, 400), color)
            product.image.save(f'prod_{data["slug"]}.jpg', img, save=True)
            print(f'  Producto creado: {product.name}')

    print('\nBase de datos poblada exitosamente!')


if __name__ == '__main__':
    seed()

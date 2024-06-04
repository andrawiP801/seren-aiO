import os
import django
from django.core.files import File
from myproject.settings import MEDIA_ROOT

# Configura Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SerenAI.settings')
django.setup()

from chatai.models import Book

# Define la carpeta donde están tus imágenes
covers_folder = os.path.join(MEDIA_ROOT, 'book_covers')

# Lista de libros y sus respectivas portadas y URLs
books_data = [
    {'title': 'La inteligencia emocional', 'author': 'Daniel Goleman', 'cover': 'la_inteligencia_emocional.jpg', 'url': 'http://www.cutonala.udg.mx/sites/default/files/adjuntos/inteligencia_emocional_daniel_goleman.pdf'},
    {'title': 'El poder del ahora', 'author': 'Eckhart Tolle', 'cover': 'el_poder_del_ahora.jpg', 'url': 'https://example.com/book1'},
    {'title': 'Mujeres que corren con los lobos', 'author': 'Clarissa Pinkola Estés', 'cover': 'mujeres_que_corren_con_los_lobos.jpg', 'url': 'https://example.com/book1'},
    {'title': 'El camino del artista', 'author': 'Julia Cameron	', 'cover': 'el_camino_del_artista.jpg', 'url': 'https://example.com/book1'},
    {'title': 'Las cuatro revelaciones', 'author': 'Alberto Villoldo', 'cover': 'las_cuatro_revelaciones.jpg', 'url': 'https://example.com/book1'},
    {'title': 'El monje que vendió su Ferrari', 'author': 'Robin Sharma', 'cover': 'el_monje_que_vendio_su_ferrari.jpg', 'url': 'https://example.com/book1'},
]

for book_data in books_data:
    try:
        # Encuentra el libro en la base de datos
        book = Book.objects.get(title=book_data['title'], author=book_data['author'])
        
        # Crea la ruta completa al archivo de la imagen
        cover_path = os.path.join(covers_folder, book_data['cover'])
        
        # Abre el archivo de imagen y actualiza el campo cover_image del libro
        with open(cover_path, 'rb') as f:
            book.cover_image.save(book_data['cover'], File(f), save=True)
        
        # Actualiza el campo book_url
        book.book_url = book_data['url']
        book.save()
        
        print(f"Actualizado: {book.title}")
    except Book.DoesNotExist:
        print(f"No encontrado: {book_data['title']} por {book_data['author']}")

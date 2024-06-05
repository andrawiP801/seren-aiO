import os
import django

# Configura Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SerenAI.settings')
django.setup()

from chatai.models import Book

# Define la carpeta donde están tus imágenes en la carpeta static
covers_folder = 'static/book_covers/'

# Lista de libros y sus respectivas portadas y URLs
books_data = [
    {'title': 'La inteligencia emocional', 'author': 'Daniel Goleman', 'cover': 'la_inteligencia_emocional.jpg', 'url': 'http://www.cutonala.udg.mx/sites/default/files/adjuntos/inteligencia_emocional_daniel_goleman.pdf'},

    {'title': 'El poder del ahora', 'author': 'Eckhart Tolle', 'cover': 'el_poder_del_ahora.jpg', 'url': 'https://seduc.edomex.gob.mx/sites/seduc.edomex.gob.mx/files/files/padres_familia/fomento-lectura/Tolle_Eckhart-El_Poder_del_Ahora%20(1).pdf'},

    {'title': 'Mujeres que corren con los lobos', 'author': 'Clarissa Pinkola Estés', 'cover': 'mujeres_que_corren_con_los_lobos.jpg', 'url': 'https://www.legisver.gob.mx/equidadNotas/publicacionLXIII/Mujeres%20que%20corren%20con%20los%20lobos%20(1998).pdf'},

    {'title': 'El camino del artista', 'author': 'Julia Cameron', 'cover': 'el_camino_del_artista.jpg', 'url': 'https://everythingisvital.files.wordpress.com/2014/12/el-camino-del-artista-julia-cameron.pdf'},

    {'title': 'Las cuatro revelaciones', 'author': 'Alberto Villoldo', 'cover': 'las_cuatro_revelaciones.jpg', 'url': 'https://es.scribd.com/doc/242128459/105545341-Las-Cuatro-Revelaciones-Alberto-Villoldo-pdf'},
    
    {'title': 'El monje que vendió su Ferrari', 'author': 'Robin Sharma', 'cover': 'el_monge_que_vendio_su_ferrari.jpg', 'url': 'https://paulpalacios.mx/eBooks/pdf/Robin%20Sharma%20-%20El%20Monje%20que%20Vendi%C3%B3%20su%20Ferrari.pdf'},
]

for book_data in books_data:
    try:
        # Encuentra el libro en la base de datos
        book = Book.objects.get(title=book_data['title'], author=book_data['author'])
        
        # Almacena solo el nombre del archivo en cover_image
        book.cover_image = book_data['cover']
        
        # Actualiza el campo book_url
        book.book_url = book_data['url']
        book.save()
        
        print(f"Actualizado: {book.title}")
    except Book.DoesNotExist:
        print(f"No encontrado: {book_data['title']} por {book_data['author']}")

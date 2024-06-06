# views.py
import random
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from langchain_core.messages import HumanMessage, AIMessage

from .ai_model import get_chat
from .models import User, Chat, Book, ChatMessage, EmotionLog, Message, FAQ
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.utils import timezone
from .forms import ChatMessageForm, MessageForm
import json



# Create your views here.
def home_page(request):
    if request.user.is_authenticated:
        return redirect('main')
    return render(request, 'index.html')


def signup_page(request):
    error_message = None
    
    if request.user.is_authenticated:
        return redirect('main')

    if request.method == 'POST':
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        date_of_birth = request.POST.get('date_of_birth')
        gender = request.POST.get('gender')

        if User.objects.filter(username=username).exists():
            error_message = "Nickname already exists. Please choose a different nickname."
            return render(request, 'signup.html', {'error_message': error_message})

        if password == password2:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                name=name,
                surname=surname,
            )

            user.date_of_birth = date_of_birth
            user.gender = gender
            user.save()

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('main')
            else:
                error_message = "No User Found !"
        else:
            error_message = "Passwords doesn't match"

    return render(request, 'signup.html', {'error_message': error_message})


def login_page(request):
    
    if request.user.is_authenticated:
        return redirect('main')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('main')
        else:
            error_message = "Invalid Nickname or Password."
            return render(request, 'login.html', {'error_message': error_message})

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def main_page(request):
    motivational_phrases = [
        "El único límite para alcanzar tus sueños eres tú mismo.",
        "La vida es 10% lo que te sucede y 90% cómo reaccionas ante ello.",
        "Nunca es demasiado tarde para ser lo que podrías haber sido.",
        "El éxito no es la clave de la felicidad. La felicidad es la clave del éxito.",
        "Cree en ti mismo y todo será posible.",
        "No esperes el momento perfecto, toma el momento y hazlo perfecto.",
        "La única forma de hacer un gran trabajo es amar lo que haces.",
        "No te rindas, cada fracaso es una lección.",
        "El futuro pertenece a quienes creen en la belleza de sus sueños.",
        "La mayor gloria no es nunca caer, sino levantarse siempre.",
        "La perseverancia es la clave para el éxito.",
        "Haz de cada día tu obra maestra.",
        "El éxito es la suma de pequeños esfuerzos repetidos día tras día.",
        "El dolor que sientes hoy será la fuerza que sentirás mañana.",
        "No se trata de ser el mejor, se trata de ser mejor de lo que eras ayer.",
        "La única diferencia entre un buen día y un mal día es tu actitud.",
        "Si puedes soñarlo, puedes hacerlo.",
        "El camino al éxito y el camino al fracaso son casi exactamente el mismo.",
        "No cuentes los días, haz que los días cuenten.",
        "La fuerza no proviene de la capacidad física, sino de una voluntad indomable."
    ]
    selected_phrase = random.choice(motivational_phrases)
    
    context = {
        'motivational_phrase': selected_phrase
    }
    
    return render(request, 'main-page.html', context)


@login_required
def chat_page(request):
    messages = Chat.objects.filter(user=request.user)
    return render(request, 'chat-page.html', {'messages': messages})

@login_required
@csrf_exempt
def chat_query(request):
    query = request.POST.get('query')
    messages = Chat.objects.filter(user=request.user).order_by('id')
    history = []
    for message in messages:
        history.append(HumanMessage(
                content=message.user_message
            )
        )
        history.append(
            AIMessage(content=message.ai_message)
        )
    response = get_chat(query, request.user.id, history)
    Chat.objects.create(user=request.user, user_message=query, ai_message=response.content)
    return JsonResponse({"messages": response.content}, status=200)


@login_required
def profile_page(request):
    if request.method == 'POST':
        request.user.name = request.POST.get('name')
        request.user.surname = request.POST.get('surname')
        date_of_birth_str = request.POST.get('date_of_birth')
        if date_of_birth_str:
            request.user.date_of_birth = datetime.strptime(date_of_birth_str, '%Y-%m-%d').date()
        request.user.gender = request.POST.get('gender')
        request.user.username = request.POST.get('username')
        request.user.email = request.POST.get('email')
        password = request.POST.get('password')
        if password:
            request.user.set_password(password)
        request.user.save()
        return redirect('profile')
    
    user_date_of_birth = request.user.date_of_birth.strftime('%Y-%m-%d') if request.user.date_of_birth else ''
    context = {
        'user': request.user,
        'user_date_of_birth': user_date_of_birth,
    }
    return render(request, 'profile.html', context)

def books_page(request):
    books = Book.objects.all()
    return render(request, 'books.html', {'books': books})

def book_detail(request, book_id):
    book = Book.objects.get(id=book_id)
    return render(request, 'book_detail.html', {'book': book})

@login_required
def foro_page(request):
    if request.method == 'POST':
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            chat_message = form.save(commit=False)
            chat_message.user = request.user
            chat_message.save()
            return redirect('foro')
    else:
        form = ChatMessageForm()
    
    messages = ChatMessage.objects.all().order_by('timestamp')
    return render(request, 'general-chat.html', {'form': form, 'messages': messages})

@login_required
def emotional_state(request):
    activities = {
        "Respiración profunda": "1. Encuentra un lugar cómodo para sentarte.\n2. Cierra los ojos y respira profundamente por la nariz.\n3. Exhala lentamente por la boca.\n4. Repite este proceso por 5 minutos.",
        "Meditación guiada": "1. Encuentra un lugar tranquilo.\n2. Siéntate en una posición cómoda.\n3. Sigue una meditación guiada en una aplicación o video.\n4. Concéntrate en tu respiración.",
        "Ejercicio ligero": "1. Realiza una caminata de 10 minutos.\n2. Haz estiramientos suaves.\n3. Realiza movimientos de yoga simples.",
        "Escuchar música relajante": "1. Encuentra una lista de reproducción de música relajante.\n2. Siéntate en un lugar cómodo.\n3. Cierra los ojos y concéntrate en la música.",
        "Leer un libro": "1. Escoge un libro que te guste.\n2. Encuentra un lugar tranquilo para leer.\n3. Dedica al menos 15 minutos a la lectura.",
        "Tomar un baño caliente": "1. Llena la bañera con agua caliente.\n2. Añade sales de baño o aceites esenciales.\n3. Relájate en el agua durante 20 minutos.",
        "Dibujar o pintar": "1. Prepara tus materiales de dibujo o pintura.\n2. Encuentra un lugar tranquilo.\n3. Deja que tu creatividad fluya durante al menos 30 minutos.",
        "Escribir un diario": "1. Encuentra un lugar tranquilo.\n2. Abre tu diario o un cuaderno.\n3. Escribe tus pensamientos y sentimientos durante 15 minutos.",
        "Practicar yoga": "1. Despliega tu esterilla de yoga.\n2. Realiza una serie de posturas suaves.\n3. Concéntrate en tu respiración y en estirarte.",
        "Salir a caminar": "1. Ponte ropa y calzado cómodo.\n2. Sal a caminar por un parque o tu vecindario.\n3. Disfruta del aire libre durante al menos 20 minutos.",
        "Jugar con una mascota": "1. Dedica tiempo a jugar con tu mascota.\n2. Utiliza juguetes o simplemente acaríciala.\n3. Disfruta del momento.",
        "Ver una película": "1. Elige una película que te guste.\n2. Prepara unas palomitas o tu snack favorito.\n3. Relájate y disfruta de la película.",
        "Hacer jardinería": "1. Encuentra un espacio en tu jardín o balcón.\n2. Planta algunas flores o cuida tus plantas.\n3. Dedica al menos 30 minutos.",
        "Cocinar una receta nueva": "1. Elige una receta que te interese.\n2. Reúne los ingredientes necesarios.\n3. Cocina y disfruta del proceso.",
        "Hacer una sesión de estiramientos": "1. Encuentra un espacio cómodo.\n2. Realiza una serie de estiramientos suaves.\n3. Concéntrate en relajar tus músculos.",
    }
    
    selected_activity, activity_details = random.choice(list(activities.items()))
    
    context = {
        'activity': selected_activity,
        'details': activity_details,
    }
    
    return render(request, 'emotional_state.html', context)

@login_required
def save_emotion(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        emotion = data.get('emotion')
        user = request.user
        today = timezone.now().date()

        # Contar emociones guardadas hoy
        emotions_today = EmotionLog.objects.filter(user=user, date__date=today).count()

        if emotions_today >= 3:
            return JsonResponse({'success': False, 'error': 'Has alcanzado el límite de 3 emociones por día.'})
        
        EmotionLog.objects.create(user=user, emotion=emotion, date=timezone.now())
        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)

@login_required
def emotion_log(request):
    user = request.user
    emotions = EmotionLog.objects.filter(user=user).order_by('-date')

    emotion_data = [
        {'date': emotion.date.strftime('%Y-%m-%d %H:%M:%S'), 'emotion': emotion.emotion}
        for emotion in emotions
    ]

    return JsonResponse({'emotions': emotion_data})

@login_required
def servicio_page(request):
    if request.user.is_superuser:
        messages = Message.objects.all()
        return render(request, 'superuser-servicio.html', {'messages': messages})
    else:
        faqs = FAQ.objects.all()
        return render(request, 'user-servicio.html', {'faqs': faqs})

@login_required
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.user = request.user
            message.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'fail', 'errors': form.errors})
    return JsonResponse({'status': 'fail', 'error': 'Invalid request'})

@login_required
def fetch_messages(request):
    messages = Message.objects.all()
    messages_data = [{'user': message.user.username, 'text': message.text, 'timestamp': message.timestamp} for message in messages]
    return JsonResponse(messages_data, safe=False)
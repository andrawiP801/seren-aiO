# views.py
import random
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from langchain_core.messages import HumanMessage, AIMessage

from .ai_model import get_chat
from .models import User, Chat, Book, ChatMessage
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .forms import ChatMessageForm


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
    books = Book.objects.all()  # Asumiendo que tienes un modelo de Book
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
    return render(request, 'emotional_state.html')
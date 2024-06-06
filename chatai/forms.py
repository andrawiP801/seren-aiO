from django import forms
from .models import ChatMessage, Message


class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['message']

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text']
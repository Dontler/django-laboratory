from django import forms
from .models import Post

class SearchForm(forms.Form):
    query = forms.CharField(label="Введите название для поиска",
        widget=forms.TextInput(
            attrs={'class': 'search_input'}
        )
    )
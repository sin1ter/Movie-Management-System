from django import forms
from .models import Movie

class MovieForm(forms.ModelForm):
    hours = forms.IntegerField(required=False, min_value=0, label='Hours', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Hours'}))
    minutes = forms.IntegerField(required=False, min_value=0, max_value=59, label='Minutes', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Minutes'}))
    seconds = forms.IntegerField(required=False, min_value=0, max_value=59, label='Seconds', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Seconds'}))
    

    class Meta:
        model = Movie
        fields = ['title', 'description', 'released_at', 'hours', 'minutes', 'seconds', 'genre', 'language', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['released_at'].widget.attrs.update({'class': 'form-control datepicker'})  # Add datepicker class
        self.fields['genre'].widget.attrs.update({'class': 'form-control'})
        self.fields['language'].widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        movie = super().save(commit=False)
        # Set the duration based on the input fields
        movie.duration_hours = self.cleaned_data['hours'] or 0
        movie.duration_minutes = self.cleaned_data['minutes'] or 0
        movie.duration_seconds = self.cleaned_data['seconds'] or 0
        
        if commit:
            movie.save()
        return movie
    
class RatingForm(forms.Form):
    rating = forms.FloatField(
        required=True,  
        min_value=1,
        max_value=5,
        label='Rating',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Rating'})
    )

class ReportForm(forms.Form):
    reason = forms.CharField(max_length=256, label='Reason for Reporting', widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your reason here...'}))

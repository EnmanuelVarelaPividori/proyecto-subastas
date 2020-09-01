from django import forms
from .models import Auction, Comments, Bid
from django.core.exceptions import ValidationError

class Lcreate(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ('name', 'img', 'description', 'category', 'starting_bid')
        
        widgets = {
            'description' : forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '5',
                'cols': '90',
                'maxlength': '500',
            }),
            'name' : forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '1',
                'cols': '100',
                'maxlength': '30',
            }),
            'category' : forms.Select(attrs={
                'class': 'form-control'
            }),
            'starting_bid' : forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('body',)      


class PlaceNewBid(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ('new_bid',) 

from django import forms
from django.contrib.auth.models import User
from .models import ScheduledBattlefield, BattlefieldCompletion


class FCSignUpForm(forms.ModelForm):
    class Meta:
        model = ScheduledBattlefield
        fields = ['fc']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fc'].queryset = User.objects.all()  # Optionally, filter for specific users if needed

class ParticipantSignUpForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput())  # Hidden field for the current user

class BattlefieldCompletionForm(forms.ModelForm):
    class Meta:
        model = BattlefieldCompletion
        fields = ['solar_system', 'winner', 'defender', 'completion_time']  # Add the fields relevant to your model

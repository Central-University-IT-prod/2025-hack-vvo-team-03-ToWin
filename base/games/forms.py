from django import forms
from . import models


class CreateCompetitionForm(forms.ModelForm):
    time = forms.TimeField()
    time.label = 'Время'
    time.widget = forms.TimeInput(attrs={"type": "time"})
    class Meta:
        model = models.Competition
        fields = ('name', 'command', 'datetime', 'time', 'place', 'description', 'type_game', 'count_player_max')
        labels = {
            'name': 'Название',
            'command': 'Для команд',
            'datetime': 'Дата',
            'time': 'Время',
            'place': 'Место проведения',
            'description': 'Описание',
            'type_game': 'Вид спорта',
            'count_player_max': 'Макс. кол-во участников'
        }
        widgets = {
            'datetime': forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        }

    
    def __init__(self, *args, **kwargs):
        super(CreateCompetitionForm, self).__init__(*args, **kwargs)
   
        self.fields['description'].required = False
        self.fields['type_game'].required = False
       
        
class EditGameForm(forms.ModelForm):
    time = forms.TimeField()
    time.label = 'Время'
    time.widget = forms.TimeInput(attrs={"type": "time"})
    class Meta:
        model = models.Game
        fields = ('count1', 'count2', 'datetime', 'time', 'place')
        labels = {
            'datetime': 'Дата',
            'time': 'Время',
            'place': 'Место'
        }

    def __init__(self, *args, **kwargs):
        super(CreateCompetitionForm, self).__init__(*args, **kwargs)

        self.fields['count1'].required = False
        self.fields['count2'].required = False
        self.fields['place'].required = False
        self.fields['dtateime'].required = False
        self.fields['time'].required = False
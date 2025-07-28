from django import forms
from .models import Project, Event, EventPhoto

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'title', 'description', 'background', 'status', 'relevance',
            'goal', 'metrics', 'results', 'team',
            'audience', 'event_type', 'risks',
            'material_resources', 'non_material_resources'
        ]
        widgets = {
            'metrics': forms.HiddenInput(),
            'team': forms.HiddenInput(),
            'risks': forms.HiddenInput(),
        }

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['date', 'name']
        widgets = {
            'date': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control'
                },
                format='%Y-%m-%dT%H:%M'
            ),
            'name': forms.TextInput(attrs={'placeholder': 'Место проведения'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.date:
            self.initial['date'] = self.instance.date.strftime('%Y-%m-%dT%H:%M')

class EventMetricsForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['actual_metrics']
        widgets = {
            'actual_metrics': forms.HiddenInput(),
        }

class EventHeaderForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['date', 'name']
        widgets = {
            'date': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control'
                },
                format='%Y-%m-%dT%H:%M'
            ),
            'name': forms.TextInput(attrs={'placeholder': 'Место проведения'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.date:
            self.initial['date'] = self.instance.date.strftime('%Y-%m-%dT%H:%M')


class EventPhotoForm(forms.ModelForm):
    class Meta:
        model = EventPhoto
        fields = ['image']

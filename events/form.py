from django import forms
from .models import Event, Participant, Category
from django.contrib.auth.models import Group,Permission

# Form Mixin for Styling
class FormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widget()

    default_classes = "border-2 border-black w-full p-3 rounded-lg shadow-sm focus:outline-none "

    def apply_styled_widget(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': f"{self.default_classes} ",
                    'placeholder': f"Enter {field.label.lower()}",
                    'rows': 5
                })
            elif isinstance(field.widget, forms.SelectDateWidget):
                field.widget.attrs.update({
                    "class": "border-2 border-gray-300 p-3 rounded-lg shadow-sm focus:outline-none mr-2 mt-2"
                })
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class': "space-y-2 mt-2"
                })
            else:
                field.widget.attrs.update({
                    'class': self.default_classes
                })


# Event Form
class EventModelForm(FormMixin, forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Select a category",
        widget=forms.Select(attrs={'class': 'border-2 border-gray-300 p-3 rounded-lg shadow-sm focus:outline-none '})
    )

    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'time', 'location', 'category']
        widgets = {
            'date': forms.SelectDateWidget,
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'description': forms.Textarea(attrs={'rows': 5}),
        }


# Participant Form
class ParticipantModelForm(FormMixin, forms.ModelForm):
    participants = forms.ModelMultipleChoiceField(
        queryset=Participant.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'space-y-2 mt-2'})
    )

    class Meta:
        model = Event
        fields = ['participants']
        
class ParticipantForm(FormMixin, forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['name', 'email']  # Fields for creating a new participant


# Category Form
class CategoryModelForm(FormMixin, forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }
        
class AssignRoleForm(FormMixin, forms.Form):
    role = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        empty_label="Select a Role"
    ) 
    
class CreateGroupForm(FormMixin, forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Assign Permission'
    )

    class Meta:
        model = Group
        fields = ['name', 'permissions']
from django import forms
from .models import Story, Description, Category
from django.contrib.auth.models import User


class StoryForm(forms.ModelForm):
    new_category = forms.CharField(required=False, max_length=30)

    class Meta:
        model = Story
        fields = ['name', 'categories']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'story-title placeholder-centered', 'placeholder': 'Add story title'}),
            'categories': forms.CheckboxSelectMultiple(),
        }
        labels = {
            'name': '',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make 'categories' field optional
        self.fields['categories'].required = False
        # Add attributes for 'new_category' field
        self.fields['new_category'].widget.attrs.update({
            'class': 'minimal-textarea placeholder-centered fs-4',
            'placeholder': 'Custom category here'
        })

    def save(self, commit=True):
        # Call the parent save method to create the story object
        story = super().save(commit=False)
        new_category_name = self.cleaned_data.get('new_category')

        if commit:
            story.save()
            # Handle the new category if provided
            if new_category_name:
                category, created = Category.objects.get_or_create(name=new_category_name)
                story.categories.add(category)
                self.save_m2m()
        return story


class DescriptionForm(forms.ModelForm):
    class Meta:
        model = Description
        fields = ('description_text',)
        widgets = {
            'description_text': forms.Textarea(
                attrs={'class': 'minimal-textarea story-container placeholder-centered',
                       'id': 'description_text_input',
                       'placeholder': 'Continue story here'})
        }
        labels = {
            'description_text': '',
        }

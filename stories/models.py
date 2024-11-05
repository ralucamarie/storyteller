from django.conf import settings
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Story(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, related_name='stories')
    created_at = models.DateTimeField(auto_now_add=True)  # Add this field

    def __str__(self):
        return self.name


class Description(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='descriptions')
    description_text = models.TextField()
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)  # Add this field

    def __str__(self):
        return f'Description for {self.story.name} by {self.added_by.username}'


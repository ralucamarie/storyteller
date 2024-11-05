import json

from django.db.models import Prefetch
from django.shortcuts import render, redirect
from .forms import StoryForm, DescriptionForm
from .models import Story, Description, Category
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required


def stories(request):
    search_by = request.GET.get('search_by')
    search_text = request.GET.get('search_text')
    if search_by and search_text:
        match search_by:
            case 'owner':
                db_stories = Story.objects.select_related('owner').prefetch_related(
                    'categories',
                    'descriptions__added_by'
                ).filter(owner__username__icontains=search_text).order_by('-created_at')
            case 'description':
                db_stories = Story.objects.select_related('owner').prefetch_related(
                    'categories',
                    'descriptions__added_by'
                ).filter(descriptions__description_text__icontains=search_text).order_by('-created_at')
            case 'category':
                db_stories = Story.objects.select_related('owner').prefetch_related(
                    'categories', 'descriptions__added_by'
                ).filter(categories__name__icontains=search_text).order_by('-created_at')
                # For multiple categories:
                # category_list = search_text.split(',')  # Split search text by commas to get list of categories
                # db_stories = Story.objects.select_related('owner').prefetch_related(
                #     'categories', 'descriptions__added_by'
                # ).filter(categories__name__in=category_list).distinct().order_by('-id')
            case _:
                db_stories = Story.objects.select_related('owner').prefetch_related(
                    'categories',
                    Prefetch('descriptions', queryset=Description.objects.select_related('added_by').order_by('created_at'))
                ).order_by('-created_at')
    else:
        db_stories = Story.objects.select_related('owner').prefetch_related(
            'categories',
            Prefetch('descriptions', queryset=Description.objects.select_related('added_by').order_by('created_at'))
        ).order_by('-created_at')
    total_stories = db_stories.count()
    return render(request, 'stories/stories.html', {
        'stories': db_stories,
        'total_stories': total_stories,
        'search_by': search_by,
        'search_text': search_text
    })


@login_required(login_url="/users/login")
def add_story_view(request):
    if request.method == 'POST':
        story_form = StoryForm(request.POST)
        description_form = DescriptionForm(request.POST)
        if story_form.is_valid() and description_form.is_valid():
            story = story_form.save(commit=False)
            story.owner = request.user
            story.save()

            for category in story_form.cleaned_data['categories']:
                print(category)
                story.categories.add(category)

            new_category_name = story_form.cleaned_data.get('new_category')
            if new_category_name:
                print(story_form.cleaned_data['new_category'])
                category, created = Category.objects.get_or_create(name=story_form.cleaned_data['new_category'])
                print(category, created)
                print(created)
                story.categories.add(category)

            description = description_form.save(commit=False)
            description.story = story
            description.added_by = request.user
            description.save()

            return redirect('stories:view_story', story_id=story.id)
    else:
        story_form = StoryForm()
        description_form = DescriptionForm()

    return render(request, 'stories/add_story.html', {'story_form': story_form, 'description_form': description_form})


def view_story(request, story_id):
    # story = Story.objects.select_related('owner').prefetch_related(
    #     'categories', 'descriptions__added_by'
    # ).get(id=story_id)
    story = get_object_or_404(Story, id=story_id)
    descriptions = story.descriptions.all().order_by('created_at')
    categories = story.categories.all()
    if request.method == 'POST':
        form = DescriptionForm(request.POST)
        if form.is_valid():
            description = form.save(commit=False)
            description.story = story
            description.added_by = request.user
            description.save()
            return redirect('stories:view_story', story_id=story_id)
    else:
        form = DescriptionForm()

    return render(request, 'stories/view_story.html', {
        'story': story,
        'descriptions': descriptions,
        'categories': categories,
        'form': form
    })


# delete Story
def delete(request):
    return render(request, 'stories/stories.html')


def update(request):
    return render(request, 'stories/stories.html')


@login_required
def edit_description(request, story_id, description_id):
    story = get_object_or_404(Story, id=story_id)
    description = get_object_or_404(Description, id=description_id, story_id=story_id)

    if description.story != story:
        return redirect('stories:view_story', story_id=story_id)

    if request.method == 'POST' and request.user == description.added_by:
        new_text = request.POST.get('description_text')
        description.description_text = new_text
        description.save()
        return redirect('stories:view_story', story_id=story_id)
    return redirect('stories:view_story', story_id=story_id)


def delete_description(request, story_id, description_id):
    description = get_object_or_404(Description, id=description_id)
    if description:
        description.delete()
        return redirect('stories:view_story', story_id=story_id)
    return redirect('stories:view_story', story_id=story_id)

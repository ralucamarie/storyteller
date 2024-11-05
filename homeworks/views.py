# from django.http import HttpResponse
from django.shortcuts import render, redirect


def homepage(request):
    return redirect('stories:stories')


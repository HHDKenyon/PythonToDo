from typing import Any
from django.db import models
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import List, Item

class IndexView(generic.ListView):
	template_name = "todoapp/index.html"
	context_object_name = "latest_list"

	def get_queryset(self):
		return List.objects.order_by("-created_date")[:5]
	
class DetailView(generic.DetailView):
	model = List
	template_name = "todoapp/detail.html"

class ResultsView(generic.DetailView):
	model = List
	template_name = "todoapp/results.html"
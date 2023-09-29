from django.urls import path

from . import views

app_name = "todoapp"
urlpatterns = [
    # eg: /todoapp/
    path("", views.IndexView.as_view(), name="index"),
	# eg: /todoapp/5/
	path("<int:pk>/", views.DetailView.as_view(), name="detail"),
]
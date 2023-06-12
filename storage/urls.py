from django.urls import path, include
from .views import userAPI,roomAPI

urlpatterns = [
    path("user/<str:id>",userAPI),
    path("room/<int:id>",roomAPI),
]
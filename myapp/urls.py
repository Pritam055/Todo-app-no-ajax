from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views

app_name = "todo"

urlpatterns = [
    path('', views.TodoListView.as_view(), name='todoList'),
    path('add/', views.AddTodo.as_view(), name='addTodo'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='todo:login'), name='logout'),
    path('delete/<int:pk>/', views.TodoDeleteView.as_view(), name='delete'),
    path('edit/<int:pk>/', views.TodoEditView.as_view(), name='edit'),
    path('detail/<int:pk>/', views.TodoDetailView.as_view(), name='detail'),
]
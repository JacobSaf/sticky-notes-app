from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.note_list, name='note_list'),
    path('add/', views.add_note, name='add_note'),
    path('edit/<int:note_id>/', views.edit_note, name='edit_note'),
    path('delete/<int:note_id>/', views.delete_note, name='delete_note'),
    path('accounts/', include('django.contrib.auth.urls')),  # 👈 This line fixes the 404
]
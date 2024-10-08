from django.urls import path
from . import views

app_name = 'movies'
urlpatterns = [
    path('', views.movie_list, name='list'),
    path('<int:id>/',views.movie_detail, name= 'detail'),
    path('<int:id>/create-review/', views.movie_create_review, name='create-review'),
    path('<int:id>/edit-review/', views.movie_edit_review, name='edit-review'),
    path('<int:id>/delete-review/<int:review_id>/', views.movie_delete_review, name='delete-review'),
    #path('<slug:slug>/',views.movie_detail, name= 'detail'),
]

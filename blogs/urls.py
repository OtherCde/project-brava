from django.urls import path
from .views import *

urlpatterns = [
    # Ruta para devolver todos los posteos realizados por los usuarios
    path(
        "", 
        PostListView.as_view(), 
        name="post-list"
    ),
    # Ruta que me permite crear un blog
    path(
        "create/",
        CreatePostView.as_view(),
        name="post-create"
    ),
    # Ruta para crear un 'Me gusta'
    path(
        '<int:post_id>/like/', 
        ToggleLikeView.as_view(), 
        name='toggle_like'
    ),
    # Ruta para crear un 'Comentario en una publicacion'
    path(
        '<int:post_id>/comments/', 
        CommentView.as_view(), 
        name='comments'
    ),
]
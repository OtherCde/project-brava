from django.shortcuts import render

from rest_framework import generics, permissions
from .models import Post, Like, Comment
from .serializers import PostSerializer, LikeSerializer, CommentSerializer
# Para las vista de dar like
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils.timezone import now
from django.shortcuts import get_object_or_404

# Create your views here.

##########################################################################################################
####################################### VIEW PARA POSTEOS ###############################################
##########################################################################################################


class PostListView(generics.ListAPIView):
    queryset = Post.objects.filter(deleted_at=None)
    serializer_class = PostSerializer
    permission_classes = [AllowAny]  # Permite acceso a cualquiera

    def get_serializer_context(self):
        context = super().get_serializer_context()
        print(f"🔍 Usuario en la vista: {self.request.user}")  # <-- Verifica aquí
        context["request"] = self.request
        return context

class CreatePostView(generics.CreateAPIView):
    """Vista para crear un nuevo post."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]  # Solo usuarios autenticados pueden crear posts

    def perform_create(self, serializer):
        """Asigna el usuario autenticado como el autor del post."""
        serializer.save(author=self.request.user)


##########################################################################################################
####################################### VIEW PARA LIKES ###############################################
##########################################################################################################

class ToggleLikeView(APIView):
    """Vista para dar o quitar like a un post."""
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        user = request.user
        post = get_object_or_404(Post, id=post_id)

        # Intentar obtener el like del usuario para este post
        like = Like.all_objects.filter(user=user, post=post).first()
        
        if like:
            if like.deleted_at:
                # Si el like está "eliminado", restaurarlo
                like.deleted_at = None
                like.save()
                message = "Like restaurado"
            else:
                # Si el like está activo, marcarlo como eliminado
                like.deleted_at = now()
                like.save()
                message = "Like eliminado"
        else:
            # Si no existe, crearlo
            like = Like.objects.create(user=user, post=post)
            message = "Like agregado"

        # Contar los likes activos
        likes_count = Like.objects.filter(post=post, deleted_at__isnull=True).count()
        liked = Like.objects.filter(post=post, user=user, deleted_at__isnull=True).exists()

        return Response(
            {
                "message": message,
                "like_id": like.id,
                "likes_count": likes_count,
                "liked": liked,
            },
            status=status.HTTP_200_OK,
        )
    
##################################################################################################
################################ VIEW DE COMENTARIOS #############################################
##################################################################################################


class CommentView(APIView):
    """Vista para listar y crear comentarios en un post."""
    permission_classes = [IsAuthenticated]

    def get(self, request, post_id):
        """Lista los comentarios de un post."""
        post = get_object_or_404(Post, id=post_id)
        comments = Comment.objects.filter(post=post).order_by("-created_at")  # Comentarios más recientes primero
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, post_id):
        """Crea un comentario en una publicación."""
        post = get_object_or_404(Post, id=post_id)
        print("📥 Datos recibidos:", request.data)  

        serializer = CommentSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(user=request.user, post=post)  # 🔥 Asignamos el post aquí
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        print("❌ Error en el serializer:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
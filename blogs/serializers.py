from rest_framework import serializers
from .models import Post, Like, Comment

class PostSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Post."""
    author = serializers.SerializerMethodField()
    likes_count = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()

    class Meta:
        model = Post
        fields = [
            "id", 
            "author", 
            "title", 
            "content", 
            "image", 
            "created_at",
            'likes_count',
            'comments_count'
        ]
        read_only_fields = ['author']

    def get_author(self, obj):
        """Obtenemos el autor"""
        return {
            "name": obj.author.get_full_name(),
            "avatar": obj.author.profile_image.url if obj.author.profile_image else None,
        }
    
    def create(self, validated_data):
        """Asigna el usuario autenticado como autor al crear un post."""
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            validated_data["author"] = request.user
        return super().create(validated_data)
    
class LikeSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Like."""
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at']
        read_only_fields = ['user']

class CommentSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Comment."""
    user = serializers.SerializerMethodField()  # 🔥 Personalizamos la salida del usuario
    # post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())  # Permite recibir solo el ID del post
    post = serializers.PrimaryKeyRelatedField(read_only=True)  # 🔥 Hacer post solo lectura

    class Meta:
        model = Comment
        fields = ['id', 'user', 'post', 'content', 'created_at']
        read_only_fields = ['user', 'created_at']

    def get_user(self, obj):
        """Devuelve un diccionario con el nombre y avatar del usuario."""
        return {
            "name": obj.user.get_full_name(),
            "avatar": obj.user.profile_image.url if obj.user.profile_image else None  # 🔥 Obtiene la URL de la imagen
        }
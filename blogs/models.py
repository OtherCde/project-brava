
# Create your models here.
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from core.models import BaseAbstractWithUser

class Post(BaseAbstractWithUser):
    """Modelo que representa una publicación en la radio."""
    author = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=255, verbose_name=_("Título"))
    content = models.TextField(verbose_name=_("Contenido"))
    image = models.ImageField(upload_to="post_images/", null=True, blank=True, verbose_name=_("Imagen"))

    class Meta:
        verbose_name = _("Publicación")
        verbose_name_plural = _("Publicaciones")
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def likes_count(self):
        return self.likes.count()

    def comments_count(self):
        return self.comments.count()
    

class Like(BaseAbstractWithUser):
    """Modelo que representa un 'Me gusta' en una publicación."""
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")

    class Meta:
        unique_together = ('user', 'post')
        verbose_name = _("Like")
        verbose_name_plural = _("Likes")

    def __str__(self):
        return f"{self.user} le gustó '{self.post.title}'."
    

class Comment(BaseAbstractWithUser):
    """Modelo que representa un comentario en una publicación."""
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField(verbose_name=_("Comentario"))

    class Meta:
        verbose_name = _("Comentario")
        verbose_name_plural = _("Comentarios")
        ordering = ["-created_at"]

    def __str__(self):
        return f"Comentario de {self.user} en '{self.post.title}'."

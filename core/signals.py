# apps/core/signals.py
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
 # Asegúrate de importar tu modelo de usuario si tienes uno personalizado.

@receiver(post_migrate)
def create_groups(sender, **kwargs):
    # Definir los grupos y sus permisos
    groups_permissions = {
        'Oyentes': [
            'add_emailaddress', 'change_emailaddress', 'delete_emailaddress', 'view_emailaddress',
            'add_emailconfirmation', 'change_emailconfirmation', 'delete_emailconfirmation', 'view_emailconfirmation',
            'add_comment', 'change_comment', 'delete_comment', 'view_comment',
            'add_like', 'change_like', 'delete_like', 'view_like',
            'view_program', 'add_socialaccount', 'change_socialaccount', 'delete_socialaccount', 'view_socialaccount',
            'add_socialapp', 'change_socialapp', 'delete_socialapp', 'view_socialapp',
            'add_socialtoken', 'change_socialtoken', 'delete_socialtoken', 'view_socialtoken',
            'view_user'
        ],
        'Periodistas': [
            'add_emailaddress', 'change_emailaddress', 'delete_emailaddress', 'view_emailaddress',
            'add_emailconfirmation', 'change_emailconfirmation', 'delete_emailconfirmation', 'view_emailconfirmation',
            'add_comment', 'change_comment', 'delete_comment', 'view_comment',
            'add_like', 'change_like', 'delete_like', 'view_like',
            'add_post', 'change_post', 'delete_post', 'view_post',
            'view_program', 'add_session', 'change_session', 'delete_session', 'view_session',
            'add_user', 'change_user', 'delete_user', 'view_user'
        ],
        'Conductores': [
            'add_emailaddress', 'change_emailaddress', 'delete_emailaddress', 'view_emailaddress',
            'add_emailconfirmation', 'change_emailconfirmation', 'delete_emailconfirmation', 'view_emailconfirmation',
            'add_logentry', 'change_logentry', 'delete_logentry', 'view_logentry',
            'add_comment', 'change_comment', 'delete_comment', 'view_comment',
            'add_like', 'change_like', 'delete_like', 'view_like',
            'add_post', 'change_post', 'delete_post', 'view_post',
            'add_program', 'change_program', 'delete_program', 'view_program',
            'add_user', 'change_user', 'delete_user', 'view_user'
        ]
    }
    # Crear grupos y asignarles permisos
    for group_name, permissions_codename_list in groups_permissions.items():
        group, created = Group.objects.get_or_create(name=group_name)
        if created:
            permissions = Permission.objects.filter(codename__in=permissions_codename_list)
            group.permissions.set(permissions)

    print("Grupos y permisos creados correctamente.")
    # Crear el grupo 'Administradores' y asignarle permisos
    admin_group, created = Group.objects.get_or_create(name='Administradores')
    if created:
        permissions = Permission.objects.filter(codename__in=[
            'add_user', 'change_user', 'delete_user', 'view_user',
            'add_program', 'change_program', 'delete_program', 'view_program'
        ])
        admin_group.permissions.set(permissions)

    # Crear el grupo 'Usuarios' y asignarle permisos
    user_group, created = Group.objects.get_or_create(name='Usuarios')
    if created:
        permissions = Permission.objects.filter(codename__in=[
            'view_user', 'view_program'
        ])
        user_group.permissions.set(permissions)

    # Añadir otros grupos según sea necesario...

import sys
import os
import django

# Agregar la ruta de tu proyecto al sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()
from django.contrib.auth.models import Group, Permission

# Obtener todos los grupos y sus permisos
groups = Group.objects.all()

print("📌 Listado de grupos con sus permisos:\n")

for group in groups:
    print(f"🔹 Grupo: {group.name}")
    permissions = group.permissions.all()
    if permissions:
        for perm in permissions:
            print(f"    ✅ {perm.codename} ({perm.name})")
    else:
        print("    ⚠️ No tiene permisos asignados.")
    print("-" * 40)

# Obtener todos los permisos disponibles en el sistema
print("\n📌 Lista de todos los permisos disponibles:\n")

all_permissions = Permission.objects.all()
for perm in all_permissions:
    print(f"🔸 {perm.codename} ({perm.name}) - {perm.content_type.app_label}")

print("\n✅ Script ejecutado correctamente.")

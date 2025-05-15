# In your app's signals.py file
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from core.models import UserManager
from trivia.models import QuestionType

@receiver(post_migrate)
def add_initial_data(sender, **kwargs):
    if sender.name == 'core':
        UserManager.createSuperInstance()
        
@receiver(post_migrate)
def add_initial_data(sender, **kwargs):
    if sender.name == 'core':
        UserManager.createSuperInstance()

        tipos_iniciales = [
            ('multiple_selection', 'Selección múltiple'),
            ('single_selection',   'Selección única'),
        ]
        for name, description in tipos_iniciales:
            obj, creado = QuestionType.objects.get_or_create(
                name=name,
                defaults={'description': description}
            )
            if creado:
                print(f"Tipo de pregunta «{name}» creado.")
            else:
                print(f"Tipo de pregunta «{name}» ya existe.")
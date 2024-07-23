from django.apps import apps
from django.contrib import admin

# register all models in django
models = apps.get_models()
for model in models:
    try:
        admin.site.register(model)
    except Exception as e:
        pass

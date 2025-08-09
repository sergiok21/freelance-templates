from django import forms
from django.db import models


class SimpleUrlFieldAdmin:
    formfield_overrides = {
        models.URLField: {"widget": forms.TextInput()},
    }

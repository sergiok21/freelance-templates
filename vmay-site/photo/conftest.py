import logging

import pytest


logger = logging.getLogger(__name__)


@pytest.fixture(autouse=True)
def disable_file_save(monkeypatch):
    monkeypatch.setattr(
        "django.db.models.fields.files.FieldFile.save",
        lambda *args, **kwargs: None
    )

    monkeypatch.setattr(
        "django.db.models.fields.files.FieldFile.delete",
        lambda *args, **kwargs: None
    )

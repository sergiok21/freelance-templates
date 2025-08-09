class DeleteOldImageModelMixin:
    image_field_name = 'image'

    def save(self, *args, **kwargs):
        if self.pk:
            old = type(self).objects.filter(pk=self.pk).only(self.image_field_name).first()
            fn = getattr(old, self.image_field_name, None)
            if fn and fn != getattr(self, self.image_field_name):
                fn.delete(save=False)
        return super().save(*args, **kwargs)

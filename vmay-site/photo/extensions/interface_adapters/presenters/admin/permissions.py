class SingleValuePermission:
    def has_add_permission(self, request):
        return not self.model.objects.exists()

from django.utils.html import format_html


class ImagePreviewAdmin:
    def preview_image(self, obj):
        if obj.image:
            return format_html(
                '<a href="{0}" target="_blank"><img src="{0}" style="height: 50px; border-radius: 4px;" /></a>',
                obj.image.url)
        return "-"
    preview_image.short_description = 'Фото'

from django.db import models
from django.utils.safestring import mark_safe


class Slider(models.Model):
    image = models.FileField(blank=True)


class SliderImage(models.Model):
    slider = models.ForeignKey(Slider, default=None, on_delete=models.CASCADE)
    title = models.CharField(blank=True, null=True, max_length=250, default='')
    images = models.FileField(upload_to='')

    def __str__(self):
        return self.title

    def image_preview(self):
        if self.images:
            return mark_safe('<img src="{0}" width="150" height="150" />'.format(self.images.url))
        else:
            return '(No Image)'

from django.db import models
from django.utils.text import slugify

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50,blank=False,null=False,editable=True)
    slug = models.SlugField(unique=True, blank=True)
    def save(self, *args, **kwargs):
        if not self.slug or self.slug.strip() == '':
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while Category.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    

class Video(models.Model):
    video = models.FileField(upload_to='videos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.video.name


class Course(models.Model):
    title = models.CharField(max_length=50, blank=False, null=True, editable=True)
    slug = models.SlugField(default='', editable=False, blank=True, unique=True)
    description = models.TextField(blank=True, editable=True)
    images = models.ImageField(upload_to='images/')
    create_time = models.DateTimeField(auto_now=True, blank=True)
    isActive = models.BooleanField(editable=True, blank=False)
    categories = models.ManyToManyField(Category)
    
    # Yeni eklenen alan:
    videos = models.ManyToManyField(Video, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug or self.slug.strip() == '':
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1

            while Course.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from slugify import slugify
from parler.models import TranslatableModel, TranslatedFields

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.username

class BaseModel(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, 
        related_name="%(class)s_related"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Page(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(max_length=255, unique=False),
        title = models.CharField(max_length=255, null=True, blank=True),
        description = models.TextField(null=True, blank=True),
        slug = models.SlugField(unique=False, blank=True, null=True),
    )
    icon = models.ImageField(upload_to='static/icons/categories', null=True, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="categories"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Kateqoriya"
        verbose_name_plural = "Kateqoriyalar"
        ordering = ['order']

    def save(self, *args, **kwargs):
        if not self.slug and self.safe_translation_getter('name', any_language=True):
            self.slug = slugify(self.safe_translation_getter('name', any_language=True), allow_unicode=True, separator='-')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.safe_translation_getter('name', any_language=True) or "Unnamed Category"
    
class PageImage(models.Model):
    category = models.ForeignKey(
        Page, 
        on_delete=models.CASCADE, 
        related_name='images'
    )
    image = models.ImageField(upload_to='static/images/categories/')
    alt_text = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.category.name} şəkli"

class Subpage(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(max_length=255, unique=False),
        title = models.CharField(max_length=255, null=True, blank=True),
        description = models.TextField(null=True, blank=True),
        slug = models.SlugField(unique=False, blank=True, null=True),
        full_slug = models.SlugField(unique=False, blank=True, null=True),
    )
    icon = models.ImageField(upload_to='static/icons/subcategories', null=True, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    category = models.ForeignKey(
        Page,
        models.CASCADE,
        related_name="subcategories"
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="subcategories"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Alt Kateqoriya"
        verbose_name_plural = "Alt Kateqoriyalar"
        # unique_together = ('category', 'parent')
        ordering = ['order']

    def save(self, *args, **kwargs):
        if not self.slug and self.safe_translation_getter('name', any_language=True):
            self.slug = slugify(self.safe_translation_getter('name', any_language=True), allow_unicode=True, separator='-')
        
        self.full_slug = self.get_full_slug_path()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_full_path()}"
    
    def get_full_path(self):
        """ Rekursiv olaraq tam yol göstərir: Haqqımızda > Mediada Biz > Qalereya """
        if self.parent:
            return f"{self.parent.get_full_path()} > {self.name}"
        return self.name

    def get_full_slug_path(self):
        parts = []

        if self.parent:
            parts.append(self.parent.get_full_slug_path())
        
        elif self.category and self.category.slug:
            parts.append(self.category.slug)

        current_slug = self.slug or slugify(self.name, allow_unicode=True, separator='-')
        parts.append(current_slug)

        return "/".join(parts)


class SubcategoryImage(models.Model):
    subcategory = models.ForeignKey(
        Subpage,
        on_delete=models.CASCADE, 
        related_name='images'
    )
    image = models.ImageField(upload_to='static/images/subcategories/')
    alt_text = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.subcategory.name} şəkli"
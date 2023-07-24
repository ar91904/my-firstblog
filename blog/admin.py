from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'published_date')
    list_filter = ('status', 'created_date', 'published_date')
    date_hierarchy = ('published_date')
    ordering = ('status', 'published_date')
from django.contrib import admin
from lexandstuff.blog.models import *

class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug":("title",)}
    search_fields = ["title"]
    display_fields = ["title", "created"]

admin.site.register(Post, PostAdmin)
admin.site.register(Tag)



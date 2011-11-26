from django.contrib import admin
from lexandstuff.blog.models import *

class PostAdmin(admin.ModelAdmin):
	search_fields = ["title"]
	display_fields = ["title", "created"]

class CommentAdmin(admin.ModelAdmin):
	display_fields = ["post", "author", "created"]

admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
admin.site.register(Comment, CommentAdmin)



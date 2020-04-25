from django.contrib import admin
from django.urls import path, include

# Register your models here.
from users_app.models import User, Message, Comment

class UserAdmin(admin.ModelAdmin):
    pass
admin.site.register(User, UserAdmin)

class MessageAdmin(admin.ModelAdmin):
    pass
admin.site.register(Message, MessageAdmin)

class CommentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Comment, CommentAdmin)

# ****************
urlpatterns = [
# Your app's urls is lined to the project
    path('admin/',admin.site.urls),
    path('users_app/', include('users_app.urls')),
]
from django.contrib import admin
from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    """
    我们使用继承了ModelAdmin的定制类来告诉Django管理站点中需要注册我们自己的模型（model）。
    在这个类中，我们可以包含一些关于如何在管理站点中展示模型（model）的信息以及如何与该模型（model）进行交互。
    list_display属性允许你在设置一些你想要在管理对象列表页面显示的模型（model）字段。

    作者：夜夜月
    链接：https://www.jianshu.com/p/05810d38f93a
    來源：简书
    著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
    """
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug':('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']

class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)

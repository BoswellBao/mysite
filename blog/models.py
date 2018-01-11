from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,
                     self).get_queryset().filter(status = 'published')

class Post(models.Model):
    """
    title： 这个字段对应帖子的标题。它是CharField，在SQL数据库中会被转化成VARCHAR。
    slug：这个字段将会在URLs中使用。slug就是一个短标签，该标签只包含字母，数字，下划线或连接线。我们将通过使用slug字段给我们的blog帖子构建漂亮的，友好的URLs。
          我们给该字段添加了unique_for_date参数，这样我们就可以使用日期和帖子的slug来为所有帖子构建URLs。在相同的日期中Django会阻止多篇帖子拥有相同的slug。
    author：这是一个ForeignKey。这个字段定义了一个多对一（many-to-one）的关系。我们告诉Django一篇帖子只能由一名用户编写，一名用户能编写多篇帖子。
            根据这个字段，Django将会在数据库中通过有关联的模型（model）主键来创建一个外键。在这个场景中，我们关联上了Django权限系统的User模型（model）。
            我们通过related_name属性指定了从User到Post的反向关系名。我们将会在之后学习到更多关于这方面的内容。
    body：这是帖子的主体。它是TextField，在SQL数据库中被转化成TEXT。
    publish：这个日期表明帖子什么时间发布。我们使用Djnago的timezone的now方法来设定默认值。This is just a timezone-aware datetime.now（译者注：这句该咋翻译好呢）。
    created：这个日期表明帖子什么时间创建。因为我们在这儿使用了auto_now_add，当一个对象被创建的时候这个字段会自动保存当前日期。
    updated：这个日期表明帖子什么时候更新。因为我们在这儿使用了auto_now，当我们更新保存一个对象的时候这个字段将会自动更新到当前日期。
    status：这个字段表示当前帖子的展示状态。我们使用了一个choices参数，这样这个字段的值只能是给予的选择参数中的某一个值。
            （译者注：传入元组，比如(1,2)，那么该字段只能选择1或者2，没有其他值可以选择）
    作者：夜夜月
    链接：https://www.jianshu.com/p/05810d38f93a
    來源：简书
    著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
    """

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250, blank=True)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    author = models.ForeignKey(User,
                               related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')
    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ('-publish',)

    def __str__(self):   # 总是返回一个字符串，在django管理站点时有用
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail',   # 这里的blog是命名空间，响应mysite/urls里面定义的namespace，post_detail就是该namespace里的一个name，
                       args=[                   # 再把args插入到name对应的路径中,最后生成blog/2018/01/04/slug类型的url
                           self.publish.year,
                           self.publish.strftime('%m'),
                           self.publish.strftime('%d'),
                           self.slug
                       ])

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)   # 禁用那些不合适的评论

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)
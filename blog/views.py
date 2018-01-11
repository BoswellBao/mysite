from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail


def post_share(request, post_id):
    '''
    此视图完成以下工作：
    我们定义了post_share视图，参数为request对象和post_id。
    我们使用get_object_or_404快捷方法通过ID获取对应的帖子，并且确保获取的帖子有一个published状态。
    我们使用同一个视图（view）来展示初始表单和处理提交后的数据。我们会区别被提交的表单和不基于这次请求方法的表单。
    我们将使用POST来提交表单。如果我们得到一个GET请求，一个空的表单必须显示，而如果我们得到一个POST请求，则表单需要提交和处理。
    因此，我们使用request.method == 'POST'来区分这两种场景。
    :param request:
    :param post_id:
    :return:
    '''
    # 通过id取邮件
    post = get_object_or_404(Post, id=post_id, status='draft')
    cd = None
    sent = False
    if request.method == 'POST':
        # 表单被提交了
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # 表单数据通过了验证，如果没通过验证的话，直接返回上面的form，里面还带有用户原来填写的数据
            cd = form.cleaned_data
            # 发送邮件
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, '277532844@qq.com', [cd['to']])
            sent = True   # 只有邮件成功发送sent才会是True
    else:
        # 如果不是POST请求，只返回一个空表单实例，让用户填写
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post':post, 'form':form, 'sent':sent, 'cd':cd})

class PostListView(ListView):
    """
    这个视图类和下面的post_list功能一样，但更简洁，只需要继承ListView，然后配置相关属性即可
    ListView做了以下操作：
    使用一个特定的查询集（QuerySet）代替取回所有的对象。代替定义一个queryset属性，我们可以指定model = Post然后Django将会构建Post.objects.all() 查询集（QuerySet）给我们。
    使用环境变量posts给查询结果。如果我们不指定任意的context_object_name默认的变量将会是object_list。
    对结果进行分页处理每页只显示3个对象。
    使用定制的模板（template）来渲染页面。如果我们不设置默认的模板（template），ListView将会使用blog/post_list.html。
    """
    model = Post
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


# def post_list(request):
#     object_list = Post.objects.all()
#     paginator = Paginator(object_list, 3)   # 每页三条记录
#     page = request.GET.get('page')
#     try:
#         posts = paginator.page(page)
#     except PageNotAnInteger:
#         # 如果page不是一个integer，就传递第一页
#         posts = paginator.page(1)
#     except EmptyPage:
#         # 如果page在页数范围外，就传递最后一页
#         posts = paginator.page(paginator.num_pages)
#     return render(request, 'blog/post/list.html', {'page':page, 'posts':posts})

def post_detail(request, year, month, day, slug):   # request后面的参数分别对应url尖括号中的变量
    post = get_object_or_404(Post, slug=slug, status='draft', publish__year=year, publish__month=month, publish__day=day)   # 查询一条数据
    # 列出active是True的评论
    comments = post.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        # 接收一个评论
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # 创建一个评论对象，但还不存入数据库
            new_comment = comment_form.save(commit=False)
            # 为评论分配当前的文章
            new_comment.post = post
            # 保存评论到数据库
            new_comment.save()
        else:
            comment_form = CommentForm()

    return render(request, 'blog/post/detail.html', {'post':post,
                                                     'comments':comments,
                                                     'new_comment':new_comment,
                                                     'comment_form':comment_form})



from django.core.mail import send_mail

send_mail('Django mail', 'This was sent with Django.哈哈哈', '277532844@qq.com', ['bq277532@163.com','277532844@qq.com'], fail_silently=False)

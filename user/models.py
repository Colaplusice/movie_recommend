from django.db import models
from django.db.models import Avg


class User(models.Model):
    username = models.CharField(max_length=32, unique=True, verbose_name="账号")
    password = models.CharField(max_length=32, verbose_name="密码")
    phone = models.CharField(max_length=32, verbose_name="手机号码")
    name = models.CharField(max_length=32, verbose_name="名字", unique=True)
    address = models.CharField(max_length=32, verbose_name="地址")
    email = models.EmailField(verbose_name="邮箱")

    class Meta:
        verbose_name_plural = "用户"
        verbose_name = "用户"

    def __str__(self):
        return self.name


class Tags(models.Model):
    name = models.CharField(max_length=32, verbose_name="标签", unique=True)

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = "标签"

    def __str__(self):
        return self.name


class Movie(models.Model):
    tags = models.ManyToManyField(Tags, verbose_name='标签', blank=True)
    collect = models.ManyToManyField(User, verbose_name="收藏者", blank=True)
    sump = models.IntegerField(verbose_name="收藏人数", default=0)
    name = models.CharField(verbose_name="电影名称", max_length=32, unique=True)
    director = models.CharField(verbose_name="导演名称", max_length=128)
    country = models.CharField(verbose_name="国家", max_length=32)
    years = models.CharField(verbose_name="年份", max_length=32)
    leader = models.CharField(verbose_name="主演", max_length=128)
    d_rate_nums = models.IntegerField(verbose_name="豆瓣评价数")
    d_rate = models.CharField(verbose_name="豆瓣评分", max_length=32)
    intro = models.TextField(verbose_name="描述")
    num = models.IntegerField(verbose_name="浏览量", default=0)
    pic = models.FileField(verbose_name="封面图片", max_length=64, upload_to='movie_cover')
    prize = (("奥斯卡", "奥斯卡"), ("戛纳", "戛纳"), ("金鸡", "金鸡"), ("None", "None"))
    good = models.CharField(
        verbose_name="获奖", max_length=32, default=None, choices=prize
    )

    class Meta:
        verbose_name = "电影"
        verbose_name_plural = "电影"

    def __str__(self):
        return self.name


class Rate(models.Model):
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, blank=True, null=True, verbose_name="电影id"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, verbose_name="用户id",
    )
    mark = models.FloatField(verbose_name="评分")
    create_time = models.DateTimeField(verbose_name="发布时间", auto_now_add=True)

    @property
    def avg_mark(self):
        average = Rate.objects.all().aggregate(Avg('mark'))['mark__avg']
        return average

    class Meta:
        verbose_name = "评分信息"
        verbose_name_plural = verbose_name


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    content = models.CharField(max_length=64, verbose_name="内容")
    create_time = models.DateTimeField(auto_now_add=True)
    good = models.IntegerField(verbose_name="点赞", default=0)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name="电影")

    class Meta:
        verbose_name = "评论"
        verbose_name_plural = verbose_name


class Num(models.Model):
    users = models.IntegerField(verbose_name="用户数量", default=0)
    movies = models.IntegerField(verbose_name="电影数量", default=0)
    comments = models.IntegerField(verbose_name="评论数量", default=0)
    rates = models.IntegerField(verbose_name="评分汇总", default=0)
    actions = models.IntegerField(verbose_name="活动汇总", default=0)
    message_boards = models.IntegerField(verbose_name="留言汇总", default=0)

    class Meta:
        verbose_name = "数据统计"
        verbose_name_plural = verbose_name

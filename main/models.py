from django.db import models
from django.db.models.fields.related import ForeignKey
from decimal import Decimal

class Post(models.Model):
    category_choices = {
        # 후자 값으로 html에 출력을 원하면 {{post.get_필드명_display}}
        ('etc', '잡담'),
        ('information', '정보'),
        ('review', '후기')
    } 

    title = models.CharField(verbose_name='제목', max_length=100)
    category = models.CharField(verbose_name='카테고리', max_length=100, choices=category_choices, default='top')
    text = models.TextField(verbose_name='본문')
    # related_name 에서는 post 관련이라는 것을 명시해두는 것이 좋다
    writer = models.ForeignKey('account.CustomUser', verbose_name='작성자', related_name='writer_post', on_delete=models.CASCADE, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='작성시간')
    tags = models.ManyToManyField('Product', verbose_name='태그', related_name='product_tags', blank=True)
    view_count = models.IntegerField(verbose_name='조회수', default=0)
    liked_user = models.ManyToManyField('account.CustomUser', verbose_name='스크랩유저', related_name='liked_post', blank=True)
    is_review = models.BooleanField(verbose_name='후기여부', default=False)
    is_liked = models.BooleanField(verbose_name='인기글', default=False)
    img = models.ImageField(upload_to='main/', blank=True, null=True)

    def __str__(self):
        return self.title
    def summary(self):
        return self.text [:20]


#auto_now : 해당 모델이 save 가 발생할 때 마다 해당 필드의 값을 현재 날짜시간으로 업데이트 하는 옵션.
#auto_now_add : 하나의 레코드(데이터베이스의 실제 기록되는 한 행의 데이터) 가 생성될 때, 그 때의 날짜시간을 해당 필드의 값으로 업데이트 하는 옵션

class Comment(models.Model):
    post=models.ForeignKey('Post', verbose_name='포스트', related_name='comment_post', on_delete=models.CASCADE, blank=True, null=True)
    writer=models.ForeignKey('account.CustomUser', verbose_name='작성자', related_name='writer_comment', on_delete=models.CASCADE, blank=True, null=True)
    contents=models.TextField(verbose_name='내용')
    created_at=models.DateTimeField(verbose_name='작성시간', auto_now_add=True)

class Product(models.Model):
    pID=models.CharField(verbose_name='공연ID', max_length=200, blank=True, null=True)
    title=models.CharField(verbose_name='제목', max_length=200)
    img=models.ImageField(verbose_name='포스터', blank=True, upload_to='main/')
    openDate = models.DateTimeField(verbose_name='예매오픈시간', blank=True, null=True)
    likes=models.ManyToManyField('account.CustomUser', verbose_name='담은유저', related_name='liked_product', blank=True)
    score1=models.DecimalField(verbose_name='넘버점수', max_digits=10, decimal_places=4, default=0.0)
    score2=models.DecimalField(verbose_name='배우점수', max_digits=10, decimal_places=4, default=0.0)
    score3=models.DecimalField(verbose_name='무대점수', max_digits=10, decimal_places=4, default=0.0)
    score4=models.DecimalField(verbose_name='스토리점수', max_digits=10, decimal_places=4, default=0.0)
    review_count = models.IntegerField(verbose_name='리뷰수', default=0)

    def __str__(self):
        return self.title



#개인후기(다이어리) 모델
# class Diary(models.Model):
#   title=models.CharField(verbose_name='제목', max_length=200)
#   musical_title=models.CharField(verbose_name='뮤지컬 이름', max_length=200)
#   text=models.TextField(verbose_name='본문')
#   img=models.ImageField(verbose_name='사진', blank=True, upload_to='main/')
#   view_date=models.DateField(verbose_name='관람일', blank=True, null=True)
#   comment=models.CharField(verbose_name='한줄평', max_length=200, blank=True, null=True)
#   location=models.CharField(verbose_name='관람장소', blank=True, null=True)
#   seat=models.CharField(verbose_name='좌석', max_length=100, blank=True, null=True)
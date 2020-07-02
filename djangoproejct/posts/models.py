from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.conf import settings

# Create your models here.
class Post(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    content=models.TextField()
    image = ProcessedImageField(
        upload_to='posts/images', # 저장 위치
        processors=[ResizeToFill(600,600)], # 처리할 작업 목록
        format='JPEG', # 저장 포맷(확장자)
        options= {'quality': 90 }, # 저장 포맷 관련 옵션 (JPEG 압축률 설정)
        blank=True,
        null=True,
    )
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='like_posts')
    
class Comment(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    post=models.ForeignKey(Post,on_delete=models.CASCADE) #CASCADE : 부모가 삭제되면 자기자신도 삭제
    content=models.TextField()




#python manage.py makemigrations :마이그레이션 파일 초안 생성
#python manage.py migrate : 마이그레이션 파일을 데이터베이스에 적용
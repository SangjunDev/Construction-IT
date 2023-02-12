from django.db import models
from django.conf import settings
from django.db.models import Count

class InstallationSite(models.Model):
  region = models.CharField(max_length = 50, unique=True,verbose_name='지역')
  site = models.CharField(max_length=100, unique=True, verbose_name='현장 위치')
  sitenickname = models.CharField(max_length=100, unique=True, verbose_name='별칭', default = '')
    
  def __str__(self):
    return self.region +' / '+ self.sitenickname
  
  class Meta:
    db_table = 'installationsite'
    verbose_name = '설치 현장'
    verbose_name_plural = '설치 현장'




class topicManage(models.Model):
  maintopic = models.CharField(max_length = 50,verbose_name='메인 토픽')
  subtopic = models.CharField(max_length = 50 , unique = True , verbose_name = '서브 토픽')
  topicnicname = models.CharField(max_length=100, unique=True, verbose_name='별칭', default = '')
    
  def __str__(self):
    return self.topicnicname
  
  class Meta:
    db_table = 'topicmanage'
    verbose_name = '토픽 종합 관리'
    verbose_name_plural = '토픽 종합 관리'    
    
      
class Manage(models.Model):
  managenicname = models.CharField(max_length=100, unique=True, verbose_name='별칭', default = '')
  
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE ,verbose_name='유저')
  
  installationsite = models.ForeignKey(InstallationSite, null=True, on_delete=models.SET_NULL,verbose_name='현장 선택')


  serverip = models.CharField(max_length = 50,verbose_name='MQTT 접속 IP')
  
  serverport = models.CharField(max_length = 50,verbose_name='MQTT 접속 Port')
  
  topic = models.ManyToManyField(topicManage, verbose_name='토픽')

  def __str__(self):
    return self.user.name

  @property
  def maintopic_count(self):
      return self.topic.values('subtopic').annotate(count=Count('subtopic')).count()
  
  class Meta:
    db_table = 'manage'
    verbose_name = '회원별 토픽 관리'
    verbose_name_plural = '회원별 토픽 관리'

      
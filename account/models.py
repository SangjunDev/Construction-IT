from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
  #일반 user 생성
  
  def create_user(self, email, name, password=None):
    pass

from unicodedata import name
from django.contrib.auth.hashers import make_password
import uuid
from django.db import models


class CommonUser(models.Model):
    userid = models.UUIDField(default=uuid.uuid4, unique=True,
                              primary_key=True, editable=False, verbose_name="使用者ID")
    username = models.CharField(
        max_length=100, unique=True, verbose_name="使用者名稱")
    password = models.CharField(max_length=100, verbose_name="使用者密碼")
    hobby = models.CharField(max_length=200, default=None,
                             blank=True, null=True, verbose_name="使用者興趣")

    create_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def to_json(self):
        data = {
            "userid": self.userid,
            "username": self.username,
            "password": self.password,
            "hobby": self.hobby
        }
        return data

    # 儲存使用者
    def save(self, *args, **kwargs):
        try:
            # if no such user, raise exception
            user = CommonUser.objects.get(username=self.username)

            # finding exist user, checking the password changed or not
            if self.password != user.password:
                self.password = make_password(self.password)
            super(CommonUser, self).save(*args, **kwargs)
        except:
            # run add new user
            self.password = make_password(self.password)
            super(CommonUser, self).save(*args, **kwargs)

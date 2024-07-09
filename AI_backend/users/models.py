from django.db import models


# Create your models here.
class UserInfo(models.Model):

    user_id = models.AutoField(primary_key=True)
    username = models.CharField("用户名", max_length=100)
    password = models.CharField("密码", max_length=100)
    realname = models.CharField("真实姓名", max_length=100)
    email = models.EmailField("邮箱", null=True, blank=True)
    phone = models.CharField("电话号码", max_length=100, null=True, blank=True)
    status = models.CharField("用户身份", max_length=100)

    age = models.IntegerField("年龄", null=True, blank=True)
    sex = models.IntegerField("性别", null=True, blank=True)
    birth_day = models.DateTimeField("出生日期", null=True, blank=True)
    user_level = models.IntegerField("用户等级", null=True, blank=True)
    role = models.IntegerField("角色", null=True, blank=True)  # 新增字段，类型为 int

    level = models.IntegerField()

    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    modify_time = models.DateTimeField("修改时间", auto_now=True)

    def __str__(self):
        return str(self.user_id)

    class Meta:
        verbose_name = "镜像信息"
        verbose_name_plural = verbose_name

    def update_role_and_status(self):
        if self.status and not self.role:
            if self.status == 'student':
                self.role = 1
            elif self.status == 'teacher':
                self.role = 2
        elif self.role and not self.status:
            if self.role == 1:
                self.status = 'student'
            elif self.role == 2:
                self.status = 'teacher'
    def save(self, *args, **kwargs):
        self.update_role_and_status()
        super(UserInfo, self).save(*args, **kwargs)

class CurrentUser(models.Model):
    id = models.AutoField(primary_key=True)
    current_user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Post(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    title=models.CharField(max_length=100,null=True)
    CATEGORY=(
        ('UI', 'UI'),
        ('Performance','Performance'),
        ('Functionality','Functionality'),
        ('Bugs', 'Bugs')
    )
    category=models.CharField(max_length=50,null=True,choices=CATEGORY)
    description=models.CharField(max_length=3000,null=True)
    date_created=models.DateTimeField(auto_now_add=True, null=True)
    underWork=models.BooleanField(null=True,default=False)

    def __str__(self):
        return self.title





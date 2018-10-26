import MySQLdb
from django.db import models

# Create your models here.
from user.models import User


class Board(models.Model):
    title = models.CharField(max_length=50)
    message = models.TextField(blank=True)
    hit = models.IntegerField(default=0)
    reg_date = models.DateTimeField(auto_now_add=True)
    group_no = models.IntegerField(default=0)
    order_no = models.IntegerField(default=0)
    depth = models.IntegerField(default=0)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return 'Board(%s, %s, %s, %s, %s, %s, %s, %s)'\
               % (self.title, self.message, self.hit, self.reg_date
                  , self.group_no, self.order_no, self.depth, self.user_id)


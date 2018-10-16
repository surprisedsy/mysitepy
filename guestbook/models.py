from django.db import models

# Create your models here.
class Guestbook(models.Model):
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)
    message = models.TextField(blank=True)

    def __str__(self):
        return 'Guestbook(%s, %s, %s, %s)' % (self.name, self.password, self.date, self.message)

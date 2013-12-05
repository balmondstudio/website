from django.db import models

class Tweet(models.Model):
  term = models.TextField(unique=True)
  text = models.TextField()
  screen_name = models.TextField()

  def __unicode__(self):
    return self.term

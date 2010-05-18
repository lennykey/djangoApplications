from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Mannschaft(models.Model):
    name = models.CharField(max_length=30)
    
    def __unicode__(self):
        return self.name


class Begegnung(models.Model):

    mannschaftHeim = models.ForeignKey(Mannschaft, unique=False, 
                                       related_name="mannschaftHeim_mannschaft")
    mannschaftGast = models.ForeignKey(Mannschaft, unique=False, 
                                       related_name="mannschaftGast_mannschaft")

    toreHeim = models.IntegerField(max_length=2)
    toreGast = models.IntegerField(max_length=2)
    datum = models.DateTimeField()
    art = models.CharField(max_length=30)
    
    def __unicode__(self):
        return u'%s %s %s' % (self.mannschaftHeim, self.mannschaftGast,
                               self.datum)


 
class Tipps(models.Model):
    user = models.ForeignKey(User, unique=False)
    begegnung = models.ForeignKey(Begegnung, unique=False)
    
    toreHeim = models.IntegerField(max_length=2) 
    toreGast = models.IntegerField(max_length=2) 
    tippDatum = models.DateTimeField()
    
    def __unicode__(self):
        return u'%s %s' % (self.user, self.begegnung)
   

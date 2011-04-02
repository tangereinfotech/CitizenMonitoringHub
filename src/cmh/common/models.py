from django.db import models

class Category(models.Model):
    name   = models.CharField (max_length = 200)
    parent = models.ForeignKey ('Category', blank = True, null = True)

class Attribute (models.Model):
    name     = models.CharField (max_length = 200)
    category = models.ForeignKey (Category)
    parent   = models.ForeignKey ('Attribute', blank = True, null = True)
    
    def __unicode__(self):
        return u'%s.%s' % (self.category.name , self.name)
        


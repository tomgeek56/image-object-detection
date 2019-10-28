from django.db import models

# Create your models here.
class DetectionObject:
    x = 0
    y = 0
    width = 0
    height = 0
    name = ''

    def set(self, values):
        self.x, self.y, self.w, self.h, self.name, _ = values
    
    def __str__(self):
        return f'Detection {self.x} {self.y} {self.width} {self.height}'
    
    def __unicode__(self):
        return 'General settings'
from django.db import models

LEVEL_OF_IMPORTANCE = [
    ('VU', 'Very umportant'), 
    ('UN', 'Unimportant'), 
    ('NL', 'Normal'), 
    ('IM', 'Important'), 
    ('VI', 'Very important'),
]

CATEGORY = [
    ('PER', 'Personal'), 
    ('FIN', 'Finance'), 
    ('BUS', 'Business'),
]

class Task(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    level_of_importance = models.CharField(choices=LEVEL_OF_IMPORTANCE, default='Normal', max_length=100)
    category = models.CharField(choices=CATEGORY, default='Personal', max_length=100)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_completed = models.BooleanField(default=False)
    owner = models.ForeignKey('auth.User', related_name='tasks', on_delete=models.CASCADE)

    class Meta:
        ordering = ['start_time']

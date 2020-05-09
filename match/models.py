from django.db import models


# Create your models here.
class Human(models.Model):
    first_name = models.CharField(max_length=30)
    second_name = models.CharField(max_length=60)
    age = models.SmallIntegerField()
    gender = models.SmallIntegerField()
    avatar = models.ImageField()

    def __str__(self):
        gender_map = {0: 'undefined', 1: 'male', 2: 'female'}
        return f'{self.first_name} {self.second_name}, {self.age} y.o., {gender_map[self.gender]}'

    class Meta:
        managed = False
        db_table = 'human_human'


class Match(models.Model):
    first_name = models.CharField(max_length=30)
    second_name = models.CharField(max_length=60)
    age = models.SmallIntegerField()
    gender = models.SmallIntegerField()
    matched_human = models.ForeignKey(Human, on_delete=models.DO_NOTHING)

    def __str__(self):
        gender_map = {0: 'undefined', 1: 'male', 2: 'female'}
        return f'{self.pk}: {self.first_name} {self.second_name} of age {self.age} and gender {gender_map[self.gender]}'

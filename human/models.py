from django.db import models
from django.contrib.staticfiles import finders


# Create your models here.
class Human(models.Model):
    avatar = models.ImageField(upload_to=finders.find('avatars'), default=finders.find('avatars/cat_default.bmp'))
    first_name = models.CharField(max_length=30)
    second_name = models.CharField(max_length=60)
    # В реальном проекте здесь дата рождения будет
    age = models.SmallIntegerField()
    """
    Может быть булеан, если выбор должен быть определённым
    Если вариантов много и они где-то используются,
        то можно определить Enum или что-то вроде
    0 - не определён
    1 - мужской
    2 - женский
    """
    _gender = models.SmallIntegerField(db_column='gender')

    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, value):
        # Можно заменить валидатором, скорее всего, но в этом пока не разобрался
        self._gender = int(value) if value in (0, 1, 2, '0', '1', '2') else 0

    def get_gender_str(self):
        gender_map = {0: 'Undefined', 1: 'Male', 2: 'Female'}
        return gender_map[self._gender]

    def __str__(self):
        gender_map = {0: 'Human', 1: 'Male', 2: 'Female'}
        return f'{self.pk}: {gender_map[self._gender]} being {self.first_name} {self.second_name} of age {self.age}'

    class Meta:
        ordering = ['-pk']

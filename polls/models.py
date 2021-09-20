from django.db import models

# Create your models here.
class Category(models.Model):
    category = models.CharField(max_length=60)

    def __str__(self):
        return self.category

    class Meta(object):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Test(models.Model):
    title = models.CharField(max_length=4096)
    visible = models.BooleanField(default=False)
    max_points = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.title
    

    class Meta(object):
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'



class Question(models.Model):
    title_test = models.ForeignKey(Test, on_delete=models.DO_NOTHING)
    question_text = models.TextField()
    question_point = models.IntegerField(default = 1)
    
    option_one = models.TextField(max_length=30)
    option_one_points = models.IntegerField(default=0)
    option_one_visible = models.BooleanField(default=True)

    option_two = models.TextField(max_length=30)
    option_two_points = models.IntegerField(default=0)
    option_two_visible = models.BooleanField(default=True)
    
    option_three = models.TextField(max_length=30)
    option_three_points = models.IntegerField(default=0)
    option_three_visible = models.BooleanField(default=True)
    
    option_four = models.TextField(max_length=30)
    option_four_points = models.IntegerField(default=0)
    option_four_visible = models.BooleanField(default=True)


    def __str__(self):
        return self.question_text

    class Meta(object):
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Profile(models.Model):
    external_id = models.PositiveIntegerField('id пользователя', unique=True)
    name = models.CharField('имя пользователя', max_length=32, null=True, blank=True)
    def __str__(self):
        return str(self.external_id)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

class Result(models.Model):
    external_id = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)
    title = models.ForeignKey(Test, on_delete=models.DO_NOTHING)
    points = models.IntegerField()
    max_points = models.IntegerField(default=0)                                          #сделать в боте чтобы он возвращал значение max_points в соответствие с title

    def __str__(self):
        return str(self.external_id)

    class Meta:
        verbose_name = 'Результат'
        verbose_name_plural = 'Результаты'

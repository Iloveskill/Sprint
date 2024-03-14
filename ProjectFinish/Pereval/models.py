from django.db import models
from .services import get_path_upload_images


class Users(models.Model):
    fam = models.CharField(max_length=128, verbose_name='Фамилия')
    name = models.CharField(max_length=128, verbose_name='Имя')
    otc = models.CharField(max_length=128, verbose_name='Отчество')
    email = models.EmailField(max_length=128)
    phone = models.IntegerField(verbose_name='Телефон')

    def __str__(self):
        return f'fam: {self.fam}, name: {self.name}, otc: {self.otc}, email: {self.email}, phone: {self.phone}'


class Coords(models.Model):
    latitude = models.FloatField(max_length=20, verbose_name='Широта')
    longitude = models.FloatField(max_length=20, verbose_name='Долгота')
    height = models.IntegerField(verbose_name='Высота')

    def str(self):
        return f'Широта: {self.latitude}, долгота: {self.longitude}, высота: {self.height}.'


class Level(models.Model):
    LEVEL = [
        ('1B', '1Б'),
        ('2A', '2А'),
        ('2B', '2Б'),
        ('3A', '3А'),
        ('3B', '3Б'),
        ('4A', '4А'),
        ('4B', '4Б'),
        ('5A', '5А'),
        ('5B', '5Б'),
        ('6A', '6А'),
        ('6B', '6Б')
    ]

    summer = models.CharField(max_length=2, choices=LEVEL, verbose_name='Лето')
    autumn = models.CharField(max_length=2, choices=LEVEL, verbose_name='Осень')
    winter = models.CharField(max_length=2, choices=LEVEL, verbose_name='Зима')
    spring = models.CharField(max_length=2, choices=LEVEL, verbose_name='Весна')

    def str(self):
        return f'Уровни сложности перевала: зима: {self.winter}, лето: {self.summer}, ' \
               f'осень: {self.autumn}, весна: {self.spring}.'




class SprActivitiesTypes(models.Model):

    TYPE = [
        ('foot', 'Пешком'),
        ('ski', 'Лыжи'),
        ('catamaran', 'Катамаран'),
        ('kayak', 'Байдарка'),
        ('raft', 'Плот'),
        ('alloy', 'Сплав'),
        ('bicycle', 'Велосипед'),
        ('car', 'Автомобиль'),
        ('sail', 'Парус'),
        ('horseback', 'Верхом'),
    ]

    title = models.CharField(max_length=10, choices=TYPE, verbose_name='Тип похода')




class Perevals(models.Model):

    STATUS = [
        ('new', 'Создано'),
        ('pending', 'Взято в работу'),
        ('accepted', 'Успешно'),
        ('rejected', 'Отклонено')
    ]

    beauty_title = models.CharField(max_length=200, verbose_name='Название топонима')
    title = models.CharField(max_length=200, verbose_name='Название перевала')
    other_titles = models.CharField(max_length=200)
    connect = models.CharField(max_length=200)
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    status = models.CharField(max_length=10, choices=STATUS, default='new', verbose_name="Статус заявки")

    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    coord = models.OneToOneField(Coords, on_delete=models.CASCADE)

    def str(self):
        return f'Перевал № {self.pk} - {self.beauty_title} находится в статусе "{self.status}".'


class Images(models.Model):
    pereval = models.ForeignKey(Perevals, on_delete=models.CASCADE, related_name='images')
    title = models.CharField(max_length=200, verbose_name='Название изображения')
    date_added = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name='Дата добавления')
    # image = models.ImageField(upload_to=get_path_upload_images, verbose_name='Изображение', blank=True, null=True)
    image = models.ImageField(upload_to='images', verbose_name='Изображение', blank=True, null=True)


from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from pereval.models import Perevals, Users, Coords, Level, Images
from pereval.serializers import PerevalsUpdateSerializer


class TestURL(TestCase):

    # Работоспособность основной страницы сайта
    def test_mainpage(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    # Работоспособность страницы дял отправки POST запросов
    def test_submitdata(self):
        response = self.client.get('/submitData/')
        self.assertEqual(response.status_code, 200)

class TestPerevals(TestCase):

    # Тест на создание объекта модели Perevals
    def test_create_perevals_success(self):
        client = APIClient()
        url = '/submitData/'
        data = {
            'beauty_title': 'Название топонима',
            'title': 'Название перевала',
            "other_titles": "больше текста",
            'connect': 'Связь',
            'level': {
                'summer': '1B',
                'autumn': '2A',
                'winter': '3B',
                'spring': '4A',
            },
            'user': {
                'fam': 'Иванов',
                'name': 'Иван',
                'otc': 'Иванович',
                'email': 'ivan@example.com',
                'phone': 1234567890,
            },
            'coord': {
                'latitude': 55.12345,
                'longitude': 37.54321,
                'height': 100,
            },
            "images": [{"title": "Восхождение на Белуху через перевал Делоне",
                        "image": "https://avatars.mds.yandex.net/i?id=a888b186bc0ad309c4ec76e8004d5182712da87e-3163703-images-thumbs&n=13"},
                       {"title": "Взгляд новичка или Белуха в марте",
                        "image": "http://altai-photo.ru/_pu/1/81926227.jpg"}]
        }

        response = client.post(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK     # Запрос отправлен
        assert response.data['status'] == status.HTTP_200_OK  # Его результат 200
        assert response.data['message'] == 'Успех!'
        assert response.data['id'] is not None


    def test_create_perevals_invalid_data(self):
        client = APIClient()
        url = '/submitData/'
        data = {
            'beauty_title': 'Название топонима',
            'title': 'Название перевала',
            # missing required fields 'connect', 'level', 'user', 'coord'
        }

        response = client.post(url, data, format='json')
        assert response.data['status'] == status.HTTP_400_BAD_REQUEST
        assert response.data['message'] == 'Некорректный запрос'
        assert response.data['id'] is None


# не успел доделать
# class TestSerializers(TestCase):
#
#     def test_validate_user_data(self):
#         images = [
#             {
#                 "title": "Восхождение на Белуху через перевал Делоне",
#                 "image": "https://avatars.mds.yandex.net/i?id=a888b186bc0ad309c4ec76e8004d5182712da87e-3163703-images-thumbs&n=13"
#             },
#             {
#                 "title": "Взгляд новичка или Белуха в марте",
#                 "image": "http://altai-photo.ru/_pu/1/81926227.jpg"
#             }
#         ]
#
#         level = Level.objects.create(
#             summer='1B',
#             autumn='2A',
#             winter='3B',
#             spring='4A',
#         )  # Создаем объект Level
#
#         instance = Perevals.objects.create(
#             beauty_title='Название 1',
#             title='Перевал 1',
#             other_titles='Третье название',
#             connect='Связь',
#             status='new',
#             user=Users.objects.create(
#                 fam='Иванов',
#                 name='Иван',
#                 otc='Иванович',
#                 email='ivan@example.com',
#                 phone='1234567890',
#             ),
#             coord=Coords.objects.create(
#                 latitude=55.12345,
#                 longitude=37.54321,
#                 height=100,
#             ),
#             level=level  # Присваиваем полю level_id созданный ранее объект Level
#         )
#
#         # Создаем объекты Images и добавляем их в поле images
#         for img_data in images:
#             image = Images.objects.create(title=img_data['title'], image=img_data['image'])
#             instance.images.add(image)
#
#         for img_data in images:
#             image = Images.objects.create(
#                 title=img_data['title'],
#                 image=img_data['image'],
#                 pereval=instance  # Установка связи с экземпляром Perevals
#             )
#             instance.images.add(image)
#
#         data = {
#             'beauty_title': 'Название 2',
#             'title': 'Перевал 2',
#             'other_titles': 'Третье название 2',
#             'connect': 'Новая связь',
#             'status': 'new',
#             'user': {
#                 'fam': 'Петров',
#                 'name': 'Петр',
#                 'otc': 'Петрович',
#                 'email': 'petr@example.com',
#                 'phone': '1234567890',
#             },
#             'coord': {
#                 'latitude': 55.12345,
#                 'longitude': 37.54321,
#                 'height': 100,
#             },
#             "images": instance.images.values('id')  # Используем идентификаторы объектов Images
#         }
#
#         serializer = PerevalsUpdateSerializer(instance, data=data)
#         assert serializer.is_valid() is False
#         assert 'user' in serializer.errors.keys()

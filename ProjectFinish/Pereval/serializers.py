from .models import *
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from drf_writable_nested import WritableNestedModelSerializer


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = ['fam', 'name', 'otc', 'email', 'phone']


class CoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coords
        fields = ['latitude', 'longitude', 'height']


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ['summer', 'autumn', 'winter', 'spring']


class ImagesSerializer(serializers.ModelSerializer):
    image = serializers.URLField()
    date_added = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    class Meta:
        model = Images
        fields = ['title', 'date_added', 'image']


class PerevalsSerializer(WritableNestedModelSerializer):
    add_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    user = UsersSerializer()
    coord = CoordsSerializer()
    level = LevelSerializer()
    images = ImagesSerializer(many=True, required=False)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Perevals
        fields = ['beauty_title',
                  'title',
                  'other_titles',
                  'connect',
                  'status',
                  'add_time',
                  'level',
                  'user',
                  'coord',
                  'images'
                  ]


class PerevalsUpdateSerializer(WritableNestedModelSerializer):
    add_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    user = UsersSerializer()
    coord = CoordsSerializer()
    level = LevelSerializer()
    images = ImagesSerializer(many=True, required=False)
    status = serializers.CharField(read_only=True)

    def validate(self, validated_data):
        user_val_data = validated_data['user']
        user_original = self.instance.user
        error_messages = []

        if self.instance and self.instance.status != 'new':
            error_messages.append({
                "message": "Данный перевал принят в работу, информацию о нем уже нельзя поменять",
                "state": "0"
            })

        if any(user_val_data[field] != getattr(user_original, field) for field in
               ('fam', 'name', 'otc', 'email', 'phone')):
            error_messages.append({
                "message": "Информацию о пользователе нельзя изменять.",
                "state": "0"
            })

        if error_messages:
            raise ValidationError(error_messages)

        validated_data['message'] = "Данные успешно изменены!"
        validated_data['state'] = "1"

        return validated_data

    class Meta:
        model = Perevals
        fields = ['beauty_title',
                  'title',
                  'other_titles',
                  'connect',
                  'status',
                  'add_time',
                  'level',
                  'user',
                  'coord',
                  'images'
                  ]

    # def validate(self, validated_data):
    #     user_val_data = validated_data['user']
    #     user_original = self.instance.user
    #
    #     if self.instance and self.instance.status != 'new':
    #         raise serializers.ValidationError("Данный перевал принят в работу, информацию о нем уже нельзя поменять")
    #
    #     if any(user_val_data[field] != getattr(user_original, field) for field in
    #            ('fam', 'name', 'otc', 'email', 'phone')):
    #         raise ValidationError("Информацию о пользователе нельзя изменять.")
    #
    #     return validated_data

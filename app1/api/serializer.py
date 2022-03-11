from rest_framework import serializers
from ..models import Group, User


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'

    def to_representation(self, instance):
        data = super(GroupSerializer, self).to_representation(instance)
        if data.get('owner'):
            data.pop('owner')
        if data.get('created_at'):
            data.pop('created_at')
        return data


class GroupPartialSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ['id',]


class MyGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'

    def to_representation(self, instance):
        data = super(MyGroupSerializer, self).to_representation(instance)
        data['members']= User.objects.order_by('user_records__timestamp').filter(user_records__group__name=instance.name)
        return data


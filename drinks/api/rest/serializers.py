from rest_framework import serializers

from drinks.models import Drink


class DrinkSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Drink
        fields = ('id', 'name')

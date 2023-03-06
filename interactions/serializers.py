from rest_framework.serializers import ModelSerializer
from .models import Interactions

class InteractionsSerializer(ModelSerializer):
    class Meta:
        model = Interactions
        fields = ('id','usuario', 'comentario', 'data', 'aprovado')
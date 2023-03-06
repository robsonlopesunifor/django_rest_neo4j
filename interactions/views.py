# permite fazer create(), retrive(), uodate(), partial_update(), destroy(), list()
from rest_framework.viewsets import ModelViewSet
from .models import Interactions
from .serializers import InteractionsSerializer


class InteractionsViewSet(ModelViewSet):
    queryset = Interactions.objects.all() # pega todos do banco de dados
    serializer_class = InteractionsSerializer # como voce vai mostrar  esse dado
                                         # quais os campos que voce que inclua no json


import ipdb
from rest_framework import generics, views
from rest_framework.authtoken.views import ObtainAuthToken

from .models import Account
from .serializers import AccountSerializer


class AccountView(generics.ListCreateAPIView):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()


class AccountNewestView(generics.ListAPIView):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()

    def get_queryset(self):
        account_quantity = self.kwargs["num"]

        return self.queryset.order_by("-date_joined")[0:account_quantity]


class LoginView(ObtainAuthToken):
    def post(self, request: views.Request, *args, **kwargs) -> views.Response:
        # se eu quisesse retornar só o token eu usaria as linhas 12 e 13 mas como eu tbm quero enviar na resposta o usuário...
        # pega o token
        response = super().post(request, *args, **kwargs)
        token = response.data["token"]

        # usa o serializer padrão para pegar user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        account = serializer.validated_data["user"]
        acc_serializer = AccountSerializer(account)

        return views.Response(
            {
                "token": token,
                "user": acc_serializer.data,
            },
        )

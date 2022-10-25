from drf_spectacular.utils import extend_schema
from rest_framework import generics, views
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAdminUser

from .models import Account
from .permissions import OwnerPermission
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


class AccountDetailUpdateView(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [OwnerPermission]

    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    lookup_url_kwarg = "user_id"

    @extend_schema(exclude=True)
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)


class ActivateDeactivateAccountView(generics.UpdateAPIView, generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    lookup_url_kwarg = "user_id"

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = not instance.is_active
        instance.save()
        serializer = self.get_serializer(instance)

        return views.Response(serializer.data)

    @extend_schema(exclude=True)
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)


class LoginView(ObtainAuthToken):
    def post(self, request: views.Request, *args, **kwargs) -> views.Response:
        # se eu quisesse retornar só o token eu usaria as linhas 65 e 66 mas como eu tbm quero enviar na resposta o usuário...
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

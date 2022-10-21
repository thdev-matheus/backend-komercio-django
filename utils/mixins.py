class ProductSerializerByMethodMixin:
    # declara o atributo de instância que será utilizada, como None para forçar a reatribuição na view
    serializer_map = None

    # escreve um método getter que vai buscar na lista o serializer de acordo com o método que foi utilizado pelo cliente
    def get_serializer_class(self):
        # verifica se o atributo foi sobrescrito corretamente
        assert (
            self.serializer_map is not None
        ), f"'{self.__class__.__name__}' should include a `serializer_map` attribute"

        # retorna o respectivo serializer
        return self.serializer_map.get(self.request.method)

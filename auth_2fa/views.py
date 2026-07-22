from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
# Добавь это к остальным импортам вверху файла
from .services import generate_and_send_2fa_code
# Импортируем наши новенькие сериализаторы
from .serializers import RegisterSerializer, LoginRequestSerializer
from .serializers import VerifyCodeSerializer
User = get_user_model()


class RegisterView(APIView):
    def post(self, request):
        # 1. Засыпаем сырые JSON данные из запроса в наш сериализатор регистрации
        serializer = RegisterSerializer(data=request.data)
        # 2. Наш знакомый охранник. Запускает метод validate() внутри сериализатора
        if serializer.is_valid():

            user = serializer.save()
            # БАМ! Вызываем нашу службу, передаем ей нашего «живого» юзера
            generate_and_send_2fa_code(user)
            return Response(
                {"message": "Код подтверждения отправлен на email."},
                status=status.HTTP_201_CREATED
            )

        # 5. Если validate() нашел ошибку (например, email занят), возвращаем её обратно на сайт
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        # 1. Засыпаем сырые данные (email и пароль) в сериализатор входа
        serializer = LoginRequestSerializer(data=request.data)

        # 2. Наш охранник запускает validate().
        # Напомню: там проверяется, существует ли юзер и совпадает ли хэш пароля!
        if serializer.is_valid():
            # 3. Достаем того самого «живого» пользователя из нашей дополненной коробки validated_data,
            # которого мы туда заботливо положили строчкой attrs['user'] = user
            user = serializer.validated_data['user']

            generate_and_send_2fa_code(user)
            # 4. Возвращаем ответ, что первый этап входа успешен
            return Response(
                {"message": "Пароль верный. Код подтверждения отправлен на ваш email."},
                status=status.HTTP_200_OK
            )

        # 5. Если пароль не подошел или email нет в базе — возвращаем ошибку наружу
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Не забудь импортировать новый сериализатор вверху файла, если еще не сделал:
# from .serializers import VerifyCodeSerializer

class VerifyCodeView(APIView):
    def post(self, request):
        # 1. Передаем JSON (email и код) в наш сериализатор проверки
        serializer = VerifyCodeSerializer(data=request.data)

        # 2. Охранник запускает validate().
        # Там ищется юзер, проверяется код и что он еще не использован!
        if serializer.is_valid():
            # 3. Достаем объект кода подтверждения из коробки validated_data.
            # Мы его туда заботливо положили строчкой attrs['code_entry'] = code_entry
            code_entry = serializer.validated_data['code_entry']

            # 4. Меняем статус кода на True (использован), чтобы им нельзя было воспользоваться второй раз
            code_entry.using_status = True
            code_entry.save()  # Сохраняем это изменение в базу данных PostgreSQL

            # --- ЗДЕСЬ В БУДУЩЕМ БУДЕТ ГЕНЕРАЦИЯ JWT-ТОКЕНОВ ДЛЯ ДРУЖБЫ С ФРОНТЕНДОМ ---
            # Когда всё проверено, мы должны выдать пользователю его постоянный пропуск (Token)
            # --------------------------------------------------------------------------

            return Response(
                {"message": "Код успешно подтвержден! Вы вошли в систему."},
                status=status.HTTP_200_OK
            )

        # 5. Если код не подошел, устарел или уже был использован — возвращаем ошибку
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
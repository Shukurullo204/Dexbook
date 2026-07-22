from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    # Метод validate проверяет, не занят ли email
    def validate(self, attrs):
        email = attrs.get('email')

        # Проверяем, есть ли уже такой email в базе данных
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Пользователь с таким email уже зарегистрирован.")

        return attrs

    # Метод create запускается, когда всё проверено и мы хотим СОЗДАТЬ запись в БД
    def create(self, validated_data):
        # Достаем чистые данные
        email = validated_data['email']
        password = validated_data['password']


        user = User.objects.create_user(email=email, password=password)
        return user

    
class LoginRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Пользователь с таким email не найден.")

        if not user.check_password(password):
            raise serializers.ValidationError("Неверный пароль.")

        attrs['user'] = user
        return attrs


from rest_framework import serializers
from .models import EmailVerificationCode
from django.contrib.auth import get_user_model

User = get_user_model()


class VerifyCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    verification_code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        email = attrs.get('email')
        verification_code = attrs.get('verification_code')

        # 1. Сначала ищем пользователя по email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Пользователь с таким email не найден.")

        # 2. Ищем в ТВОЕЙ таблице ПОСЛЕДНИЙ активный код для этого пользователя
        # Мы фильтруем по юзеру, по коду и проверяем, что он еще не использован (using_status=False)
        code_entry = EmailVerificationCode.objects.filter(
            user=user,
            verification_code=verification_code,
            using_status=False
        ).last()  # Берем самый свежий код, если их вдруг несколько

        # 3. А вот теперь проверяем, нашли мы строчку в базе или нет!
        if not code_entry:
            # Если filter().last() вернул None (ничего не нашлось), значит код неверный
            raise serializers.ValidationError("Неверный или просроченный код подтверждения.")

        # Логика супер-бэкендера: сохраняем найденного юзера и сам объект кода в коробку attrs,
        # чтобы пульт views.py мог их использовать и не искать заново!
        attrs['user'] = user
        attrs['code_entry'] = code_entry

        return attrs


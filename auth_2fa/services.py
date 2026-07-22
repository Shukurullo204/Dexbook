import random
from django.core.mail import send_mail
from django.conf import settings
from .models import EmailVerificationCode


def generate_and_send_2fa_code(user):
    """
    Генерирует 6-значный код, сохраняет в БД для конкретного user
    и отправляет ему письмо на Gmail.
    """
    # 1. Генерируем случайное 6-значное число от 100000 до 999999
    # Превращаем в строку, чтобы было удобно хранить в CharField
    code = str(random.randint(100000, 999999))

    # 2. Сохраняем код в твою модельку EmailVerificationCode в БД
    # Обрати внимание: Django сам вытащит id из объекта user, который мы передали!
    EmailVerificationCode.objects.create(
        user=user,
        verification_code=code
    )

    # 3. Настраиваем тему и текст письма
    subject = "Ваш код подтверждения 2FA"
    message = f"Здравствуйте!\n\nВаш 6-значный код для подтверждения: {code}\nКод действует в течение 5 минут."

    # 4. Встроенная функция Django для отправки реальной почты
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,  # Твоя рабочая почта из settings.py
        recipient_list=[user.email],  # Кому шлем (вытаскиваем email из нашего user)
        fail_silently=False,  # Если будет ошибка отправки, Django нам громко сообщит
    )

    return code




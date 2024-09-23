from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    # Вызов стандартного обработчика исключений DRF
    response = exception_handler(exc, context)

    # Если исключение не обрабатывается стандартным обработчиком
    if response is None:
        # Логируем исключение
        logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)

        # Возвращаем стандартный ответ с 500 ошибкой
        return Response(
            {"detail": "Внутренняя ошибка сервера. Пожалуйста, повторите попытку позже."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    # Логирование известных ошибок
    logger.warning(f"Exception occurred: {exc}")
    
    return response

import time
import traceback

from django.conf import settings
from django.http import JsonResponse
from rest_framework.request import Request

from isapilib.utilities import insert_log


def safe_method(view_func):
    def wrapped_view(*args, **kwargs):
        try:
            return view_func(*args, **kwargs)
        except Exception as e:
            if settings.DEBUG:
                print(traceback.format_exc())

            return JsonResponse({
                'type': str(type(e)),
                'message': str(e)
            }, status=500)

    return wrapped_view


def logger(tipo, interfaz=None, log_all=False):
    interfaz = interfaz or getattr(settings, 'LOG_INTERFAZ', '')

    def decorador(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            request = next((arg for arg in args if isinstance(arg, Request)), None)

            try:
                response: JsonResponse = func(*args, **kwargs)
                end = time.time()
                if (hasattr(response, 'status_code') and response.status_code not in range(200, 300)) or log_all:
                    response_time = (end - start) * 1000
                    insert_log(request=request, response=response, interfaz=interfaz, tipo=tipo, time=response_time)
                return response
            except Exception as e:
                insert_log(request=request, response=str(e), interfaz=interfaz, tipo=tipo)
                raise e

        return wrapper

    return decorador

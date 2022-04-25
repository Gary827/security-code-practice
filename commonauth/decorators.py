from hashlib import algorithms_available
import json
import jwt
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from commonauth.models import *
from django.contrib.auth.models import User


def token_auth_required(view_func):
    # print("bbb", view_func)
    print("1111")

    def wrap(request, *args, **kwargs):
        try:
            print("222")
            if "HTTP_AUTHORIZATION" in request.META:
                print("444")
                token = request.META.get('HTTP_AUTHORIZATION').split()[1]
                decoded_token = jwt.decode(
                    token, settings.SECRET_KEY, algorithms=['HS256'])
                user = CommonUser.objects.get(
                    username=decoded_token['username'])
                kwargs['decoded_token'] = decoded_token
                kwargs['user'] = user
            else:
                kwargs['decoded_token'] = None
                kwargs['user'] = None
                return JsonResponse({"message": "no token"}, status=500)
        except Exception as e:
            print(e)
            return JsonResponse({"status_code": 401, "message": "Token Error"}, status=401)
        # a = view_func(request, *args, **kwargs)
        print("555")
        return view_func(request, *args, **kwargs)
    print("333")
    return wrap

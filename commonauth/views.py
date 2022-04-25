from ast import Delete
from asyncio.log import logger
from cmath import e
import logging
from multiprocessing import AuthenticationError
from operator import mod
import traceback
from unicodedata import name
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from commonauth.decorators import token_auth_required
from commonauth.models import *
import jwt
import json
from django.http import JsonResponse, HttpResponse
import datetime
from django.conf import settings
from django.contrib import auth

logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name='dispatch')
class User(View):
    # add user
    def post(self, request, *args, **kargs):
        try:
            req = json.loads(request.body)
            username = req["username"]
            password = req["password"]
            hobby = req["hobby"]
            user = CommonUser(username=username,
                              password=password, hobby=hobby)
            user.save()
            res = {
                "result": "ok",
            }
            return JsonResponse(res, status=200)
        except Exception as e:
            traceback.print_exc()
            print("error", str(e))
            return JsonResponse({"message": "failed", "error": str(e)}, status=500)

    # update user
    @method_decorator(token_auth_required)
    def put(self, request, *args, **kwargs):
        try:
            user = kwargs['user']
            req = json.loads(request.body)
            user.hobby = req['hobby']
            user.save()
            res = {
                "result": "ok"
            }
            print("666")
            print("ccc", res)
            return JsonResponse(res, status=200)
        except Exception as e:
            traceback.print_exc()
            print("error", str(e))
            return JsonResponse({"message": "failed", "Error": str(e)}, status=500)

    # get single user
    @method_decorator(token_auth_required)
    def get(self, request, *args, **kwargs):
        try:
            user = kwargs['user']
            res = {
                "result": "ok",
                "user": user.to_json()
            }
            return JsonResponse(res, status=200)
        except Exception as e:
            traceback.print_exc()
            print("error", str(e))
            return JsonResponse({"message": "failed", "error": str(e)}, status=500)

    # delete a user
    @method_decorator(token_auth_required)
    def delete(self, request, *args, **kwargs):
        try:
            user = kwargs['user']
            user.delete()
            res = {
                "result": "delete user successful"
            }
            return JsonResponse(res, status=200)
        except Exception as e:
            traceback.print_exc()
            print("error", str(e))
            return JsonResponse({"message": "failed", "erro": str(e)}, status=500)


@method_decorator(csrf_exempt, name="dispatch")
class Token(View):
    # get token
    def post(self, request, *args, **kwargs):
        try:
            req = json.loads(request.body)
            username = req['username']
            password = req['password']
            user = auth.authenticate(
                request, username=username, password=password)
            if user is None:
                res = {"token": ""}
            else:
                token = jwt.encode({"username": username, "exp": datetime.datetime.utcnow(
                ) + datetime.timedelta(seconds=12*60*60)}, settings.SECRET_KEY, algorithm='HS256')
                res = {"token": token.decode('utf-8')}
            return JsonResponse(res, status=200)
        except Exception as e:
            traceback.print_exc()
            print("error", str(e))
            return JsonResponse({"message": "failed", "error": str(e)}, status=500)

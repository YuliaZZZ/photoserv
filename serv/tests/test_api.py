import functools

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from serv.models.photo import Photo

ALREADY_EXIST_FAILURES_BODY = {
    'username': ['A user with that username already exists.']
}

CREATE_METHOD_FAILURES_BODY = {
    "password": [
        "This field is required."
    ]
}

INVALID_FORMAT_PHOTO = {
    'file': 'Формат фото должен быть PNG (*.png), JPEG (*.jpg, *.jpeg)'}



def cases(cases):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args):
            for c in cases:
                try:
                    new_args = args + (c if isinstance(c, tuple) else (c,))
                    f(*new_args)
                except Exception:
                    raise Exception(f.__name__, c)

        return wrapper

    return decorator


class UserTests(TestCase):
    @cases([
        {'username': 'cat', 'password': 'gav'}
    ])
    def setUp(self, arguments) -> None:
        user2 = User.objects.create_user(
            username=arguments["username"],
            password=arguments["password"]
        )
        Token.objects.create(user=user2)

    def get_response(self, arguments):
        user = User.objects.get(username=arguments["user"]["username"])
        token = Token.objects.get(user=user)

        client = APIClient()
        client.force_authenticate(user=user, token=token)
        if arguments["method"] == "post":
            resp = client.post(arguments["url"], data=arguments["data"], format=arguments["format"])
        elif arguments["method"] == "get":
            resp = client.get(arguments["url"], data=arguments["data"], format=arguments["format"])
        else:
            resp = client.patch(arguments["url"], data=arguments["data"], format=arguments["format"])
        return resp

    @cases([
        {'url': '/api/v1/user/', 'password': 'testing', 'data': {'username': 'test', 'password': 'testing'}},
    ])
    def test_create_user(self, arguments=None):
        # регистрация пользователя
        resp = self.client.post(arguments["url"], data=arguments["data"], content_type='application/json')
        self.assertEqual(resp.status_code, 201)
        user = User.objects.get(username=arguments["data"]["username"])
        self.assertEqual(user.username, arguments["data"]["username"])

        # пользователь уже зарегистрирован
        resp2 = self.client.post(arguments["url"], data=arguments["data"], content_type='application/json')
        self.assertEqual(resp2.json(), ALREADY_EXIST_FAILURES_BODY)
        self.assertEqual(resp2.status_code, 400)

    @cases([
        {'url': '/api/v1/user/', 'data': {"username": "main"}, 'method': 'post', 'format': 'json'}
    ])
    def test_create_wrong_user(self, arguments=None):
        # отсутствуют обязательные аргументы
        resp = self.client.post(arguments["url"], data=arguments["data"], content_type='application/json')
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json(), CREATE_METHOD_FAILURES_BODY)

    @cases([
        {
            'url': '/api/v1/login/', 'user': {'username': 'cat', 'password': 'gav'},
            'method': 'post', 'format': 'json',
            'data': {'username': 'cat', 'password': 'gav'}
        }
    ])
    def test_login_user(self, arguments=None):
        # авторизация пользователя
        resp = self.get_response(arguments)
        self.assertEqual(resp.status_code, 200)


class PhotoTests(TestCase):
    @cases([
        {
            'user1': {'username': 'test', 'password': 'testing'}, 'user2': {'username': 'cat', 'password': 'gav'},
            'photo': {"title": "photo2", "file": "./serv/tests/fixtures/image2.jpg"}
        }
    ])
    def setUp(self, arguments=None) -> None:
        user = User.objects.create_user(
            username=arguments["user1"]["username"],
            password=arguments["user1"]["password"]
        )
        user2 = User.objects.create_user(
            username=arguments["user2"]["username"],
            password=arguments["user2"]["password"]
        )
        Token.objects.create(user=user)
        Token.objects.create(user=user2)

        Photo.objects.create(
            owner=user2,
            file=arguments["photo"]["file"],
            title=arguments["photo"]["title"]
        )

    @cases([
        {
            'user': {'username': 'test', 'password': 'testing'}, 'url': '/api/v1/photo/', 'method': 'post',
            'format': 'multipart',
            'data': {"title": "test", "file": "./serv/tests/fixtures/image1.jpg"}
        }
    ])
    def test_create_photo(self, arguments=None):
        user = User.objects.get(username=arguments["user"]["username"])

        with open(arguments["data"]["file"], "rb") as infile:
            photo = SimpleUploadedFile("image1.jpg", infile.read())
            arguments["data"].update({'file': photo})
        resp = UserTests().get_response(arguments)
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(
            resp.data["id"], Photo.objects.get(owner=user, title=arguments["data"]["title"]).id)

    @cases([
        {
            'user': {'username': 'test', 'password': 'testing'}, 'url': '/api/v1/photo/', 'method': 'post',
            'format': 'multipart',
            'data': {"title": "test3", "file": "./serv/tests/fixtures/image3.webp"}
        }
    ])
    def test_wrong_format_photo(self, arguments=None):
        with open(arguments["data"]["file"], "rb") as infile:
            photo = SimpleUploadedFile("image3.webp", infile.read())
            arguments["data"].update({'file': photo})
        resp = UserTests().get_response(arguments)
        self.assertEqual(resp.status_code, 400)

    @cases([
        {
            'user': {'username': 'cat', 'password': 'gav'}, 'url': '/api/v1/photo/', 'method': 'put',
            'format': 'multipart',
            'data': {"title": "photo2", "file": "./serv/tests/fixtures/image2.jpg"}
        }
    ])
    def test_update_photo(self, arguments=None):
        user = User.objects.get(username=arguments["user"]["username"])
        photo = Photo.objects.get(owner=user, title=arguments["data"]["title"])
        arguments["data"] = {"title": "enot", "view_counter": 50, "created_date": '2021-06-06'}
        arguments["url"] = f'/api/v1/photo/{photo.id}/'
        resp = UserTests().get_response(arguments)

        self.assertEqual(resp.status_code, 200)
        self.assertNotEqual(resp.data["view_counter"], 50)
        self.assertEqual(resp.data["title"], "enot")

    def test_get_photo_list(self):
        pass

    @cases([
        {
            'user': {'username': 'cat', 'password': 'gav'}, 'url': '/api/v1/photo/', 'method': 'get',
            'format': 'multipart', 'data': None
        }
    ])
    def test_get_photo(self, arguments=None):
        user = User.objects.get(username=arguments["user"]["username"])
        photo = Photo.objects.get(owner=user)

        arguments["url"] = f'{arguments["url"]}{photo.id}/'

        resp = UserTests().get_response(arguments)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["view_counter"], 1)
        self.assertEqual(Photo.objects.get(id=photo.id).view_counter, 1)

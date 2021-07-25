from .models import User
from .oauth import OauthKakao, OauthGoogle, OauthApple
from django.http import JsonResponse


def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            token = request.headers.get('Authorization')
            type, token = token.split(' ')

            if type == 'kakao':
                response = OauthKakao().get_access_token_info(token)
            elif type == 'google':
                response = OauthGoogle().get_access_token_info(token)
            elif type == 'apple':
                response = OauthApple().get_access_token_info(token)
            else:
                return JsonResponse({'message': 'INVALID_VALUE'}, status=400)  # INVALID_TYPE

            if response['code'] == 200:
                user = User.objects.get(social_id=response['id'])
                request.user = user
                return func(self, request, *args, **kwargs)
            else:
                return JsonResponse({'message': response['message']}, status=400)

        except User.DoesNotExist:
            return JsonResponse({'message': 'INVALID_USER'}, status=400)
        except ValueError:
            return JsonResponse({'message': 'INVALID_TOKEN'}, status=400)
    return wrapper
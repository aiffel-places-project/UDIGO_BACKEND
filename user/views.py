from django.http import JsonResponse
from rest_framework.views import APIView

from .models import User
from .utils import OauthKakao, OauthGoogle
from .serializers import UserSerializer


SOCIAL_TYPE = ['kakao', 'naver', 'google']


class LoginViewSet(APIView):
    """
    로그인 및 회원가입

    - headers
        - Authorization : social_type token
            - social_type 종류 : kakao, google
    """

    def post(self, request):
        try:
            token = request.headers.get('Authorization')
            social_type, token = token.split(' ')
            social_type = social_type.lower()

            if not token:
                return JsonResponse({"MESSAGE": "INVALID_TOKEN"}, status=400)

            user_data = {'social_type': SOCIAL_TYPE.index(social_type)}

            # 소셜별 토큰 유효성 체크 및 데이터 가져오기
            if social_type not in SOCIAL_TYPE:
                return JsonResponse({'message': 'INVALID_SOCIAL_TYPE'}, status=400)

            if social_type == 'kakao':
                kakao = OauthKakao()
                valid_result = kakao.get_access_token_info(access_token=token)
            elif social_type == 'google':
                google = OauthGoogle()
                valid_result = google.get_token_info(token=token)
            else:
                pass

            # 토큰 에러에 따른 예외처리
            if valid_result['code'] == 200:
                user_data['id'] = valid_result['id']
                user_data['nickname'] = valid_result['nickname']
            else:
                return JsonResponse({'MESSAGE': valid_result['message']}, status=400)

            # 로그인
            user = User.objects.filter(social_type=user_data['social_type'], social_id=user_data['id'])
            if user.exists():
                user = user[0]
                user = UserSerializer(user).data
                user['social_type'] = SOCIAL_TYPE[user['social_type']]
                return JsonResponse(user, status=200)

            # 회원가입
            else:
                serializer = UserSerializer(data=user_data)
                if serializer.is_valid():  # POST 데이타에 잘못된 데이타가 전달되었는지를 체크
                    user = serializer.save()
                    return JsonResponse(user.data, status=201)

        except ValueError:
            return JsonResponse({'message': 'INVALID_TOKEN'}, status=400)
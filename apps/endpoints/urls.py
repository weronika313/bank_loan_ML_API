# backend/server/apps/endpoints/urls.py file
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from apps import users
from apps.endpoints.views import MLAlgorithmViewSet
from apps.endpoints.views import MLAlgorithmStatusViewSet
from apps.endpoints.views import PredictView
from apps.endpoints.views import AlgorithmComparisonViewSet
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter(trailing_slash=False)
router.register(r"algorithms", MLAlgorithmViewSet, basename="algorithms")
router.register(
    r"algorithm_statuses", MLAlgorithmStatusViewSet, basename="algorithm_statuses"
)
router.register(r"algorithm_comparisons", AlgorithmComparisonViewSet, basename="algorithm_comparisons")

urlpatterns = [
    url(r"^", include(router.urls)),
    url(
        r"^(?P<algorithm_name>.+)/predict$", PredictView.as_view(), name="predict"
    ),
    url(r"^users/", include('apps.users.urls')),
    url(r"^rest-auth/", include('rest_auth.urls')),
    url(r"^rest-auth/registration/", include('rest_auth.registration.urls'))
]

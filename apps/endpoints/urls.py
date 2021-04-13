# backend/server/apps/endpoints/urls.py file
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

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
    url(r"^api/v1/", include(router.urls)),
    url(
        r"^api/v1/(?P<algorithm_name>.+)/predict$", PredictView.as_view(), name="predict"
    ),
    url('api-token-auth/', obtain_auth_token, name='api_token_auth')
]

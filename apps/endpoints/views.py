import joblib
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.exceptions import APIException

from apps.endpoints.models import Endpoint
from apps.endpoints.serializers import EndpointSerializer

from apps.endpoints.models import MachineLearningAlgorithm
from apps.endpoints.serializers import MLAlgorithmSerializer

from apps.endpoints.models import MLAlgorithmStatus
from apps.endpoints.serializers import MLAlgorithmStatusSerializer

from apps.endpoints.models import MLRequest
from apps.endpoints.serializers import MLRequestSerializer

from django.db import transaction
from apps.endpoints.models import AlgorithmsComparison
from apps.endpoints.serializers import AlgorithmComparisonSerializer

import json
from rest_framework import views, status
from rest_framework.response import Response
from djangoProject.wsgi import registry

from rest_framework.permissions import IsAuthenticated


class EndpointViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    serializer_class = EndpointSerializer
    queryset = Endpoint.objects.all()


class MLAlgorithmViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    serializer_class = MLAlgorithmSerializer
    queryset = MachineLearningAlgorithm.objects.all()


def deactivate_old_statuses(instance):
    old_statuses = MLAlgorithmStatus.objects.filter(
        parent_mlalgorithm=instance.parent_mlalgorithm,
        created_at__lt=instance.created_at,
        active=True,
    )
    for i in range(len(old_statuses)):
        old_statuses[i].active = False
    MLAlgorithmStatus.objects.bulk_update(old_statuses, ["active"])


class MLAlgorithmStatusViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
):

    serializer_class = MLAlgorithmStatusSerializer
    queryset = MLAlgorithmStatus.objects.all()

    def perform_create(self, serializer):
        try:
            with transaction.atomic():
                instance = serializer.save(active=True)
                deactivate_old_statuses(instance)

        except Exception as e:
            raise APIException(str(e))


class MLRequestViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
    mixins.UpdateModelMixin,
):
    serializer_class = MLRequestSerializer
    queryset = MLRequest.objects.all()


class PredictView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, algorithm_name):

        algorithm_status = self.request.query_params.get("status", "production")
        algorithm_version = self.request.query_params.get("version")

        algs = MachineLearningAlgorithm.objects.filter(
            name=algorithm_name,
            status__status=algorithm_status,
            status__active=True,
        )

        if algorithm_version is not None:
            algs = algs.filter(version=algorithm_version)

        if len(algs) == 0:
            return Response(
                {"status": "Error", "message": "ML algorithm is not available"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if len(algs) != 1:
            return Response(
                {
                    "status": "Error",
                    "message": "ML algorithm selection is ambiguous. Please specify algorithm version.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        alg_index = 0

        algorithm_object = registry.endpoints[algs[alg_index].id]
        prediction = algorithm_object.compute_prediction(request.data)

        label = prediction["label"] if "label" in prediction else "error"
        ml_request = MLRequest(
            input_data=json.dumps(request.data),
            full_response=prediction,
            response=label,
            feedback="",
            parent_algorithm=algs[alg_index],
        )
        ml_request.save()

        prediction["request_id"] = ml_request.id

        return Response(prediction)


class AlgorithmComparisonViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet,
    mixins.CreateModelMixin, mixins.UpdateModelMixin
):
    permission_classes = (IsAuthenticated,)
    serializer_class = AlgorithmComparisonSerializer
    queryset = AlgorithmsComparison.objects.all()

    def perform_create(self, serializer):
        try:
            alg_1 = MachineLearningAlgorithm.objects.filter(
                name=serializer.validated_data['parent_algorithm_1'].name,
                version=serializer.validated_data['parent_algorithm_1'].version,
                status__active=True,
            )

            alg_2 = MachineLearningAlgorithm.objects.filter(
                name=serializer.validated_data['parent_algorithm_2'].name,
                version=serializer.validated_data['parent_algorithm_2'].version,
                status__active=True,
            )
            algorithm_object_1 = registry.endpoints[alg_1[0].id]
            algorithm_object_2 = registry.endpoints[alg_2[0].id]

            x_test = joblib.load("research/X_test.joblib")
            y_test = joblib.load("research/y_test.joblib")

            accuracy_1 = algorithm_object_1.get_accuracy(x_test, y_test)
            accuracy_2 = algorithm_object_2.get_accuracy(x_test, y_test)


            summary = "Algorithm #1 accuracy: {}, Algorithm #2 accuracy: {}".format(accuracy_1, accuracy_2)
            serializer.save(summary=summary)

        except Exception as e:
            raise APIException(str(e))

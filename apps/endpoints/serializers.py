from rest_framework import serializers
from apps.endpoints.models import Endpoint
from apps.endpoints.models import MachineLearningAlgorithm
from apps.endpoints.models import MLAlgorithmStatus
from apps.endpoints.models import MLRequest
from apps.endpoints.models import AlgorithmsComparison


class EndpointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endpoint
        read_only_fields = ("id", "name", "created_at")
        fields = read_only_fields


class MLAlgorithmSerializer(serializers.ModelSerializer):
    current_status = serializers.SerializerMethodField(read_only=True)

    def get_current_status(self, algorithm):
        return (
            MLAlgorithmStatus.objects.filter(parent_algorithm=algorithm)
                .latest("created_at")
                .status
        )

    class Meta:
        model = MachineLearningAlgorithm
        read_only_fields = (
            "id",
            "name",
            "description",
            "code",
            "version",
            "created_at",
            "parent_endpoint",
            "current_status",
        )
        fields = read_only_fields


class MLAlgorithmStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLAlgorithmStatus
        read_only_fields = ("id", "active")
        fields = ("id", "active", "status", "created_at", "parent_algorithm")


class MLRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLRequest
        read_only_fields = (
            "id",
            "input_data",
            "full_response",
            "response",
            "created_at",
            "parent_algorithm",
        )
        fields = (
            "id",
            "input_data",
            "full_response",
            "response",
            "feedback",
            "created_at",
            "parent_algorithm",
        )


class AlgorithmComparisonSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlgorithmsComparison
        read_only_fields = (
            "id",
            "created_at",
            "summary",
        )
        fields = (
            "id",
            "title",
            "created_at",
            "summary",
            "parent_algorithm_1",
            "parent_algorithm_2",
        )

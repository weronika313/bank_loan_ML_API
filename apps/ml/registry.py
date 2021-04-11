from apps.endpoints.models import Endpoint
from apps.endpoints.models import MachineLearningAlgorithm
from apps.endpoints.models import MLAlgorithmStatus


class MLRegistry:
    def __init__(self):
        self.endpoints = {}

    def add_algorithm(
        self,
        endpoint_name,
        algorithm_object,
        algorithm_name,
        algorithm_status,
        algorithm_version,
        algorithm_description,
        algorithm_code,
    ):

        endpoint, _ = Endpoint.objects.get_or_create(name=endpoint_name)

        (
            database_object,
            algorithm_created,
        ) = MachineLearningAlgorithm.objects.get_or_create(
            name=algorithm_name,
            description=algorithm_description,
            code=algorithm_code,
            version=algorithm_version,
            parent_endpoint=endpoint,
        )
        if algorithm_created:
            status = MLAlgorithmStatus(
                status=algorithm_status, parent_algorithm=database_object, active=True
            )
            status.save()

        self.endpoints[database_object.id] = algorithm_object

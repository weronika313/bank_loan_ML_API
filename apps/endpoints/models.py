from django.db import models


class Endpoint(models.Model):
    name = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)


class MachineLearningAlgorithm(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=1000)
    code = models.CharField(max_length=50000)
    version = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    parent_endpoint = models.ForeignKey(Endpoint, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + ' ' + self.version

class MLAlgorithmStatus(models.Model):
    status = models.CharField(max_length=128)
    active = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    parent_algorithm = models.ForeignKey(
        MachineLearningAlgorithm, on_delete=models.CASCADE, related_name="status"
    )

    def __str__(self):
        return self.parent_algorithm.name + ' ' + self.status


class MLRequest(models.Model):
    input_data = models.CharField(max_length=10000)
    full_response = models.CharField(max_length=10000)
    response = models.CharField(max_length=10000)
    feedback = models.CharField(max_length=10000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    parent_algorithm = models.ForeignKey(
        MachineLearningAlgorithm, on_delete=models.CASCADE
    )

class AlgorithmsComparison(models.Model):
    title = models.CharField(max_length=10000)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    summary = models.CharField(max_length=10000, blank=True, null=True)

    parent_algorithm_1 = models.ForeignKey(MachineLearningAlgorithm, on_delete=models.CASCADE, related_name="parent_algorithm_1")
    parent_algorithm_2 = models.ForeignKey(MachineLearningAlgorithm, on_delete=models.CASCADE, related_name="parent_algorithm_2")
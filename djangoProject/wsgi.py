"""
WSGI config for djangoProject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')

application = get_wsgi_application()


import inspect
from apps.ml.registry import MLRegistry
from apps.ml.income_classifier.random_forest import RandomForestClassifier

try:
    registry = MLRegistry() # create ML registry
    # Random Forest classifier
    rf = RandomForestClassifier()
    # add to ML registry
    registry.add_algorithm(endpoint_name="random_forest_classifier_alg",
                            algorithm_object=rf,
                            algorithm_name="random forest",
                            algorithm_status="production",
                            algorithm_version="v4",
                            algorithm_description="A random forest is a meta estimator that fits a number of decision tree classifiers " \
                                "on various sub-samples of the dataset and uses averaging to improve the predictive " \
                                "accuracy and control over-fitting. ",
                            algorithm_code=inspect.getsource(RandomForestClassifier))

except Exception as e:
    print("Exception while loading the algorithms to the registry,", str(e))

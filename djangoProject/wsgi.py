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
from apps.ml.income_classifier.extra_trees import ExtraTreesClassifier
from apps.ml.income_classifier.logistic_regression import LogisticRegressionClassifier



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

    # Extra Trees classifier
    et = ExtraTreesClassifier()
    # add to ML registry
    registry.add_algorithm(endpoint_name="income_classifier",
                           algorithm_object=et,
                           algorithm_name="extra trees",
                           algorithm_status="testing",
                           algorithm_version="0.0.1",
                           algorithm_description="Extremely Randomized Trees Classifier(Extra Trees Classifier) is a "
                                                 "type of ensemble learning technique which aggregates the results of "
                                                 "multiple de-correlated decision trees collected in a “forest” to "
                                                 "output it’s classification result. In concept, it is very similar "
                                                 "to a Random Forest Classifier and only differs from it in the "
                                                 "manner of construction of the decision trees in the forest.",
                           algorithm_code=inspect.getsource(RandomForestClassifier))


    # Extra Trees classifier
    lr = LogisticRegressionClassifier()
    # add to ML registry
    registry.add_algorithm(endpoint_name="income_classifier",
                            algorithm_object=lr,
                            algorithm_name="logistic regression",
                            algorithm_status="testing",
                            algorithm_version="0.0.1",
                            algorithm_description="Logistic Regression is a Machine Learning algorithm which is used "
                                                  "for the classification problems, it is a predictive analysis "
                                                  "algorithm and based on the concept of probability.",
                            algorithm_code=inspect.getsource(RandomForestClassifier))

except Exception as e:
    print("Exception while loading the algorithms to the registry,", str(e))

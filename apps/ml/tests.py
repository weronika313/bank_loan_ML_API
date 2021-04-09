import inspect

from django.test import TestCase

from apps.ml.income_classifier.random_forest import RandomForestClassifier
from apps.ml.income_classifier.extra_trees import ExtraTreesClassifier
from apps.ml.income_classifier.logistic_regression import LogisticRegressionClassifier
from apps.ml.income_classifier.naive_bayes import NaiveBayesClassifier
from apps.ml.income_classifier.support_vector_machine import SupportVectorMachineClassifier
from apps.ml.income_classifier.voting_classifier import VotingClassifier



from apps.ml.registry import MLRegistry


class MLTests(TestCase):
    def test_rf_algorithm(self):
        input_data = {
            "Gender": "Male",
            "Married": "Yes",
            "Dependents": 2,
            "Education": "Graduate",
            "Self_Employed": "Yes",
            "ApplicantIncome": 5849,
            "CoapplicantIncome": 6000,
            "LoanAmount": 120,
            "Loan_Amount_Term": 360,
            "Credit_History": 1,
            "Property_Area": "Urban",
        }
        my_alg = RandomForestClassifier()
        response = my_alg.compute_prediction(input_data)
        self.assertEqual("OK", response["status"])
        self.assertTrue("label" in response)
        self.assertEqual("Approved", response["label"])

    def test_et_algorithm(self):
        input_data = {
            "Gender": "Male",
            "Married": "Yes",
            "Dependents": 2,
            "Education": "Graduate",
            "Self_Employed": "Yes",
            "ApplicantIncome": 5849,
            "CoapplicantIncome": 6000,
            "LoanAmount": 120,
            "Loan_Amount_Term": 360,
            "Credit_History": 1,
            "Property_Area": "Urban",
        }
        my_alg = ExtraTreesClassifier()
        response = my_alg.compute_prediction(input_data)
        self.assertEqual("OK", response["status"])
        self.assertTrue("label" in response)
        self.assertEqual("Approved", response["label"])

    def test_lr_algorithm(self):
        input_data = {
            "Gender": "Male",
            "Married": "Yes",
            "Dependents": 2,
            "Education": "Graduate",
            "Self_Employed": "Yes",
            "ApplicantIncome": 5849,
            "CoapplicantIncome": 6000,
            "LoanAmount": 120,
            "Loan_Amount_Term": 360,
            "Credit_History": 1,
            "Property_Area": "Urban",
        }
        my_alg = LogisticRegressionClassifier()
        response = my_alg.compute_prediction(input_data)
        self.assertEqual("OK", response["status"])
        self.assertTrue("label" in response)
        self.assertEqual("Approved", response["label"])

    def test_evc_algorithm(self):
        input_data = {
            "Gender": "Male",
            "Married": "Yes",
            "Dependents": 2,
            "Education": "Graduate",
            "Self_Employed": "Yes",
            "ApplicantIncome": 5849,
            "CoapplicantIncome": 6000,
            "LoanAmount": 120,
            "Loan_Amount_Term": 360,
            "Credit_History": 1,
            "Property_Area": "Urban",
        }
        my_alg = VotingClassifier()
        response = my_alg.compute_prediction(input_data)
        self.assertEqual("OK", response["status"])
        self.assertTrue("label" in response)
        self.assertEqual("Approved", response["label"])

    def test_nb_algorithm(self):
        input_data = {
            "Gender": "Male",
            "Married": "Yes",
            "Dependents": 2,
            "Education": "Graduate",
            "Self_Employed": "Yes",
            "ApplicantIncome": 5849,
            "CoapplicantIncome": 6000,
            "LoanAmount": 120,
            "Loan_Amount_Term": 360,
            "Credit_History": 1,
            "Property_Area": "Urban",
        }
        my_alg = NaiveBayesClassifier()
        response = my_alg.compute_prediction(input_data)
        self.assertEqual("OK", response["status"])
        self.assertTrue("label" in response)
        self.assertEqual("Approved", response["label"])



    def test_registry(self):
        registry = MLRegistry()
        self.assertEqual(len(registry.endpoints), 0)
        endpoint_name = "income_classifier"
        algorithm_object = RandomForestClassifier()
        algorithm_name = "random forest"
        algorithm_status = "production"
        algorithm_version = "v1"
        algorithm_description = (
            "A random forest is a meta estimator that fits a number of decision tree classifiers "
            "on various sub-samples of the dataset and uses averaging to improve the predictive "
            "accuracy and control over-fitting. "
        )
        algorithm_code = inspect.getsource(RandomForestClassifier)
        # add to registry
        registry.add_algorithm(
            endpoint_name,
            algorithm_object,
            algorithm_name,
            algorithm_status,
            algorithm_version,
            algorithm_description,
            algorithm_code,
        )
        # there should be one endpoint available
        self.assertEqual(len(registry.endpoints), 1)

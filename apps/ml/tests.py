from django.test import TestCase

from apps.ml.income_classifier.random_forest import RandomForestClassifier

class MLTests(TestCase):
    def test_rf_algorithm(self):
        input_data = {
            "Gender": 'Male',
            "Married": "Yes",
            "Dependents": 2,
            "Education": "Graduate",
            "Self_Employed": 'Yes',
            "ApplicantIncome": 5849,
            "CoapplicantIncome": 6000,
            "LoanAmount": 120,
            "Loan_Amount_Term": 360,
            "Credit_History": 1,
            "Property_Area": "Urban"
        }
        my_alg = RandomForestClassifier()
        response = my_alg.compute_prediction(input_data)
        self.assertEqual('OK', response['status'])
        self.assertTrue('label' in response)
        self.assertEqual('Approved', response['label'])
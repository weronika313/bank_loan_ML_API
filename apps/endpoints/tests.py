from django.test import TestCase
from rest_framework.test import APIClient


class EndpointTests(TestCase):
    def test_prediction_view(self):
        client = APIClient()
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
            "Property_Area": "Urban"
        }

        classifier_url = "/api/v1/random_forest_classifier_alg/predict"
        response = client.post(classifier_url, input_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["label"], "Approved")
        self.assertTrue("request_id" in response.data)
        self.assertTrue("status" in response.data)
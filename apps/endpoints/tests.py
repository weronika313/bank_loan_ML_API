from django.test import TestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


class EndpointTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
        self.token = Token.objects.create(user=self.user)

    def test_prediction_view(self):
        self.client.force_login(user=self.user)
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

        classifier_url = "/api/v1/random_forest/predict"
        response = self.client.post(classifier_url, data=input_data, format='json', HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["label"], "Approved")
        self.assertTrue("request_id" in response.data)
        self.assertTrue("status" in response.data)

    def test_comparison_view(self):
        self.client.force_login(user=self.user)
        input_data = {
            "title": "test comparison view",
            "parent_algorithm_1": 1,
            "parent_algorithm_2": 2

        }

        comparison_url = "/api/v1/algorithm_comparisons"
        response = self.client.post(comparison_url, data=input_data, format='json', HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["title"], "test comparison view")
        self.assertEqual(response.data["parent_algorithm_1"], 1)
        self.assertEqual(response.data["parent_algorithm_2"], 2)

    def test_authentication_failed(self):
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

        url = "/api/v1/random_forest/predict"
        response = self.client.post(url, data=input_data, format='json')
        self.assertEqual(response.status_code, 403)


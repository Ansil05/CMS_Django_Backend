

# Create your tests here.
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from datetime import date, timedelta
from .models import Role, Specialization, Staff, Doctor


# class RoleAPITest(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.role = Role.objects.create(RoleName="Doctor", Description="Medical Doctor")

#     def test_create_role(self):
#         response = self.client.post("/api/admin/roles/", {"RoleName": "Nurse", "Description": "Nursing staff"}, format="json")
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#     def test_get_roles(self):
#         response = self.client.get("/api/admin/roles/")
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertGreaterEqual(len(response.json()), 1)

#     def test_invalid_role_name(self):
#         response = self.client.post("/api/admin/roles/", {"RoleName": "Dr"}, format="json")
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# class SpecializationAPITest(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.spec = Specialization.objects.create(SpecializationName="Cardiology", Description="Heart Specialist")

#     def test_create_specialization(self):
#         response = self.client.post("/api/admin/specializations/", {"SpecializationName": "Neurology"}, format="json")
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#     def test_invalid_specialization_name(self):
#         response = self.client.post("/api/admin/specializations/", {"SpecializationName": "Ne"}, format="json")
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# class StaffAPITest(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.role = Role.objects.create(RoleName="Doctor")
#         self.staff_data = {
#             "FirstName": "John",
#             "LastName": "Doe",
#             "DOB": str(date.today() - timedelta(days=365*25)),  # 25 years old
#             "Gender": "Male",
#             "Role": { "RoleName": self.role.RoleName},
#             "Email": "johndoe@example.com",
#             "PhoneNumber": "9876543210",
#             "Address": "123 Main Street"
#         }

#     def test_create_staff(self):
#         response = self.client.post("/api/admin/staffs/", self.staff_data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#     def test_invalid_age(self):
#         self.staff_data["DOB"] = str(date.today() - timedelta(days=365*15))  # 15 years old
#         response = self.client.post("/api/admin/staffs/", self.staff_data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#     def test_invalid_phone(self):
#         self.staff_data["PhoneNumber"] = "1234"
#         response = self.client.post("/api/admin/staffs/", self.staff_data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# class DoctorAPITest(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.role = Role.objects.create(RoleName="Doctor")
#         self.spec = Specialization.objects.create(SpecializationName="Cardiology")
#         self.staff = Staff.objects.create(
#             FirstName="Alice",
#             LastName="Smith",
#             DOB=date.today() - timedelta(days=365*30),
#             Gender="Female",
#             Role=self.role,
#             Email="alice@example.com",
#             PhoneNumber="9876543211",
#             Address="456 Main Street"
#         )
#         self.doctor = Doctor.objects.create(
#             Staff=self.staff,
#             Specialization=self.spec,
#             ConsultationFee=500,
#             availability="Available",
#             YearsOfExperience=5
#         )

#     def test_create_doctor(self):
#         new_staff = Staff.objects.create(
#             FirstName="Bob",
#             LastName="Brown",
#             DOB=date.today() - timedelta(days=365*40),
#             Gender="Male",
#             Role=self.role,
#             Email="bob@example.com",
#             PhoneNumber="9876543212",
#             Address="789 Main Street"
#         )
#         response = self.client.post(
#             "/api/admin/doctors/",
#             {
#                 "Staff": {"FirstName": "Bob", "LastName": "Brown", "DOB": str(new_staff.DOB),
#                           "Gender": "Male", "Role": {"RoleId": self.role.RoleId, "RoleName": "Doctor"},
#                           "Email": "bob@example.com", "PhoneNumber": "9876543212", "Address": "789 Main Street"},
#                 "Specialization": {"SpecializationId": self.spec.SpecializationId, "SpecializationName": "Cardiology"},
#                 "ConsultationFee": 1000,
#                 "availability": "Available",
#                 "YearsOfExperience": 10,
#             },
#             format="json",
#         )
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#     def test_doctor_must_have_doctor_role(self):
#         wrong_role = Role.objects.create(RoleName="Receptionist")
#         staff_wrong = Staff.objects.create(
#             FirstName="Tom",
#             LastName="Lee",
#             DOB=date.today() - timedelta(days=365*28),
#             Gender="Male",
#             Role=wrong_role,
#             Email="tom@example.com",
#             PhoneNumber="9876543213",
#             Address="123 Elm Street"
#         )
#         response = self.client.post(
#             "/api/admin/doctors/",
#             {
#                 "Staff": {"FirstName": staff_wrong.FirstName, "LastName": staff_wrong.LastName,
#                           "DOB": str(staff_wrong.DOB), "Gender": "Male",
#                           "Role": {"RoleId": wrong_role.RoleId, "RoleName": "Receptionist"},
#                           "Email": "tom@example.com", "PhoneNumber": "9876543213", "Address": "123 Elm Street"},
#                 "Specialization": {"SpecializationId": self.spec.SpecializationId, "SpecializationName": "Cardiology"},
#                 "ConsultationFee": 500,
#                 "availability": "Available",
#                 "YearsOfExperience": 3,
#             },
#             format="json",
#         )
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#     def test_filter_doctors_by_specialization(self):
#         response = self.client.get(f"/api/admin/doctors/?specialization={self.spec.SpecializationId}")
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertGreaterEqual(len(response.json()), 1)

#     def test_filter_doctors_by_availability(self):
#         response = self.client.get("/api/admin/doctors/?availability=Available")
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertGreaterEqual(len(response.json()), 1)

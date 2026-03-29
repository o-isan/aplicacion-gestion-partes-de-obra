from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import (
    Part, Project, Employee, Canal, Ground, 
    Machineries, ExcessHoursReasons, PartMachinery, 
    ExcessHoursJustification
)
import datetime

class BaseTestCase:
    """Base setup for both API and Template view tests."""
    def setUp(self):
        self.project = Project.objects.create(name="Test Project", total_activities_min=60)
        self.employee = Employee.objects.create(name="John Doe", role="Supervisor")
        self.canal = Canal.objects.create(code="C1", name="Canal 1")
        self.ground = Ground.objects.create(name="Rocky")
        self.machinery = Machineries.objects.create(name="Excavator")
        self.reason = ExcessHoursReasons.objects.create(name="Urgent work")
        
        self.part_data = {
            'project': self.project,
            'part_number': 'P-001',
            'part_date': datetime.date.today(),
            'canal': self.canal,
            'responsible_employee': self.employee,
            'ground': self.ground,
            'excess_hours_justified': False,
            'status': 'pending'
        }
        self.part = Part.objects.create(**self.part_data)

class PartAPITestCase(BaseTestCase, APITestCase):
    def test_list_parts(self):
        url = reverse('part-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # response.data is a dict because of pagination: {'count': 1, 'next': None, 'previous': None, 'results': [...]}
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_part(self):
        url = reverse('part-list')
        data = {
            'project': self.project.id,
            'part_number': 'P-002',
            'part_date': str(datetime.date.today()),
            'canal': self.canal.id,
            'responsible_employee': self.employee.id,
            'ground': self.ground.id,
            'excess_hours_justified': True,
            'machinery_ids': [self.machinery.id],
            'justification': {
                'reason_id': self.reason.id,
                'justification_text': 'Working overtime for deadline'
            }
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Part.objects.count(), 2)
        
        # Check related data
        part = Part.objects.get(part_number='P-002')
        self.assertTrue(part.excess_hours_justified)
        self.assertEqual(part.partmachinery_set.count(), 1)
        self.assertEqual(part.excesshoursjustification_set.count(), 1)

    def test_update_part(self):
        url = reverse('part-detail', args=[self.part.id])
        data = {
            'part_number': 'P-001-UPDATED',
            'project': self.project.id,
            'part_date': str(datetime.date.today()),
            'canal': self.canal.id,
            'responsible_employee': self.employee.id,
            'ground': self.ground.id,
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.part.refresh_from_db()
        self.assertEqual(self.part.part_number, 'P-001-UPDATED')

    def test_delete_part_soft(self):
        url = reverse('part-detail', args=[self.part.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.part.refresh_from_db()
        self.assertTrue(self.part.is_deleted)
        self.assertEqual(Part.active_objects.count(), 0)

class PartTemplateViewTestCase(BaseTestCase, TestCase):
    def setUp(self):
        super().setUp()
        self.client = Client()

    def test_list_view(self):
        url = reverse('part_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.part.part_number)

    def test_create_view(self):
        url = reverse('part_add')
        data = {
            'project': self.project.id,
            'part_number': 'P-003',
            'part_date': str(datetime.date.today()),
            'canal': self.canal.id,
            'responsible_employee': self.employee.id,
            'ground': self.ground.id,
            'machinery_ids': [self.machinery.id],
            # Note: PartForm handles the nested logic, so we send what it expects
            'is_deleted': False,
            'status': 'pending'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302) # Redirect after success
        self.assertEqual(Part.objects.filter(part_number='P-003').count(), 1)

    def test_update_view(self):
        url = reverse('part_edit', args=[self.part.id])
        data = {
            'project': self.project.id,
            'part_number': 'P-001-EDITED',
            'part_date': str(datetime.date.today()),
            'canal': self.canal.id,
            'responsible_employee': self.employee.id,
            'ground': self.ground.id,
            'status': 'pending'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.part.refresh_from_db()
        self.assertEqual(self.part.part_number, 'P-001-EDITED')

    def test_delete_view_post(self):
        url = reverse('part_delete', args=[self.part.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.part.refresh_from_db()
        self.assertTrue(self.part.is_deleted)

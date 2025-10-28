from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db import transaction
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from decimal import Decimal
from datetime import date, timedelta

from .models import Consultation, Prescription, LabPrescription
from labtechbackendapi.models import Labtest
from .serializers import (
    ConsultationSerializer,
    PrescriptionSerializer,
    LabPrescriptionSerializer,
    LabTestSerializer,
)

# Import pharmacy models and serializers
from pharmasistbackendapi.models import Bill, Medicine
from pharmasistbackendapi.serializers import BillSerializer


class ConsultationViewSet(viewsets.ModelViewSet):
    queryset = Consultation.objects.all()
    serializer_class = ConsultationSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def create_pharmacy_bill(self, request, pk=None):
        """
        Create a pharmacy bill from consultation prescriptions
        """
        try:
            consultation = self.get_object()
            prescriptions = consultation.prescriptions.all()
            
            if not prescriptions.exists():
                return Response(
                    {'error': 'No prescriptions found for this consultation'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            bill_items = []
            total_amount = Decimal('0.00')
            warnings = []
            
            print(f"\n=== Processing {prescriptions.count()} prescriptions ===")
            
            for prescription in prescriptions:
                try:
                    # Get medicine string from prescription
                    medicine_str = str(prescription.medicine).strip()
                    print(f"Raw prescription: '{medicine_str}'")
                    
                    if not medicine_str:
                        warnings.append("Empty medicine name")
                        continue
                    
                    # Extract medicine name from format: "Paracetamol (MED4844A3CD) - Paraman"
                    medicine_name = medicine_str
                    if '(' in medicine_str:
                        medicine_name = medicine_str.split('(')[0].strip()
                        print(f"Extracted name: '{medicine_name}'")
                    
                    # Try to find medicine by name
                    medicine = Medicine.objects.filter(name__iexact=medicine_name).first()
                    
                    if not medicine:
                        # Try partial match
                        medicine = Medicine.objects.filter(name__icontains=medicine_name).first()
                    
                    if not medicine:
                        # Try by code
                        medicine = Medicine.objects.filter(med_code__iexact=medicine_name).first()
                    
                    if medicine:
                        print(f"✅ Found: {medicine.name} (Stock: {medicine.stock}, Rate: ₹{medicine.unit_rate})")
                    else:
                        available = list(Medicine.objects.values_list('name', flat=True))
                        print(f"❌ Not found. Available: {available}")
                        warnings.append(f"Medicine '{medicine_name}' not found in inventory")
                        continue
                    
                    # Quantity default to 1
                    quantity = 1
                    
                    # Check stock
                    if medicine.stock < quantity:
                        warnings.append(
                            f"Insufficient stock for {medicine.name}. "
                            f"Available: {medicine.stock}, Required: {quantity}"
                        )
                        continue
                    
                    # Calculate cost
                    item_cost = medicine.unit_rate * Decimal(str(quantity))
                    total_amount += item_cost
                    
                    bill_items.append({
                        'medicine': medicine.name,
                        'code': medicine.med_code,
                        'quantity': quantity,
                        'rate': float(medicine.unit_rate),
                        'total': float(item_cost),
                        'dosage': prescription.dosage if hasattr(prescription, 'dosage') else 'As directed'
                    })
                    
                    print(f"✅ Added: {medicine.name} x{quantity} = ₹{float(item_cost)}")
                    
                except Exception as e:
                    print(f"❌ Error: {str(e)}")
                    import traceback
                    traceback.print_exc()
                    warnings.append(f"Error: {str(e)}")
                    continue
            
            print(f"\n=== Summary: {len(bill_items)} items, Total: ₹{float(total_amount)} ===\n")
            
            if not bill_items:
                return Response({
                    'error': 'Could not process any medicines',
                    'details': warnings
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Get patient
            patient = None
            if hasattr(consultation, 'appointment') and consultation.appointment:
                patient = consultation.appointment.patient
            
            if not patient:
                return Response(
                    {'error': 'Patient information not found'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Create bill notes
            bill_notes = f"📋 Consultation #{consultation.consultation_id}\n"
            bill_notes += f"🩺 Diagnosis: {consultation.diagnosis}\n\n"
            bill_notes += "💊 Prescribed Medicines:\n"
            for item in bill_items:
                bill_notes += f"• {item['medicine']} ({item['code']}) x{item['quantity']} @ ₹{item['rate']} = ₹{item['total']}\n"
            
            if warnings:
                bill_notes += f"\n⚠️ Warnings:\n" + "\n".join([f"• {w}" for w in warnings])
            
            # Create bill with transaction
            with transaction.atomic():
                bill = Bill.objects.create(
                    bill_type='MEDICINE',
                    patient_id=patient,
                    ref_id=consultation.consultation_id,
                    total_amount=total_amount,
                    paid_amount=Decimal('0.00'),
                    status='PENDING',
                    due_date=date.today() + timedelta(days=7),
                    notes=bill_notes,
                    created_by=request.user
                )
                
                # Reduce stock
                for item in bill_items:
                    med = Medicine.objects.get(med_code=item['code'])
                    med.stock -= item['quantity']
                    med.save()
                    print(f"Stock reduced: {med.name} → {med.stock}")
            
            print(f"✅ Bill {bill.serial_number} created successfully!\n")
            
            return Response({
                'success': True,
                'message': 'Bill created successfully!',
                'bill': {
                    'bill_id': bill.bill_id,
                    'serial_number': bill.serial_number,
                    'total_amount': float(bill.total_amount),
                    'status': bill.status,
                    'patient_name': f"{patient.first_name} {patient.last_name}"
                },
                'items': bill_items,
                'warnings': warnings if warnings else None
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({
                'error': f'Failed to create bill: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def with_prescriptions(self, request):
        """Get consultations that have prescriptions"""
        consultations_with_rx = self.get_queryset().filter(
            prescriptions__isnull=False
        ).distinct()
        
        serializer = self.get_serializer(consultations_with_rx, many=True)
        return Response({
            'count': consultations_with_rx.count(),
            'results': serializer.data
        })


class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated]


class LabPrescriptionViewSet(viewsets.ModelViewSet):
    queryset = LabPrescription.objects.all()
    serializer_class = LabPrescriptionSerializer
    permission_classes = [IsAuthenticated]


class LabTestViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Labtest.objects.all()
    serializer_class = LabTestSerializer
    permission_classes = [IsAuthenticated]

# pharmacy/views.py
from rest_framework import viewsets, status, filters, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Sum, Count, Avg
from django.db import transaction
from django.utils import timezone
from datetime import date, timedelta
from decimal import Decimal
import logging

from .models import Medicine, Bill
from .serializers import MedicineSerializer, BillSerializer

# Setup logging
logger = logging.getLogger(__name__)

class BasePharmacyPermission(permissions.BasePermission):
    """
    Custom base permission for pharmacy operations with role-based access
    """
    message = "You do not have permission to perform this action."

    def has_permission(self, request, view):
        """Check if user has permission for the view"""
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Allow all authenticated users for safe methods (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # For write operations (POST, PUT, DELETE):
        # Allow if user is staff
        if request.user.is_staff or request.user.is_superuser:
            return True
            
        # Check if user has role and convert to uppercase for comparison
        if hasattr(request.user, 'role'):
            user_role = str(request.user.role).upper()  # ← Convert to uppercase
            return user_role in ['PHARMACIST', 'ADMIN', 'DOCTOR']
        
        # Fallback: deny access
        return False

    def has_object_permission(self, request, view, obj):
        """Check if user has permission for specific object"""
        # Safe methods allowed for all authenticated users
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Staff/superuser can do anything
        if request.user.is_staff or request.user.is_superuser:
            return True
            
        # Only allow modification by staff or object creator
        if hasattr(obj, 'created_by'):
            return request.user.is_staff or obj.created_by == request.user
            
        return request.user.is_staff


class MedicineViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Medicine model with comprehensive CRUD operations
    """
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    # Filtering and search configuration
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'manufacturer': ['exact', 'icontains'],
        'med_code': ['exact', 'icontains'],
        'unit_rate': ['exact', 'gte', 'lte'],
        'stock': ['exact', 'gte', 'lte'],
        'expiry_date': ['exact', 'gte', 'lte'],
        'created_at': ['exact', 'gte', 'lte']
    }
    search_fields = ['name', 'manufacturer', 'serial_number', 'med_code']
    ordering_fields = ['unit_rate', 'stock', 'expiry_date', 'created_at', 'name']
    ordering = ['-created_at']

    def get_permissions(self):
        """
         Allow all authenticated users for all actions (development mode)
        """
        permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    def get_queryset(self):
        """
        Optionally filter queryset based on user role and request parameters
        """
        queryset = Medicine.objects.all()
        
        # Filter by availability
        available_only = self.request.query_params.get('available_only', None)
        if available_only and available_only.lower() == 'true':
            queryset = queryset.filter(stock__gt=0)
            
        # Filter by expiry status
        exclude_expired = self.request.query_params.get('exclude_expired', None)
        if exclude_expired and exclude_expired.lower() == 'true':
            queryset = queryset.filter(expiry_date__gt=date.today())
            
        return queryset

    def perform_create(self, serializer):
        """
        Custom creation logic with logging and validation
        """
        try:
            medicine = serializer.save()
            logger.info(f"Medicine created: {medicine.serial_number} by user {self.request.user.id}")
            
            # Additional business logic after creation
            if medicine.stock < 10:
                logger.warning(f"Low stock alert: Medicine {medicine.serial_number} has only {medicine.stock} units")
                
        except Exception as e:
            logger.error(f"Failed to create medicine: {str(e)} by user {self.request.user.id}")
            raise ValidationError(f"Failed to create medicine: {str(e)}")

    def perform_update(self, serializer):
        """
        Custom update logic with audit logging
        """
        original_instance = self.get_object()
        original_stock = original_instance.stock
        
        try:
            medicine = serializer.save()
            logger.info(f"Medicine updated: {medicine.serial_number} by user {self.request.user.id}")
            
            # Log stock changes
            if medicine.stock != original_stock:
                stock_change = medicine.stock - original_stock
                action = "increased" if stock_change > 0 else "decreased"
                logger.info(f"Stock {action}: {medicine.serial_number} changed by {abs(stock_change)} units")
                
        except Exception as e:
            logger.error(f"Failed to update medicine: {str(e)} by user {self.request.user.id}")
            raise ValidationError(f"Failed to update medicine: {str(e)}")

    def perform_destroy(self, instance):
        """
        Custom deletion logic with validation and logging
        """
        # Check if medicine can be deleted
        if instance.stock > 0:
            raise ValidationError("Cannot delete medicine with existing stock. Please reduce stock to zero first.")
            
        # Check if there are any bills referencing this medicine (if you have bill items)
        # This would require a BillItem model linking medicines to bills
        
        serial_number = instance.serial_number
        try:
            instance.delete()
            logger.info(f"Medicine deleted: {serial_number} by user {self.request.user.id}")
        except Exception as e:
            logger.error(f"Failed to delete medicine {serial_number}: {str(e)}")
            raise ValidationError(f"Failed to delete medicine: {str(e)}")

    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        """
        Get medicines with stock below specified threshold (default: 10)
        """
        try:
            threshold = int(request.query_params.get('threshold', 10))
            low_stock_medicines = self.get_queryset().filter(stock__lt=threshold)
            
            serializer = self.get_serializer(low_stock_medicines, many=True)
            return Response({
                'count': low_stock_medicines.count(),
                'threshold': threshold,
                'medicines': serializer.data
            })
        except ValueError:
            return Response(
                {'error': 'Invalid threshold value'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['get'])
    def expiring_soon(self, request):
        """
        Get medicines expiring within specified days (default: 30)
        """
        try:
            days = int(request.query_params.get('days', 30))
            cutoff_date = date.today() + timedelta(days=days)
            expiring_medicines = self.get_queryset().filter(expiry_date__lte=cutoff_date)
            
            serializer = self.get_serializer(expiring_medicines, many=True)
            return Response({
                'count': expiring_medicines.count(),
                'days_ahead': days,
                'cutoff_date': cutoff_date,
                'medicines': serializer.data
            })
        except ValueError:
            return Response(
                {'error': 'Invalid days value'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['get'])
    def inventory_report(self, request):
        """
        Get comprehensive inventory statistics
        """
        queryset = self.get_queryset()
        
        total_medicines = queryset.count()
        total_stock = queryset.aggregate(total=Sum('stock'))['total'] or 0
        total_value = sum(med.total_value for med in queryset)
        low_stock_count = queryset.filter(stock__lt=10).count()
        expiring_soon_count = queryset.filter(
            expiry_date__lte=date.today() + timedelta(days=30)
        ).count()
        out_of_stock = queryset.filter(stock=0).count()
        
        avg_unit_rate = queryset.aggregate(avg=Avg('unit_rate'))['avg'] or 0
        
        return Response({
            'summary': {
                'total_medicines': total_medicines,
                'total_stock_units': total_stock,
                'total_inventory_value': float(total_value),
                'average_unit_rate': float(avg_unit_rate),
                'out_of_stock': out_of_stock,
                'low_stock_items': low_stock_count,
                'expiring_soon': expiring_soon_count,
            },
            'alerts': {
                'critical_low_stock': queryset.filter(stock__lt=5).count(),
                'expired_medicines': queryset.filter(expiry_date__lt=date.today()).count(),
            }
        })

    @action(detail=True, methods=['post'])
    def update_stock(self, request, pk=None):
        """
        Update stock quantity for a specific medicine
        """
        medicine = self.get_object()
        
        try:
            operation = request.data.get('operation', 'set')  # 'add', 'subtract', 'set'
            quantity = int(request.data.get('quantity', 0))
            reason = request.data.get('reason', 'Manual adjustment')
            
            if operation not in ['add', 'subtract', 'set']:
                return Response(
                    {'error': 'Operation must be one of: add, subtract, set'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            if quantity < 0:
                return Response(
                    {'error': 'Quantity must be non-negative'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            original_stock = medicine.stock
            
            if operation == 'add':
                medicine.stock += quantity
            elif operation == 'subtract':
                if medicine.stock < quantity:
                    return Response(
                        {'error': 'Insufficient stock for subtraction'}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
                medicine.stock -= quantity
            else:  # set
                medicine.stock = quantity
            
            medicine.save()
            
            logger.info(f"Stock updated for {medicine.serial_number}: {original_stock} -> {medicine.stock}. Reason: {reason}")
            
            return Response({
                'message': 'Stock updated successfully',
                'medicine': self.get_serializer(medicine).data,
                'stock_change': medicine.stock - original_stock,
                'reason': reason
            })
            
        except (ValueError, TypeError):
            return Response(
                {'error': 'Invalid quantity value'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': f'Failed to update stock: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def search_advanced(self, request):
        """
        Advanced search with multiple criteria
        """
        name = request.query_params.get('name', '')
        manufacturer = request.query_params.get('manufacturer', '')
        min_price = request.query_params.get('min_price', '')
        max_price = request.query_params.get('max_price', '')
        available_only = request.query_params.get('available_only', 'false').lower() == 'true'
        
        queryset = self.get_queryset()
        
        if name:
            queryset = queryset.filter(name__icontains=name)
        if manufacturer:
            queryset = queryset.filter(manufacturer__icontains=manufacturer)
        if min_price:
            try:
                queryset = queryset.filter(unit_rate__gte=Decimal(min_price))
            except:
                pass
        if max_price:
            try:
                queryset = queryset.filter(unit_rate__lte=Decimal(max_price))
            except:
                pass
        if available_only:
            queryset = queryset.filter(stock__gt=0)
            
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'count': queryset.count(),
            'results': serializer.data
        })


class BillViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Bill model with comprehensive CRUD operations
    """
    # queryset = Bill.objects.all()
    serializer_class = BillSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    # Filtering and search configuration
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'status': ['exact'],
        'bill_type': ['exact'],
        'patient_id': ['exact'],
        'ref_id': ['exact'],
        'total_amount': ['exact', 'gte', 'lte'],
        'bill_date': ['exact', 'gte', 'lte'],
        'due_date': ['exact', 'gte', 'lte']
    }
    search_fields = ['serial_number', 'notes']
    ordering_fields = ['total_amount', 'bill_date', 'due_date', 'status']
    ordering = ['-bill_date']

    def get_permissions(self):
        """
         Allow all authenticated users for all actions (development mode)
        """
        permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """
        Filter queryset based on user role and request parameters
        """
        queryset = Bill.objects.select_related('patient_id', 'created_by').all()        
        # Filter by status if specified
        status_filter = self.request.query_params.get('status_filter', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
            
        # Filter by date range
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        if start_date:
            try:
                queryset = queryset.filter(bill_date__gte=start_date)
            except:
                pass
                
        if end_date:
            try:
                queryset = queryset.filter(bill_date__lte=end_date)
            except:
                pass
        
        return queryset

    def perform_create(self, serializer):
        """
        Custom creation logic with user assignment and logging
        """
        try:
            bill = serializer.save(created_by=self.request.user)
            logger.info(f"Bill created: {bill.serial_number} for patient {bill.patient_id} by user {self.request.user.id}")
            
        except Exception as e:
            logger.error(f"Failed to create bill: {str(e)} by user {self.request.user.id}")
            raise ValidationError(f"Failed to create bill: {str(e)}")

    def perform_update(self, serializer):
        """
        Custom update logic with audit logging
        """
        original_instance = self.get_object()
        original_status = original_instance.status
        original_paid_amount = original_instance.paid_amount
        
        try:
            bill = serializer.save()
            logger.info(f"Bill updated: {bill.serial_number} by user {self.request.user.id}")
            
            # Log status changes
            if bill.status != original_status:
                logger.info(f"Bill status changed: {bill.serial_number} from {original_status} to {bill.status}")
                
            # Log payment changes
            if bill.paid_amount != original_paid_amount:
                payment_change = bill.paid_amount - original_paid_amount
                logger.info(f"Payment updated: {bill.serial_number} payment changed by {payment_change}")
                
        except Exception as e:
            logger.error(f"Failed to update bill: {str(e)} by user {self.request.user.id}")
            raise ValidationError(f"Failed to update bill: {str(e)}")

    def perform_destroy(self, instance):
        """
        Custom deletion logic with validation and logging
        """
        # Check if bill can be deleted
        if instance.status == 'PAID':
            raise ValidationError("Cannot delete a paid bill")
            
        if instance.paid_amount > 0:
            raise ValidationError("Cannot delete a bill with partial payments")
            
        serial_number = instance.serial_number
        try:
            instance.delete()
            logger.info(f"Bill deleted: {serial_number} by user {self.request.user.id}")
        except Exception as e:
            logger.error(f"Failed to delete bill {serial_number}: {str(e)}")
            raise ValidationError(f"Failed to delete bill: {str(e)}")

    @action(detail=True, methods=['post'])
    def mark_paid(self, request, pk=None):
        """
        Mark bill as paid with payment validation
        """
        bill = self.get_object()
        
        if bill.status == 'PAID':
            return Response(
                {'error': 'Bill is already marked as paid'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        if bill.status in ['CANCELLED', 'REFUNDED']:
            return Response(
                {'error': f'Cannot mark {bill.status.lower()} bill as paid'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            with transaction.atomic():
                bill.paid_amount = bill.total_amount
                bill.status = 'PAID'
                bill.save()
                
                logger.info(f"Bill marked as paid: {bill.serial_number} by user {self.request.user.id}")
                
                return Response({
                    'message': 'Bill marked as paid successfully',
                    'bill': self.get_serializer(bill).data
                })
        except Exception as e:
            logger.error(f"Failed to mark bill as paid: {str(e)}")
            return Response(
                {'error': f'Failed to mark bill as paid: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'])
    def add_payment(self, request, pk=None):
        """
        Add partial or full payment to a bill
        """
        bill = self.get_object()
        
        try:
            payment_amount = Decimal(str(request.data.get('amount', 0)))
            payment_method = request.data.get('payment_method', 'CASH')
            notes = request.data.get('notes', '')
            
            if payment_amount <= 0:
                return Response(
                    {'error': 'Payment amount must be greater than zero'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if bill.paid_amount + payment_amount > bill.total_amount:
                return Response(
                    {'error': 'Payment amount exceeds outstanding balance'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if bill.status in ['CANCELLED', 'REFUNDED']:
                return Response(
                    {'error': f'Cannot add payment to {bill.status.lower()} bill'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            with transaction.atomic():
                bill.paid_amount += payment_amount
                
                # Update status based on payment
                if bill.paid_amount == bill.total_amount:
                    bill.status = 'PAID'
                elif bill.paid_amount > 0:
                    bill.status = 'PARTIAL'
                    
                bill.save()
                
                logger.info(f"Payment added: {payment_amount} to bill {bill.serial_number} by user {self.request.user.id}")
                
                return Response({
                    'message': 'Payment added successfully',
                    'bill': self.get_serializer(bill).data,
                    'payment_added': float(payment_amount),
                    'remaining_balance': float(bill.balance_amount)
                })
                
        except (ValueError, TypeError):
            return Response(
                {'error': 'Invalid payment amount'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Failed to add payment: {str(e)}")
            return Response(
                {'error': f'Failed to add payment: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def patient_bills(self, request):
        """
        Get all bills for a specific patient with summary
        """
        patient_id = request.query_params.get('patient_id')
        if not patient_id:
            return Response(
                {'error': 'patient_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            patient_id = int(patient_id)
            bills = self.get_queryset().filter(patient_id=patient_id)
            
            # Calculate summary statistics
            total_bills = bills.count()
            total_amount = bills.aggregate(total=Sum('total_amount'))['total'] or 0
            total_paid = bills.aggregate(paid=Sum('paid_amount'))['paid'] or 0
            outstanding_balance = total_amount - total_paid
            
            pending_bills = bills.filter(status='PENDING').count()
            overdue_bills = bills.filter(status='OVERDUE').count()
            
            serializer = self.get_serializer(bills, many=True)
            
            return Response({
                'patient_id': patient_id,
                'summary': {
                    'total_bills': total_bills,
                    'total_amount': float(total_amount),
                    'total_paid': float(total_paid),
                    'outstanding_balance': float(outstanding_balance),
                    'pending_bills': pending_bills,
                    'overdue_bills': overdue_bills
                },
                'bills': serializer.data
            })
            
        except ValueError:
            return Response(
                {'error': 'Invalid patient_id format'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['get'])
    def overdue_bills(self, request):
        """
        Get all overdue bills with summary
        """
        today = date.today()
        overdue_bills = self.get_queryset().filter(
            due_date__lt=today,
            status__in=['PENDING', 'PARTIAL', 'OVERDUE']
        )
        
        total_overdue_amount = overdue_bills.aggregate(
            total=Sum('total_amount')
        )['total'] or 0
        total_paid_amount = overdue_bills.aggregate(
            paid=Sum('paid_amount')
        )['paid'] or 0
        outstanding_amount = total_overdue_amount - total_paid_amount
        
        serializer = self.get_serializer(overdue_bills, many=True)
        
        return Response({
            'count': overdue_bills.count(),
            'summary': {
                'total_overdue_amount': float(total_overdue_amount),
                'total_paid_amount': float(total_paid_amount),
                'outstanding_amount': float(outstanding_amount)
            },
            'bills': serializer.data
        })

    @action(detail=False, methods=['get'])
    def billing_report(self, request):
        """
        Get comprehensive billing statistics
        """
        queryset = self.get_queryset()
        
        # Overall statistics
        total_bills = queryset.count()
        total_revenue = queryset.aggregate(revenue=Sum('total_amount'))['revenue'] or 0
        total_collected = queryset.aggregate(collected=Sum('paid_amount'))['collected'] or 0
        outstanding_amount = total_revenue - total_collected
        
        # Status breakdown
        status_breakdown = {}
        for status_choice in Bill.STATUS_CHOICES:
            status_code = status_choice[0]
            status_count = queryset.filter(status=status_code).count()
            status_amount = queryset.filter(status=status_code).aggregate(
                amount=Sum('total_amount')
            )['amount'] or 0
            status_breakdown[status_code] = {
                'count': status_count,
                'amount': float(status_amount)
            }
        
        # Bill type breakdown
        type_breakdown = {}
        for bill_type in Bill.BILL_TYPES:
            type_code = bill_type[0]
            type_count = queryset.filter(bill_type=type_code).count()
            type_amount = queryset.filter(bill_type=type_code).aggregate(
                amount=Sum('total_amount')
            )['amount'] or 0
            type_breakdown[type_code] = {
                'count': type_count,
                'amount': float(type_amount)
            }
        
        # Recent activity (last 30 days)
        thirty_days_ago = timezone.now() - timedelta(days=30)
        recent_bills = queryset.filter(bill_date__gte=thirty_days_ago)
        recent_revenue = recent_bills.aggregate(revenue=Sum('total_amount'))['revenue'] or 0
        
        return Response({
            'overall_statistics': {
                'total_bills': total_bills,
                'total_revenue': float(total_revenue),
                'total_collected': float(total_collected),
                'outstanding_amount': float(outstanding_amount),
                'collection_rate': float((total_collected / total_revenue * 100) if total_revenue > 0 else 0)
            },
            'status_breakdown': status_breakdown,
            'bill_type_breakdown': type_breakdown,
            'recent_activity': {
                'last_30_days_bills': recent_bills.count(),
                'last_30_days_revenue': float(recent_revenue)
            }
        })
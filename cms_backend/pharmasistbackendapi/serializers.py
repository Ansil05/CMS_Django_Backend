# pharmacy/serializers.py
from rest_framework import serializers
from django.utils import timezone
from django.contrib.auth.models import User
from decimal import Decimal, InvalidOperation
from datetime import date, timedelta
import re
from .models import Medicine, Bill

class MedicineSerializer(serializers.ModelSerializer):
    # Read-only computed fields
    total_value = serializers.ReadOnlyField()
    is_low_stock = serializers.ReadOnlyField()
    is_expiring_soon = serializers.ReadOnlyField()
    
    # Additional display fields
    created_by_name = serializers.SerializerMethodField()
    days_to_expiry = serializers.SerializerMethodField()
    
    class Meta:
        model = Medicine
        fields = [
            'med_id', 'serial_number', 'med_code', 'name', 'manufacturer',
            'unit_rate', 'stock', 'expiry_date', 'created_at', 'updated_at',
            'total_value', 'is_low_stock', 'is_expiring_soon', 
            'created_by_name', 'days_to_expiry'
        ]
        read_only_fields = ('med_id', 'serial_number', 'created_at', 'updated_at', 
                           'total_value', 'is_low_stock', 'is_expiring_soon')

    def get_created_by_name(self, obj):
        """Get name of user who created the record"""
        return "System Generated"  # Can be modified based on requirements
        
    def get_days_to_expiry(self, obj):
        """Calculate days until expiry"""
        if obj.expiry_date:
            delta = obj.expiry_date - date.today()
            return delta.days
        return None

    def validate_med_code(self, value):
        """Field-level validation for medicine code"""
        if not value:
            raise serializers.ValidationError("Medicine code is required")
            
        # Clean and format
        value = value.strip().upper()
        
        # Length validation
        if len(value) < 3:
            raise serializers.ValidationError("Medicine code must be at least 3 characters")
        if len(value) > 50:
            raise serializers.ValidationError("Medicine code cannot exceed 50 characters")
            
        # Format validation
        if not re.match(r'^[A-Z0-9]+$', value):
            raise serializers.ValidationError(
                "Medicine code can only contain uppercase letters and numbers"
            )
            
        # Uniqueness validation (for updates)
        if self.instance and self.instance.med_code != value:
            if Medicine.objects.filter(med_code=value).exists():
                raise serializers.ValidationError(
                    "Medicine with this code already exists"
                )
        elif not self.instance:
            if Medicine.objects.filter(med_code=value).exists():
                raise serializers.ValidationError(
                    "Medicine with this code already exists"
                )
                
        return value

    def validate_name(self, value):
        """Field-level validation for medicine name"""
        if not value or not value.strip():
            raise serializers.ValidationError("Medicine name is required")
            
        # Clean and format
        value = value.strip().title()
        
        # Length validation
        if len(value) < 2:
            raise serializers.ValidationError("Medicine name must be at least 2 characters")
        if len(value) > 200:
            raise serializers.ValidationError("Medicine name cannot exceed 200 characters")
            
        # Format validation
        if not re.match(r'^[a-zA-Z0-9\s\-\(\)\+\.]+$', value):
            raise serializers.ValidationError(
                "Medicine name can only contain letters, numbers, spaces, hyphens, parentheses, plus signs, and periods"
            )
            
        return value

    def validate_manufacturer(self, value):
        """Field-level validation for manufacturer"""
        if not value or not value.strip():
            raise serializers.ValidationError("Manufacturer name is required")
            
        # Clean and format
        value = value.strip().title()
        
        # Length validation
        if len(value) < 2:
            raise serializers.ValidationError("Manufacturer name must be at least 2 characters")
        if len(value) > 100:
            raise serializers.ValidationError("Manufacturer name cannot exceed 100 characters")
            
        # Format validation
        if not re.match(r'^[a-zA-Z0-9\s\-&\.]+$', value):
            raise serializers.ValidationError(
                "Manufacturer name can only contain letters, numbers, spaces, hyphens, ampersands, and periods"
            )
            
        return value

    def validate_unit_rate(self, value):
        """Field-level validation for unit rate"""
        if value is None:
            raise serializers.ValidationError("Unit rate is required")
            
        # Convert to Decimal if needed
        try:
            value = Decimal(str(value))
        except (InvalidOperation, ValueError):
            raise serializers.ValidationError("Unit rate must be a valid number")
            
        # Range validation
        if value <= 0:
            raise serializers.ValidationError("Unit rate must be greater than zero")
        if value > Decimal('99999.99'):
            raise serializers.ValidationError("Unit rate cannot exceed 99999.99")
            
        # Decimal places validation
        if value.as_tuple().exponent < -2:
            raise serializers.ValidationError("Unit rate cannot have more than 2 decimal places")
            
        return value

    def validate_stock(self, value):
        """Field-level validation for stock"""
        if value is None:
            raise serializers.ValidationError("Stock quantity is required")
            
        # Type validation
        if not isinstance(value, int) or value < 0:
            raise serializers.ValidationError("Stock must be a non-negative integer")
            
        # Range validation
        if value > 999999:
            raise serializers.ValidationError("Stock cannot exceed 999999")
            
        return value

    def validate_expiry_date(self, value):
        """Field-level validation for expiry date"""
        if not value:
            raise serializers.ValidationError("Expiry date is required")
            
        # Future date validation
        if value <= date.today():
            raise serializers.ValidationError("Expiry date must be in the future")
            
        # Maximum expiry validation (10 years from today)
        max_expiry = date.today() + timedelta(days=3650)
        if value > max_expiry:
            raise serializers.ValidationError(
                "Expiry date cannot be more than 10 years from today"
            )
            
        return value

    def validate(self, data):
        """Object-level validation"""
        # Business logic validations
        expiry_date = data.get('expiry_date')
        if expiry_date and expiry_date <= date.today() + timedelta(days=7):
            # Warning for medicines expiring within a week
            pass  # Could add warning system here
            
        # Stock and rate combination validation
        stock = data.get('stock')
        unit_rate = data.get('unit_rate')
        if stock is not None and unit_rate is not None:
            total_value = stock * unit_rate
            if total_value > Decimal('9999999.99'):
                raise serializers.ValidationError(
                    "Total inventory value (stock × unit_rate) cannot exceed 9999999.99"
                )
                
        return data

    def create(self, validated_data):
        """Create method with additional validation"""
        try:
            # Create medicine instance
            medicine = Medicine.objects.create(**validated_data)
            return medicine
        except Exception as e:
            raise serializers.ValidationError(f"Failed to create medicine: {str(e)}")

    def update(self, instance, validated_data):
        """Update method with additional validation"""
        try:
            # Store original values for audit
            original_stock = instance.stock
            original_rate = instance.unit_rate
            
            # Update fields
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
                
            # Additional business logic for updates
            if 'stock' in validated_data:
                new_stock = validated_data['stock']
                if new_stock < original_stock:
                    # Stock reduced - could trigger reorder alert
                    pass
                    
            instance.save()
            return instance
        except Exception as e:
            raise serializers.ValidationError(f"Failed to update medicine: {str(e)}")


class BillSerializer(serializers.ModelSerializer):
    # Read-only computed fields
    balance_amount = serializers.ReadOnlyField()
    is_overdue = serializers.ReadOnlyField()
    payment_percentage = serializers.ReadOnlyField()
    
    # Additional display fields
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    days_overdue = serializers.SerializerMethodField()
    
    class Meta:
        model = Bill
        fields = [
            'bill_id', 'serial_number', 'bill_type', 'patient_id', 'ref_id',
            'total_amount', 'paid_amount', 'status', 'bill_date', 'due_date',
            'notes', 'created_by', 'balance_amount', 'is_overdue', 
            'payment_percentage', 'created_by_name', 'created_by_username',
            'days_overdue'
        ]
        read_only_fields = ('bill_id', 'serial_number', 'bill_date', 'balance_amount',
                           'is_overdue', 'payment_percentage')

    def get_days_overdue(self, obj):
        """Calculate days overdue"""
        if obj.is_overdue:
            delta = date.today() - obj.due_date
            return delta.days
        return 0

    def validate_bill_type(self, value):
        """Field-level validation for bill type"""
        if not value:
            raise serializers.ValidationError("Bill type is required")
            
        valid_types = [choice[0] for choice in Bill.BILL_TYPES]
        if value not in valid_types:
            raise serializers.ValidationError(
                f"Invalid bill type. Must be one of: {', '.join(valid_types)}"
            )
            
        return value

    def validate_patient_id(self, value):
        """Field-level validation for patient ID"""
        if value is None:
            raise serializers.ValidationError("Patient ID is required")
            
        if not isinstance(value, int) or value <= 0:
            raise serializers.ValidationError("Patient ID must be a positive integer")
            
        # Could add validation to check if patient exists in patient system
        # if not Patient.objects.filter(id=value).exists():
        #     raise serializers.ValidationError("Patient with this ID does not exist")
            
        return value

    def validate_ref_id(self, value):
        """Field-level validation for reference ID"""
        if value is None:
            raise serializers.ValidationError("Reference ID is required")
            
        if not isinstance(value, int) or value <= 0:
            raise serializers.ValidationError("Reference ID must be a positive integer")
            
        return value

    def validate_total_amount(self, value):
        """Field-level validation for total amount"""
        if value is None:
            raise serializers.ValidationError("Total amount is required")
            
        # Convert to Decimal if needed
        try:
            value = Decimal(str(value))
        except (InvalidOperation, ValueError):
            raise serializers.ValidationError("Total amount must be a valid number")
            
        # Range validation
        if value <= 0:
            raise serializers.ValidationError("Total amount must be greater than zero")
        if value > Decimal('999999.99'):
            raise serializers.ValidationError("Total amount cannot exceed 999999.99")
            
        # Decimal places validation
        if value.as_tuple().exponent < -2:
            raise serializers.ValidationError("Total amount cannot have more than 2 decimal places")
            
        return value

    def validate_paid_amount(self, value):
        """Field-level validation for paid amount"""
        if value is None:
            value = Decimal('0.00')
            
        # Convert to Decimal if needed
        try:
            value = Decimal(str(value))
        except (InvalidOperation, ValueError):
            raise serializers.ValidationError("Paid amount must be a valid number")
            
        # Range validation
        if value < 0:
            raise serializers.ValidationError("Paid amount cannot be negative")
        if value > Decimal('999999.99'):
            raise serializers.ValidationError("Paid amount cannot exceed 999999.99")
            
        # Decimal places validation
        if value.as_tuple().exponent < -2:
            raise serializers.ValidationError("Paid amount cannot have more than 2 decimal places")
            
        return value

    def validate_status(self, value):
        """Field-level validation for status"""
        if not value:
            raise serializers.ValidationError("Status is required")
            
        valid_statuses = [choice[0] for choice in Bill.STATUS_CHOICES]
        if value not in valid_statuses:
            raise serializers.ValidationError(
                f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
            )
            
        return value

    def validate_due_date(self, value):
        """Field-level validation for due date"""
        if value:
            # Allow past due dates but warn about overdue status
            if value < date.today():
                # This will be handled in object-level validation
                pass
                
        return value

    def validate_notes(self, value):
        """Field-level validation for notes"""
        if value and len(value) > 500:
            raise serializers.ValidationError("Notes cannot exceed 500 characters")
            
        return value

    def validate(self, data):
        """Object-level validation"""
        total_amount = data.get('total_amount')
        paid_amount = data.get('paid_amount', Decimal('0.00'))
        status = data.get('status')
        bill_type = data.get('bill_type')
        
        # Cross-field validations
        if paid_amount and total_amount and paid_amount > total_amount:
            raise serializers.ValidationError(
                "Paid amount cannot exceed total amount"
            )
            
        # Status-specific validations
        if status == 'PAID' and paid_amount != total_amount:
            raise serializers.ValidationError(
                "Status cannot be PAID if paid amount does not equal total amount"
            )
            
        if status == 'PARTIAL' and (paid_amount <= 0 or paid_amount >= total_amount):
            raise serializers.ValidationError(
                "Status can only be PARTIAL if 0 < paid amount < total amount"
            )
            
        # Bill type specific validations
        if bill_type == 'MEDICINE' and total_amount and total_amount < Decimal('1.00'):
            raise serializers.ValidationError(
                "Medicine bills must have minimum amount of 1.00"
            )
            
        # Auto-adjust status based on payment
        if paid_amount == total_amount and status in ['PENDING', 'PARTIAL']:
            data['status'] = 'PAID'
        elif 0 < paid_amount < total_amount and status == 'PENDING':
            data['status'] = 'PARTIAL'
            
        return data

    def create(self, validated_data):
        """Create method with user assignment and validation"""
        try:
            # Auto-set due date if not provided
            if 'due_date' not in validated_data or not validated_data['due_date']:
                validated_data['due_date'] = date.today() + timedelta(days=30)
                
            # Create bill instance
            bill = Bill.objects.create(**validated_data)
            return bill
        except Exception as e:
            raise serializers.ValidationError(f"Failed to create bill: {str(e)}")

    def update(self, instance, validated_data):
        """Update method with audit and business logic"""
        try:
            # Store original values for audit
            original_status = instance.status
            original_paid_amount = instance.paid_amount
            
            # Update fields
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
                
            # Business logic for status changes
            if 'paid_amount' in validated_data or 'total_amount' in validated_data:
                # Recalculate status if amounts changed
                if instance.paid_amount == instance.total_amount:
                    instance.status = 'PAID'
                elif 0 < instance.paid_amount < instance.total_amount:
                    instance.status = 'PARTIAL'
                elif instance.paid_amount == 0:
                    instance.status = 'PENDING'
                    
            # Check overdue status
            if instance.due_date and instance.due_date < date.today():
                if instance.status not in ['PAID', 'CANCELLED', 'REFUNDED']:
                    instance.status = 'OVERDUE'
                    
            instance.save()
            return instance
        except Exception as e:
            raise serializers.ValidationError(f"Failed to update bill: {str(e)}")

    def delete(self, instance):
        """Soft delete with business logic validation"""
        # Check if bill can be deleted
        if instance.status == 'PAID':
            raise serializers.ValidationError("Cannot delete a paid bill")
            
        if instance.paid_amount > 0:
            raise serializers.ValidationError("Cannot delete a bill with partial payments")
            
        # Proceed with deletion
        instance.delete()
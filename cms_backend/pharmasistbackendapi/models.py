from django.db import models
from django.contrib.auth.models import User
from django.core.validators import (
    MinValueValidator, MaxValueValidator, RegexValidator, 
    MinLengthValidator, MaxLengthValidator
)
from django.core.exceptions import ValidationError
from decimal import Decimal
from datetime import date, timedelta
import uuid
import re

def validate_medicine_code(value):
    """Custom validator for medicine code format"""
    if not re.match(r'^[A-Z0-9]{3,20}$', value):
        raise ValidationError(
            'Medicine code must be 3-20 characters, alphanumeric uppercase only'
        )

def validate_manufacturer_name(value):
    """Custom validator for manufacturer name"""
    if not re.match(r'^[a-zA-Z0-9\s\-&\.]+$', value):
        raise ValidationError(
            'Manufacturer name can only contain letters, numbers, spaces, hyphens, ampersands, and periods'
        )

def validate_expiry_date(value):
    """Custom validator for expiry date"""
    if value <= date.today():
        raise ValidationError('Expiry date must be in the future')
    
    max_expiry = date.today() + timedelta(days=3650)  # 10 years
    if value > max_expiry:
        raise ValidationError('Expiry date cannot be more than 10 years from today')

def validate_medicine_name(value):
    """Custom validator for medicine name"""
    if len(value.strip()) < 2:
        raise ValidationError('Medicine name must be at least 2 characters after trimming spaces')
    
    if not re.match(r'^[a-zA-Z0-9\s\-\(\)\+\.]+$', value):
        raise ValidationError(
            'Medicine name can only contain letters, numbers, spaces, hyphens, parentheses, plus signs, and periods'
        )

class Medicine(models.Model):
    med_id = models.AutoField(
        primary_key=True,
        help_text="Unique identifier for medicine"
    )
    
    serial_number = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        help_text="Auto-generated unique serial number",
        db_index=True
    )
    
    med_code = models.CharField(
        max_length=50,
        unique=True,
        validators=[
            MinLengthValidator(3, message="Medicine code must be at least 3 characters"),
            MaxLengthValidator(50, message="Medicine code cannot exceed 50 characters"),
            validate_medicine_code
        ],
        help_text="Unique medicine barcode/SKU (3-50 characters, alphanumeric)",
        db_index=True
    )
    
    name = models.CharField(
        max_length=200,
        validators=[
            MinLengthValidator(2, message="Medicine name must be at least 2 characters"),
            MaxLengthValidator(200, message="Medicine name cannot exceed 200 characters"),
            validate_medicine_name
        ],
        help_text="Medicine name (2-200 characters)",
        db_index=True
    )
    
    manufacturer = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(2, message="Manufacturer name must be at least 2 characters"),
            MaxLengthValidator(100, message="Manufacturer name cannot exceed 100 characters"),
            validate_manufacturer_name
        ],
        help_text="Manufacturer company name (2-100 characters)",
        db_index=True
    )
    
    unit_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal('0.01'), message="Unit rate must be at least 0.01"),
            MaxValueValidator(Decimal('99999.99'), message="Unit rate cannot exceed 99999.99")
        ],
        help_text="Price per unit (0.01 - 99999.99)"
    )
    
    stock = models.PositiveIntegerField(
        default=0,
        validators=[
            MinValueValidator(0, message="Stock cannot be negative"),
            MaxValueValidator(999999, message="Stock cannot exceed 999999")
        ],
        help_text="Current stock quantity (0 - 999999)"
    )
    
    expiry_date = models.DateField(
        validators=[validate_expiry_date],
        help_text="Medicine expiry date (must be future date, max 10 years from today)",
        db_index=True
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Record creation timestamp"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Record last update timestamp"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Medicine"
        verbose_name_plural = "Medicines"
        db_table = 'pharmacy_medicine'
        indexes = [
            models.Index(fields=['med_code'], name='med_code_idx'),
            models.Index(fields=['name'], name='med_name_idx'),
            models.Index(fields=['manufacturer'], name='manufacturer_idx'),
            models.Index(fields=['expiry_date'], name='expiry_date_idx'),
        ]

    def clean(self):
        """Model-level validation"""
        super().clean()
        
        errors = {}
        
        # Validate medicine code format
        if self.med_code:
            self.med_code = self.med_code.upper().strip()
            
        # Validate name format
        if self.name:
            self.name = self.name.strip().title()
            
        # Validate manufacturer format
        if self.manufacturer:
            self.manufacturer = self.manufacturer.strip().title()
            
        # Business logic validations
        if self.stock is not None and self.stock < 0:
            errors['stock'] = 'Stock quantity cannot be negative'
            
        if self.unit_rate is not None and self.unit_rate <= 0:
            errors['unit_rate'] = 'Unit rate must be greater than zero'
            
        # Cross-field validation
        if self.expiry_date and self.expiry_date <= date.today():
            errors['expiry_date'] = 'Expiry date must be in the future'
            
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        # Auto-generate serial number
        if not self.serial_number:
            unique_id = uuid.uuid4().hex[:8].upper()
            self.serial_number = f"MED{unique_id}"
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.serial_number}) - {self.manufacturer}"

    @property
    def is_low_stock(self):
        """Check if medicine is low on stock (less than 10 units)"""
        return self.stock < 10
        
    @property
    def is_expiring_soon(self):
        """Check if medicine expires within 30 days"""
        return self.expiry_date <= date.today() + timedelta(days=30)
        
    @property
    def total_value(self):
        """Calculate total inventory value for this medicine"""
        return self.stock * self.unit_rate


def validate_patient_id(value):
    """Custom validator for patient ID"""
    if value <= 0:
        raise ValidationError('Patient ID must be a positive integer')

def validate_ref_id(value):
    """Custom validator for reference ID"""
    if value <= 0:
        raise ValidationError('Reference ID must be a positive integer')

def validate_total_amount(value):
    """Custom validator for total amount"""
    if value <= 0:
        raise ValidationError('Total amount must be greater than zero')
from reseptionistbackendapi.models import Patient
class Bill(models.Model):
    BILL_TYPES = (
        ('MEDICINE', 'Medicine Sale'),
        ('CONSULTATION', 'Consultation Fee'),
        ('PROCEDURE', 'Medical Procedure'),
        ('DIAGNOSTIC', 'Diagnostic Test'),
        ('EMERGENCY', 'Emergency Service'),
    )
    
    STATUS_CHOICES = (
        ('PENDING', 'Pending Payment'),
        ('PAID', 'Paid'),
        ('PARTIAL', 'Partially Paid'),
        ('CANCELLED', 'Cancelled'),
        ('REFUNDED', 'Refunded'),
        ('OVERDUE', 'Overdue'),
    )

    bill_id = models.AutoField(
        primary_key=True,
        help_text="Unique identifier for bill"
    )
    
    serial_number = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        help_text="Auto-generated unique serial number",
        db_index=True
    )
    
    bill_type = models.CharField(
        max_length=20,
        choices=BILL_TYPES,
        help_text="Type of bill/service"
    )
    
    patient_id = models.ForeignKey(Patient, on_delete=models.SET_NULL,null=True, blank=True,
        validators=[validate_patient_id],
        help_text="Reference to Patient ID (must be positive integer)",
        db_index=True
    )
    
    ref_id = models.PositiveIntegerField(
        validators=[validate_ref_id],
        help_text="Reference ID (Prescription/Appointment/Doctor ID)",
        db_index=True
    )
    
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal('0.01'), message="Total amount must be at least 0.01"),
            MaxValueValidator(Decimal('999999.99'), message="Total amount cannot exceed 999999.99"),
            validate_total_amount
        ],
        help_text="Total bill amount (0.01 - 999999.99)"
    )
    
    paid_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[
            MinValueValidator(Decimal('0.00'), message="Paid amount cannot be negative"),
            MaxValueValidator(Decimal('999999.99'), message="Paid amount cannot exceed 999999.99")
        ],
        help_text="Amount already paid (0.00 - 999999.99)"
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING',
        help_text="Current bill status"
    )
    
    bill_date = models.DateTimeField(
        auto_now_add=True,
        help_text="Bill creation date and time",
        db_index=True
    )
    
    due_date = models.DateField(
        help_text="Payment due date",
        null=True,
        blank=True
    )
    
    notes = models.TextField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Additional notes or comments (max 500 characters)"
    )
    
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        help_text="User who created this bill"
    )

    class Meta:
        ordering = ['-bill_date']
        verbose_name = "Bill"
        verbose_name_plural = "Bills"
        db_table = 'pharmacy_bill'
        indexes = [
            models.Index(fields=['patient_id'], name='patient_id_idx'),
            models.Index(fields=['status'], name='bill_status_idx'),
            models.Index(fields=['bill_type'], name='bill_type_idx'),
            models.Index(fields=['bill_date'], name='bill_date_idx'),
        ]

    def clean(self):
        """Model-level validation"""
        super().clean()
        
        errors = {}
        
        # Business logic validations
        if self.paid_amount is not None and self.total_amount is not None:
            if self.paid_amount > self.total_amount:
                errors['paid_amount'] = 'Paid amount cannot exceed total amount'
        
        # Status-specific validations
        if self.status == 'PAID' and self.paid_amount != self.total_amount:
            errors['status'] = 'Status cannot be PAID if paid amount does not equal total amount'
            
        if self.status == 'PARTIAL' and (self.paid_amount <= 0 or self.paid_amount >= self.total_amount):
            errors['status'] = 'Status can only be PARTIAL if 0 < paid amount < total amount'
            
        # Due date validation
        if self.due_date and self.due_date < date.today():
            if self.status not in ['PAID', 'CANCELLED', 'REFUNDED']:
                self.status = 'OVERDUE'
        
        # Bill type specific validations
        if self.bill_type == 'MEDICINE' and self.total_amount < Decimal('1.00'):
            errors['total_amount'] = 'Medicine bills must have minimum amount of 1.00'
            
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        # Auto-generate serial number
        if not self.serial_number:
            unique_id = uuid.uuid4().hex[:8].upper()
            self.serial_number = f"BILL{unique_id}"
            
        # Auto-set due date if not provided
        if not self.due_date:
            self.due_date = date.today() + timedelta(days=30)
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Bill {self.serial_number} - ₹{self.total_amount} ({self.status})"

    @property
    def balance_amount(self):
        """Calculate remaining balance"""
        return self.total_amount - self.paid_amount
        
    @property
    def is_overdue(self):
        """Check if bill is overdue"""
        return (self.due_date and 
                self.due_date < date.today() and 
                self.status not in ['PAID', 'CANCELLED', 'REFUNDED'])
                
    @property
    def payment_percentage(self):
        """Calculate payment completion percentage"""
        if self.total_amount > 0:
            return (self.paid_amount / self.total_amount) * 100
        return 0
from django.db import models
from django.contrib.auth.models import AbstractUser


# Blood Group Choices
BLOOD_GROUP_CHOICES = [
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B-', 'B-'),
    ('O+', 'O+'),
    ('O-', 'O-'),
    ('AB+', 'AB+'),
    ('AB-', 'AB-'),
]


class Register(AbstractUser):

    # Contact Information
    whatsapp_number = models.CharField(max_length=15)

    other_number = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    address = models.TextField()


    # Blood Information
    blood_group = models.CharField(
        max_length=5,
        choices=BLOOD_GROUP_CHOICES
    )

    is_donor = models.BooleanField(
        default=False,
        verbose_name="Are you a blood donor?"
    )

    last_donation_date = models.DateField(
        null=True,
        blank=True
    )


    # Personal Information
    age = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )


    # University Information
    university_batch = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )


    def __str__(self):
        return f"{self.first_name} {self.last_name}"


    # =========================================================
# BLOOD REQUEST MODEL
# =========================================================

class BloodRequest(models.Model):

    patient_problem = models.TextField()

    blood_amount = models.PositiveIntegerField(
        help_text="Amount of blood required in bags/units"
    )

    blood_group = models.CharField(
        max_length=5,
        choices=BLOOD_GROUP_CHOICES
    )

    required_date = models.DateField()

    required_time = models.TimeField()

    phone_number = models.CharField(
        max_length=15
    )

    hospital_name = models.CharField(
        max_length=200
    )

    requested_by = models.ForeignKey(
        Register,
        on_delete=models.CASCADE,
        related_name="blood_requests"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return (
            f"{self.blood_group} - "
            f"{self.hospital_name}"
        )


# =========================================================
# BLOOD NOTIFICATION MODEL
# =========================================================

class BloodNotification(models.Model):

    donor = models.ForeignKey(
        Register,
        on_delete=models.CASCADE,
        related_name="blood_notifications"
    )

    blood_request = models.ForeignKey(
        BloodRequest,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    message = models.TextField()

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return (
            f"Notification for "
            f"{self.donor.username}"
        )
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group, Permission

from .models import (
    Register,
    BloodRequest,
    BloodNotification,
)


# =========================================================
# USER / ADMIN / MODERATOR
# =========================================================

@admin.register(Register)
class RegisterAdmin(UserAdmin):

    list_display = (
        'username',
        'email',
        'whatsapp_number',
        'blood_group',
        'is_donor',
        'age',
        'weight',
        'university_batch',
        'is_staff',
        'is_superuser',
    )

    list_filter = (
        'is_staff',
        'is_superuser',
        'is_active',
        'is_donor',
        'blood_group',
    )

    search_fields = (
        'username',
        'first_name',
        'last_name',
        'email',
        'whatsapp_number',
    )

    # =====================================================
    # USER EDIT PAGE
    # =====================================================

    fieldsets = UserAdmin.fieldsets + (
        (
            'Blood Donation Information',
            {
                'fields': (
                    'whatsapp_number',
                    'other_number',
                    'address',
                    'blood_group',
                    'is_donor',
                    'last_donation_date',
                    'age',
                    'weight',
                    'university_batch',
                )
            },
        ),
    )

    # =====================================================
    # USER ADD PAGE
    # =====================================================

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            'Blood Donation Information',
            {
                'fields': (
                    'first_name',
                    'last_name',
                    'email',
                    'whatsapp_number',
                    'other_number',
                    'address',
                    'blood_group',
                    'is_donor',
                    'last_donation_date',
                    'age',
                    'weight',
                    'university_batch',
                )
            },
        ),
    )


# =========================================================
# BLOOD REQUEST ADMIN
# =========================================================

@admin.register(BloodRequest)
class BloodRequestAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'patient_problem',
        'blood_amount',
        'blood_group',
        'required_date',
        'required_time',
        'phone_number',
        'hospital_name',
        'requested_by',
        'created_at',
    )

    list_filter = (
        'blood_group',
        'required_date',
        'hospital_name',
    )

    search_fields = (
        'patient_problem',
        'hospital_name',
        'phone_number',
        'requested_by__username',
        'requested_by__first_name',
        'requested_by__last_name',
    )

    ordering = (
        '-created_at',
    )


# =========================================================
# BLOOD NOTIFICATION ADMIN
# =========================================================

@admin.register(BloodNotification)
class BloodNotificationAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'donor',
        'blood_request',
        'is_read',
        'created_at',
    )

    list_filter = (
        'is_read',
        'created_at',
        'blood_request__blood_group',
    )

    search_fields = (
        'donor__username',
        'donor__first_name',
        'donor__last_name',
        'blood_request__hospital_name',
        'blood_request__blood_group',
    )

    ordering = (
        '-created_at',
    )
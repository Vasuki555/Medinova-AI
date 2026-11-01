"""
Pydantic Schemas Package
Export all request and response schemas
"""

from app.schemas.auth import UserRegisterRequest, UserLoginRequest, TokenResponse, ErrorResponse
from app.schemas.patient_profile import PatientProfileCreate, PatientProfileUpdate, PatientProfileResponse
from app.schemas.doctor_profile import DoctorProfileCreate, DoctorProfileUpdate, DoctorProfileResponse
from app.schemas.appointment import AppointmentCreate, AppointmentStatusUpdate, AppointmentConsultationUpdate, AppointmentResponse
from app.schemas.medication import MedicationCreate, MedicationUpdate, LogIntakeRequest, MedicationResponse
from app.schemas.health_record import HealthRecordCreate, HealthRecordResponse
from app.schemas.notification import NotificationResponse
from app.schemas.hospital import HospitalCreate, HospitalResponse

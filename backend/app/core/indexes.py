"""
Database Indexes
Create indexes for MongoDB collections
"""

from motor.motor_asyncio import AsyncIOMotorDatabase
import logging

logger = logging.getLogger(__name__)


async def create_indexes(db: AsyncIOMotorDatabase):
    """
    Create database indexes for optimal query performance
    Following the approved database design

    Args:
        db: MongoDB database instance
    """
    try:
        logger.info("Creating database indexes...")

        # Users collection indexes
        await db.users.create_index("email", unique=True)
        await db.users.create_index("role")
        await db.users.create_index("created_at")
        await db.users.create_index([("email", 1), ("is_active", 1)])

        # Patients collection indexes
        await db.patient_profiles.create_index("user_id", unique=True)

        # Doctors collection indexes
        await db.doctor_profiles.create_index("user_id", unique=True)
        # sparse=True means the unique constraint only applies to documents where the field exists
        # and is not None — prevents duplicate-key errors when license_number is not yet provided
        await db.doctor_profiles.create_index("license_number", unique=True, sparse=True)
        await db.doctor_profiles.create_index("specialization")

        # Appointments collection indexes
        await db.appointments.create_index("appointment_number", unique=True)
        await db.appointments.create_index("patient_id")
        await db.appointments.create_index("doctor_id")
        await db.appointments.create_index("appointment_date")

        # Medications collection indexes
        await db.medications.create_index("patient_id")
        await db.medications.create_index("is_active")

        # Health records collection indexes
        await db.health_records.create_index("patient_id")
        await db.health_records.create_index("recorded_at")

        # Notifications collection indexes
        await db.notifications.create_index("user_id")
        await db.notifications.create_index("is_read")
        await db.notifications.create_index("created_at")

        # Hospitals collection indexes
        # NOTE: We index the GeoJSON location field for $nearSphere queries.
        # No unique index on 'hospital_id' — hospitals use MongoDB _id as primary key.
        await db.hospitals.create_index([("address.location", "2dsphere")], sparse=True)

        logger.info("Database indexes created successfully")

    except Exception as e:
        logger.error(f"Failed to create indexes: {str(e)}")
        # Don't raise - indexes are optimization, not critical for startup

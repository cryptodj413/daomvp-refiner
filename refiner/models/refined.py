from datetime import datetime, date
from sqlalchemy import (
    Column, String, Integer, Float, ForeignKey, DateTime, Date, Boolean, DECIMAL, Table
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# =====================================================
# User / App-Specific Tables
# =====================================================
class UserRefined(Base):
    __tablename__ = 'users'
    
    user_id = Column(String, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    locale = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    
    storage_metrics = relationship("StorageMetric", back_populates="user")
    auth_sources = relationship("AuthSource", back_populates="user")

class StorageMetric(Base):
    __tablename__ = 'storage_metrics'
    
    metric_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey('users.user_id'), nullable=False)
    percent_used = Column(Float, nullable=False)
    recorded_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    user = relationship("UserRefined", back_populates="storage_metrics")

class AuthSource(Base):
    __tablename__ = 'auth_sources'
    
    auth_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey('users.user_id'), nullable=False)
    source = Column(String, nullable=False)
    collection_date = Column(DateTime, nullable=False)
    data_type = Column(String, nullable=False)
    
    user = relationship("UserRefined", back_populates="auth_sources")

# =====================================================
# FHIR Core Resources
# =====================================================

class Patient(Base):
    __tablename__ = 'patients'
    
    id = Column(String, primary_key=True)
    resource_id = Column(String, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    prefix = Column(String(50))
    gender = Column(String(10))
    birth_date = Column(Date)
    deceased_date_time = Column(DateTime)
    marital_status = Column(String(50))
    multiple_birth_boolean = Column(Boolean)
    race = Column(String(100))
    ethnicity = Column(String(100))
    birth_sex = Column(String(10))
    birth_place_city = Column(String(100))
    birth_place_state = Column(String(100))
    birth_place_country = Column(String(100))
    address_line = Column(String(500))
    address_city = Column(String(100))
    address_state = Column(String(100))
    address_postal_code = Column(String(20))
    address_country = Column(String(100))
    address_latitude = Column(DECIMAL(10,8))
    address_longitude = Column(DECIMAL(11,8))
    phone = Column(String(20))
    language = Column(String(100))
    ssn = Column(String(20))
    drivers_license = Column(String(50))
    mothers_maiden_name = Column(String(255))
    daly = Column(DECIMAL(10,6))
    qaly = Column(DECIMAL(10,6))
    import_date = Column(DateTime, default=datetime.utcnow)

    # Relationships
    encounters = relationship("Encounter", back_populates="patient")
    observations = relationship("Observation", back_populates="patient")
    conditions = relationship("Condition", back_populates="patient")
    medication_requests = relationship("MedicationRequest", back_populates="patient")
    immunizations = relationship("Immunization", back_populates="patient")
    diagnostic_reports = relationship("DiagnosticReport", back_populates="patient")
    procedures = relationship("Procedure", back_populates="patient")
    claims = relationship("Claim", back_populates="patient")


class Practitioner(Base):
    __tablename__ = 'practitioners'
    
    id = Column(String, primary_key=True)
    resource_id = Column(String, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    prefix = Column(String(50))
    suffix = Column(String(50))
    gender = Column(String(10))
    birth_date = Column(Date)
    npi = Column(String(20))
    license_number = Column(String(50))
    specialty = Column(String(100))
    import_date = Column(DateTime, default=datetime.utcnow)

    encounters = relationship("Encounter", back_populates="practitioner")
    observations = relationship("Observation", back_populates="performer")
    diagnostic_reports = relationship("DiagnosticReport", back_populates="performer")
    procedures = relationship("Procedure", back_populates="performer")
    immunizations = relationship("Immunization", back_populates="performer")
    medication_requests = relationship("MedicationRequest", back_populates="requester")


class Organization(Base):
    __tablename__ = 'organizations'
    
    id = Column(String, primary_key=True)
    resource_id = Column(String, nullable=False)
    name = Column(String)
    type = Column(String(100))
    address_line = Column(String(500))
    address_city = Column(String(100))
    address_state = Column(String(100))
    address_postal_code = Column(String(20))
    address_country = Column(String(100))
    phone = Column(String(20))
    import_date = Column(DateTime, default=datetime.utcnow)

    encounters = relationship("Encounter", back_populates="organization")
    claims = relationship("Claim", back_populates="insurer")

# =====================================================
# Clinical Resources
# =====================================================

class Encounter(Base):
    __tablename__ = 'encounters'
    
    id = Column(String, primary_key=True)
    resource_id = Column(String, nullable=False)
    patient_id = Column(String, ForeignKey('patients.id'))
    practitioner_id = Column(String, ForeignKey('practitioners.id'))
    organization_id = Column(String, ForeignKey('organizations.id'))
    status = Column(String(50))
    class_code = Column(String(50))
    type_code = Column(String(50))
    type_display = Column(String(500))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    import_date = Column(DateTime, default=datetime.utcnow)

    patient = relationship("Patient", back_populates="encounters")
    practitioner = relationship("Practitioner", back_populates="encounters")
    organization = relationship("Organization", back_populates="encounters")

    observations = relationship("Observation", back_populates="encounter")
    conditions = relationship("Condition", back_populates="encounter")
    medication_requests = relationship("MedicationRequest", back_populates="encounter")
    diagnostic_reports = relationship("DiagnosticReport", back_populates="encounter")
    procedures = relationship("Procedure", back_populates="encounter")


class Observation(Base):
    __tablename__ = 'observations'
    
    id = Column(String, primary_key=True)
    resource_id = Column(String, nullable=False)
    patient_id = Column(String, ForeignKey('patients.id'))
    encounter_id = Column(String, ForeignKey('encounters.id'))
    performer_id = Column(String, ForeignKey('practitioners.id'))
    status = Column(String(50))
    category_code = Column(String(50))
    code = Column(String(50))
    display = Column(String(500))
    effective_date_time = Column(DateTime)
    issued = Column(DateTime)
    value_quantity = Column(DECIMAL(18,4))
    value_unit = Column(String(50))
    value_code = Column(String(50))
    value_display = Column(String(500))
    value_string = Column(String(1000))
    value_boolean = Column(Boolean)
    reference_range_low = Column(DECIMAL(18,4))
    reference_range_high = Column(DECIMAL(18,4))
    import_date = Column(DateTime, default=datetime.utcnow)

    patient = relationship("Patient", back_populates="observations")
    encounter = relationship("Encounter", back_populates="observations")
    performer = relationship("Practitioner", back_populates="observations")


class Condition(Base):
    __tablename__ = 'conditions'
    
    id = Column(String, primary_key=True)
    resource_id = Column(String, nullable=False)
    patient_id = Column(String, ForeignKey('patients.id'))
    encounter_id = Column(String, ForeignKey('encounters.id'))
    asserter_id = Column(String, ForeignKey('practitioners.id'))
    status = Column(String(50))
    category_code = Column(String(50))
    code = Column(String(50))
    display = Column(String(500))
    onset_date_time = Column(DateTime)
    abatement_date_time = Column(DateTime)
    clinical_status = Column(String(50))
    verification_status = Column(String(50))
    import_date = Column(DateTime, default=datetime.utcnow)

    patient = relationship("Patient", back_populates="conditions")
    encounter = relationship("Encounter", back_populates="conditions")
    asserter = relationship("Practitioner")


class MedicationRequest(Base):
    __tablename__ = 'medication_requests'
    
    id = Column(String, primary_key=True)
    resource_id = Column(String, nullable=False)
    patient_id = Column(String, ForeignKey('patients.id'))
    encounter_id = Column(String, ForeignKey('encounters.id'))
    requester_id = Column(String, ForeignKey('practitioners.id'))
    status = Column(String(50))
    intent = Column(String(50))
    medication_code = Column(String(50))
    medication_display = Column(String(500))
    authored_on = Column(DateTime)
    dosage_instruction = Column(String(1000))
    import_date = Column(DateTime, default=datetime.utcnow)

    patient = relationship("Patient", back_populates="medication_requests")
    encounter = relationship("Encounter", back_populates="medication_requests")
    requester = relationship("Practitioner", back_populates="medication_requests")


class Immunization(Base):
    __tablename__ = 'immunizations'
    
    id = Column(String, primary_key=True)
    resource_id = Column(String, nullable=False)
    patient_id = Column(String, ForeignKey('patients.id'))
    performer_id = Column(String, ForeignKey('practitioners.id'))
    status = Column(String(50))
    vaccine_code = Column(String(50))
    vaccine_display = Column(String(500))
    occurrence_date_time = Column(DateTime)
    lot_number = Column(String(100))
    import_date = Column(DateTime, default=datetime.utcnow)

    patient = relationship("Patient", back_populates="immunizations")
    performer = relationship("Practitioner", back_populates="immunizations")


class DiagnosticReport(Base):
    __tablename__ = 'diagnostic_reports'
    
    id = Column(String, primary_key=True)
    resource_id = Column(String, nullable=False)
    patient_id = Column(String, ForeignKey('patients.id'))
    encounter_id = Column(String, ForeignKey('encounters.id'))
    performer_id = Column(String, ForeignKey('practitioners.id'))
    status = Column(String(50))
    category_code = Column(String(50))
    code = Column(String(50))
    display = Column(String(500))
    effective_date_time = Column(DateTime)
    issued = Column(DateTime)
    conclusion = Column(String(2000))
    import_date = Column(DateTime, default=datetime.utcnow)

    patient = relationship("Patient", back_populates="diagnostic_reports")
    encounter = relationship("Encounter", back_populates="diagnostic_reports")
    performer = relationship("Practitioner", back_populates="diagnostic_reports")


class Procedure(Base):
    __tablename__ = 'procedures'
    
    id = Column(String, primary_key=True)
    resource_id = Column(String, nullable=False)
    patient_id = Column(String, ForeignKey('patients.id'))
    encounter_id = Column(String, ForeignKey('encounters.id'))
    performer_id = Column(String, ForeignKey('practitioners.id'))
    location_id = Column(String, ForeignKey('organizations.id'))
    status = Column(String(50))
    code = Column(String(50))
    display = Column(String(500))
    performed_date_time = Column(DateTime)
    import_date = Column(DateTime, default=datetime.utcnow)

    patient = relationship("Patient", back_populates="procedures")
    encounter = relationship("Encounter", back_populates="procedures")
    performer = relationship("Practitioner", back_populates="procedures")
    location = relationship("Organization")


class Claim(Base):
    __tablename__ = 'claims'
    
    id = Column(String, primary_key=True)
    resource_id = Column(String, nullable=False)
    patient_id = Column(String, ForeignKey('patients.id'))
    insurer_id = Column(String, ForeignKey('organizations.id'))
    status = Column(String(50))
    type_code = Column(String(50))
    type_display = Column(String(500))
    sub_type_code = Column(String(50))
    sub_type_display = Column(String(500))
    use = Column(String(50))
    created = Column(DateTime)
    total = Column(DECIMAL(18,2))
    import_date = Column(DateTime, default=datetime.utcnow)

    patient = relationship("Patient", back_populates="claims")
    insurer = relationship("Organization", back_populates="claims")

from typing import Dict, Any, List
from refiner.models.refined import Base, UserRefined, StorageMetric, AuthSource, Patient
from refiner.models.unrefined import GoogleProfileFHIRPatient, PatientResource
from refiner.transformer.base_transformer import DataTransformer
from refiner.utils.date import parse_timestamp
from refiner.utils.pii import mask_email


class UserTransformer(DataTransformer):
    """
    Transformer for Google Profile + FHIR Patient Bundle
    into refined SQLAlchemy models.
    """
    
    def transform(self, data: Dict[str, Any]) -> List[Base]:
        """
        Transform raw user data into SQLAlchemy model instances.
        
        Args:
            data: Dictionary containing user data + FHIR patient bundle
            
        Returns:
            List of SQLAlchemy model instances
        """
        # Validate data against Pydantic schema
        bundle = GoogleProfileFHIRPatient.model_validate(data)
        created_at = parse_timestamp(bundle.timestamp)
        
        # -----------------------------
        # User Profile
        # -----------------------------
        user = UserRefined(
            user_id=bundle.userId,
            email=mask_email(bundle.email),
            name=bundle.profile.name,
            locale=bundle.profile.locale,
            created_at=created_at
        )
        
        models: List[Base] = [user]
        
        if bundle.storage:
            storage_metric = StorageMetric(
                user_id=bundle.userId,
                percent_used=bundle.storage.percentUsed,
                recorded_at=created_at
            )
            models.append(storage_metric)
        
        if bundle.metadata:
            collection_date = parse_timestamp(bundle.metadata.collectionDate)
            auth_source = AuthSource(
                user_id=bundle.userId,
                source=bundle.metadata.source,
                collection_date=collection_date,
                data_type=bundle.metadata.dataType
            )
            models.append(auth_source)

        # -----------------------------
        # Patient Resource(s) in Bundle
        # -----------------------------
        for entry in bundle.entry:
            if entry.resource and entry.resource.resourceType == "Patient":
                patient: PatientResource = entry.resource

                patient_model = Patient(
                    id=patient.id,
                    resource_id=patient.id,
                    first_name=(
                        patient.name[0].given[0]
                        if patient.name and patient.name[0].given
                        else None
                    ),
                    last_name=(
                        patient.name[0].family
                        if patient.name and patient.name[0].family
                        else None
                    ),
                    prefix=(
                        patient.name[0].prefix[0]
                        if patient.name and patient.name[0].prefix
                        else None
                    ),
                    gender=patient.gender,
                    birth_date=patient.birthDate,
                    deceased_date_time=patient.deceasedDateTime,
                    marital_status=(
                        patient.maritalStatus.coding[0].code
                        if patient.maritalStatus and patient.maritalStatus.coding
                        else None
                    ),
                    multiple_birth_boolean=patient.multipleBirthBoolean,
                    # optional: flatten address
                    address_line=",".join(patient.address[0].line)
                        if patient.address and patient.address[0].line else None,
                    address_city=patient.address[0].city if patient.address else None,
                    address_state=patient.address[0].state if patient.address else None,
                    address_postal_code=patient.address[0].postalCode if patient.address else None,
                    address_country=patient.address[0].country if patient.address else None,
                    import_date=created_at,
                )

                models.append(patient_model)

        return models

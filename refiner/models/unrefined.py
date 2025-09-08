from typing import List, Literal, Optional, Union
from pydantic import BaseModel
from datetime import datetime, date

# ---------------------------------------------------
# Google Profile Wrapper
# ---------------------------------------------------
class Profile(BaseModel):
    name: str
    locale: str

class Storage(BaseModel):
    percentUsed: float

class Metadata(BaseModel):
    source: str
    collectionDate: str
    dataType: str

# ---------------------------------------------------
# FHIR Common Types
# ---------------------------------------------------
class Coding(BaseModel):
    system: Optional[str] = None
    code: Optional[str] = None
    display: Optional[str] = None

class CodeableConcept(BaseModel):
    coding: Optional[List[Coding]] = None
    text: Optional[str] = None

class Extension(BaseModel):
    url: str
    valueCodeableConcept: Optional[CodeableConcept] = None
    valueString: Optional[str] = None
    valueCode: Optional[str] = None
    valueDecimal: Optional[float] = None
    valueAddress: Optional[dict] = None
    extension: Optional[List["Extension"]] = None

class IdentifierType(BaseModel):
    coding: Optional[List[Coding]] = None

class Identifier(BaseModel):
    system: Optional[str] = None
    value: Optional[str] = None
    type: Optional[IdentifierType] = None

class HumanName(BaseModel):
    use: Optional[str] = None
    family: Optional[Union[str, List[str]]] = None
    given: Optional[List[str]] = None
    prefix: Optional[List[str]] = None

class Telecom(BaseModel):
    system: Optional[str] = None
    value: Optional[str] = None
    use: Optional[str] = None

class Address(BaseModel):
    line: Optional[List[str]] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postalCode: Optional[str] = None
    country: Optional[str] = None

class MaritalStatus(BaseModel):
    coding: Optional[List[Coding]] = None
    text: Optional[str] = None

class Communication(BaseModel):
    language: Optional[CodeableConcept] = None

class Narrative(BaseModel):
    status: Optional[str] = None
    div: Optional[str] = None

# ---------------------------------------------------
# FHIR Resource Variants
# ---------------------------------------------------
class PatientResource(BaseModel):
    resourceType: Literal["Patient"]
    id: str
    text: Optional[Narrative] = None
    extension: Optional[List[Extension]] = None
    identifier: Optional[List[Identifier]] = None
    name: Optional[List[HumanName]] = None
    telecom: Optional[List[Telecom]] = None
    gender: Optional[str] = None
    birthDate: Optional[date] = None
    deceasedDateTime: Optional[datetime] = None
    address: Optional[List[Address]] = None
    maritalStatus: Optional[MaritalStatus] = None
    multipleBirthBoolean: Optional[bool] = None
    communication: Optional[List[Communication]] = None

# Generic fallback for Encounter, Condition, etc.
class GenericResource(BaseModel):
    resourceType: str
    id: Optional[str] = None
    text: Optional[dict] = None
    extension: Optional[List[dict]] = None
    identifier: Optional[List[dict]] = None
    name: Optional[List[dict]] = None
    telecom: Optional[List[dict]] = None
    gender: Optional[str] = None
    birthDate: Optional[str] = None
    deceasedDateTime: Optional[str] = None
    address: Optional[List[dict]] = None
    maritalStatus: Optional[dict] = None
    multipleBirthBoolean: Optional[bool] = None
    communication: Optional[List[dict]] = None

# ---------------------------------------------------
# Bundle Entry
# ---------------------------------------------------
class Request(BaseModel):
    method: str
    url: str

class Entry(BaseModel):
    fullUrl: Optional[str] = None
    resource: Union[PatientResource, GenericResource]
    request: Optional[Request] = None

# ---------------------------------------------------
# Bundle Root (Google Profile + FHIR Bundle)
# ---------------------------------------------------
class GoogleProfileFHIRPatient(BaseModel):
    userId: str
    email: str
    timestamp: int
    profile: Profile
    storage: Optional[Storage] = None
    metadata: Metadata
    resourceType: Literal["Bundle"]
    type: Literal["transaction"]
    entry: List[Entry]

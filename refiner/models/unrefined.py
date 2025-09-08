from typing import Optional
from pydantic import BaseModel

from typing import List, Literal, Optional, Union
from pydantic import BaseModel, Field
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
# FHIR Patient Resource
# ---------------------------------------------------
class Coding(BaseModel):
    system: Optional[str]
    code: Optional[str]
    display: Optional[str]


class CodeableConcept(BaseModel):
    coding: Optional[List[Coding]]
    text: Optional[str]


class ExtensionInner(BaseModel):
    url: Optional[str]
    valueDecimal: Optional[float]


class Extension(BaseModel):
    url: str
    valueCodeableConcept: Optional[CodeableConcept] = None
    valueString: Optional[str] = None
    valueCode: Optional[str] = None
    valueDecimal: Optional[float] = None
    valueAddress: Optional[dict] = None
    extension: Optional[List["Extension"]] = None


class IdentifierType(BaseModel):
    coding: Optional[List[Coding]]


class Identifier(BaseModel):
    system: Optional[str]
    value: Optional[str]
    type: Optional[IdentifierType]


class HumanName(BaseModel):
    use: Optional[str]
    family: Optional[Union[str, List[str]]]
    given: Optional[List[str]]
    prefix: Optional[List[str]]


class Telecom(BaseModel):
    system: Optional[str]
    value: Optional[str]
    use: Optional[str]


class Address(BaseModel):
    line: Optional[List[str]]
    city: Optional[str]
    state: Optional[str]
    postalCode: Optional[str]
    country: Optional[str]


class MaritalStatus(BaseModel):
    coding: Optional[List[Coding]]


class Communication(BaseModel):
    language: Optional[CodeableConcept]


class Narrative(BaseModel):
    status: Optional[str]
    div: Optional[str]


class PatientResource(BaseModel):
    resourceType: str
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


# ---------------------------------------------------
# Bundle Entry
# ---------------------------------------------------
class Request(BaseModel):
    method: str
    url: str


class Entry(BaseModel):
    fullUrl: Optional[str]
    resource: Optional[PatientResource]
    request: Optional[Request]


# ---------------------------------------------------
# Bundle Root (Google Profile + FHIR Bundle)
# ---------------------------------------------------
class GoogleProfileFHIRPatient(BaseModel):
    userId: str
    email: str
    timestamp: int
    profile: Profile
    storage: Optional[Storage]
    metadata: Metadata
    resourceType: Literal["Bundle"]
    type: Literal["transaction"]
    entry: List[Entry]

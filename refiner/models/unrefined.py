from typing import Optional
from pydantic import BaseModel




from typing import List, Optional, Union
from pydantic import BaseModel, EmailStr, Field
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
    url: Optional[str]
    valueCodeableConcept: Optional[CodeableConcept]
    valueString: Optional[str]
    valueCode: Optional[str]
    valueDecimal: Optional[float]
    valueAddress: Optional[dict]
    extension: Optional[List[ExtensionInner]]


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
    text: Optional[Narrative]
    extension: Optional[List[Extension]]
    identifier: Optional[List[Identifier]]
    name: Optional[List[HumanName]]
    telecom: Optional[List[Telecom]]
    gender: Optional[str]
    birthDate: Optional[date]
    deceasedDateTime: Optional[datetime]
    address: Optional[List[Address]]
    maritalStatus: Optional[MaritalStatus]
    multipleBirthBoolean: Optional[bool]
    communication: Optional[List[Communication]]


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
    email: EmailStr
    timestamp: int
    profile: Profile
    storage: Optional[Storage]
    metadata: Metadata
    resourceType: str = Field("Bundle", const=True)
    type: str = Field("transaction", const=True)
    entry: List[Entry]

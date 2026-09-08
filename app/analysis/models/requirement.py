from enum import Enum

from pydantic import BaseModel, Field


class RequirementType(str, Enum):
    FUNCTIONAL = "Functional"
    NON_FUNCTIONAL = "Non-Functional"
    BUSINESS_RULE = "Business Rule"
    ERROR_EXCEPTION = "Error/Exception"
    QA_SCOPE = "QA Scope"
    PAYMENT_STATUS = "Payment Status"
    USER_ROLE = "User Role"
    DATA_REQUIREMENT = "Data Requirement"
    DEPENDENCY = "Dependency"
    TRACEABILITY = "Traceability"


class RequirementClassification(str, Enum):
    EXPLICIT = "Explicit"
    INFERRED = "Inferred"
    AMBIGUOUS = "Ambiguous"
    MISSING = "Missing"


class Requirement(BaseModel):
    requirement_id: str = Field(
        ...,
        description="Unique requirement identifier."
    )

    title: str = Field(
        ...,
        description="Short requirement title."
    )

    description: str = Field(
        ...,
        description="Requirement description."
    )

    requirement_type: RequirementType

    classification: RequirementClassification

    source_document: str

    source_section: str

    source_page: int | None = None

    source_text: str = ""

    business_rules: list[str] = Field(
        default_factory=list
    )

    dependencies: list[str] = Field(
        default_factory=list
    )

    confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
        description="Confidence in the extracted requirement."
    )
class RequirementAnalysis(BaseModel):
    document_name: str = Field(
        ...,
        description="Name of the analyzed CRS document."
    )

    analysis_summary: str = Field(
        ...,
        description="High-level summary of the requirement analysis."
    )

    requirements: list[Requirement] = Field(
        default_factory=list,
        description="Requirements extracted from the CRS."
    )

    overall_confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
        description="Overall confidence in the analysis."
    )

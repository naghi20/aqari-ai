from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class PropertyType(StrEnum):
    APARTMENT = "apartment"
    VILLA = "villa"
    OFFICE = "office"
    LAND = "land"
    BUILDING = "building"


class TransactionType(StrEnum):
    RENT = "rent"
    SALE = "sale"


class ListingStatus(StrEnum):
    DRAFT = "draft"
    PENDING_REVIEW = "pending_review"
    APPROVED = "approved"
    EXPORTED = "exported"


class PropertyFeatures(BaseModel):
    """Checkbox-based amenities imported from Joomla property feature fields."""

    parking: bool = False
    garden: bool = False
    basement: bool = False

    private_pool: bool = False
    common_pool: bool = False
    gym: bool = False
    sauna: bool = False
    steam: bool = False

    balcony: bool = False
    internet: bool = False
    lift: bool = False
    storage: bool = False
    laundry_room: bool = False

    driver_room: bool = False
    maid_room: bool = False

    central_ac: bool = False
    split_ac: bool = False
    window_ac: bool = False

    security: bool = False


class PropertyInternalDetails(BaseModel):
    """Private information excluded from AI context and public property data."""

    landlord: str | None = Field(default=None, max_length=250)
    watchman: str | None = Field(default=None, max_length=250)
    full_address: str | None = Field(default=None, max_length=1000)


class PropertyDraftCreate(BaseModel):
    """Validated input for creation of an AQARI AI property draft."""

    model_config = ConfigDict(str_strip_whitespace=True)

    reference_code: str = Field(
        min_length=3,
        max_length=64,
        pattern=r"^[A-Za-z0-9_-]+$",
        examples=["BH-JUF-0001"],
    )
    property_type: PropertyType
    transaction_type: TransactionType
    location: str = Field(min_length=2, max_length=100, examples=["Juffair"])
    price_bhd: Decimal = Field(
        gt=0,
        max_digits=12,
        decimal_places=3,
        examples=[550],
    )

    bedrooms: int | None = Field(default=None, ge=0, le=30)
    bathrooms: int | None = Field(default=None, ge=0, le=30)
    area_sqm: Decimal | None = Field(
        default=None,
        gt=0,
        max_digits=12,
        decimal_places=2,
    )

    furnished: bool | None = None

    # Existing AQARI field retained for backward compatibility.
    parking: bool | None = None

    # New normalized Joomla checkbox feature group.
    features: PropertyFeatures = Field(default_factory=PropertyFeatures)

    # Existing verified free-text list retained for compatibility.
    verified_features: list[str] = Field(default_factory=list, max_length=30)

    # Joomla or legacy fields not yet modeled as first-class AQARI fields.
    extra_features: dict[str, str | int | float | bool | None] = Field(
        default_factory=dict,
    )

    # Private data excluded from public data and AI prompts.
    internal_details: PropertyInternalDetails | None = None
    internal_notes: str | None = Field(default=None, max_length=1000)

    @field_validator("location")
    @classmethod
    def normalise_location(cls, value: str) -> str:
        return " ".join(word.capitalize() for word in value.split())

    @field_validator("verified_features")
    @classmethod
    def clean_features(cls, features: list[str]) -> list[str]:
        cleaned_features = []
        seen_features = set()

        for feature in features:
            normalised = " ".join(feature.split()).lower()

            if not normalised or normalised in seen_features:
                continue

            cleaned_features.append(normalised)
            seen_features.add(normalised)

        return cleaned_features

    @model_validator(mode="after")
    def validate_property_draft(self) -> "PropertyDraftCreate":
        residential_types = {PropertyType.APARTMENT, PropertyType.VILLA}

        if self.property_type in residential_types and self.bedrooms is None:
            raise ValueError("bedrooms is required for apartments and villas")

        if self.property_type in residential_types and self.bathrooms is None:
            raise ValueError("bathrooms is required for apartments and villas")

        parking_was_sent_in_features = (
            "features" in self.model_fields_set and "parking" in self.features.model_fields_set
        )

        if self.parking is None and parking_was_sent_in_features:
            self.parking = self.features.parking

        if self.parking is not None and not parking_was_sent_in_features:
            self.features.parking = self.parking

        if (
            self.parking is not None
            and parking_was_sent_in_features
            and self.parking != self.features.parking
        ):
            raise ValueError(
                "parking and features.parking must have the same value when both are provided"
            )

        return self


class PropertyDraft(PropertyDraftCreate):
    listing_status: ListingStatus = ListingStatus.DRAFT

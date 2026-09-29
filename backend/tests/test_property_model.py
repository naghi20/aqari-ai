from decimal import Decimal

import pytest
from aqari_ai.models.property import PropertyDraftCreate
from pydantic import ValidationError


def test_property_draft_normalises_location_and_features() -> None:
    property_draft = PropertyDraftCreate(
        reference_code="BH-JUF-0001",
        property_type="apartment",
        transaction_type="rent",
        location="  juffair  ",
        price_bhd=Decimal("550.000"),
        bedrooms=2,
        bathrooms=2,
        furnished=True,
        parking=True,
        verified_features=[" Balcony ", "balcony", "Gym Access"],
    )

    assert property_draft.location == "Juffair"
    assert property_draft.verified_features == ["balcony", "gym access"]


def test_apartment_requires_bedrooms_and_bathrooms() -> None:
    with pytest.raises(ValidationError, match="bedrooms is required"):
        PropertyDraftCreate(
            reference_code="BH-JUF-0002",
            property_type="apartment",
            transaction_type="rent",
            location="Juffair",
            price_bhd=Decimal("450.000"),
        )


def test_reference_code_rejects_spaces() -> None:
    with pytest.raises(ValidationError):
        PropertyDraftCreate(
            reference_code="BH JUF 0003",
            property_type="villa",
            transaction_type="sale",
            location="Seef",
            price_bhd=Decimal("180000.000"),
            bedrooms=4,
            bathrooms=4,
        )

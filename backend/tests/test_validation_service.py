from decimal import Decimal

from aqari_ai.models.property import PropertyDraftCreate
from aqari_ai.services.validation_service import build_verified_property_context


def test_verified_context_excludes_internal_notes() -> None:
    property_draft = PropertyDraftCreate(
        reference_code="BH-SEE-0001",
        property_type="office",
        transaction_type="rent",
        location="Seef",
        price_bhd=Decimal("800.000"),
        area_sqm=Decimal("95.50"),
        verified_features=["reception area"],
        internal_notes="This must never be included in an AI prompt.",
    )

    context = build_verified_property_context(property_draft)

    assert context["location"] == "Seef"
    assert context["area_sqm"] == "95.50"
    assert "internal_notes" not in context

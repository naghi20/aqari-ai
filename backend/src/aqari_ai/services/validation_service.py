from aqari_ai.models.property import PropertyDraftCreate


def build_verified_property_context(property_draft: PropertyDraftCreate) -> dict[str, object]:
    """Return only verified property fields that are safe to send to an AI prompt."""

    context: dict[str, object] = {
        "reference_code": property_draft.reference_code,
        "property_type": property_draft.property_type.value,
        "transaction_type": property_draft.transaction_type.value,
        "location": property_draft.location,
        "price_bhd": str(property_draft.price_bhd),
        "verified_features": property_draft.verified_features,
    }

    optional_fields = {
        "bedrooms": property_draft.bedrooms,
        "bathrooms": property_draft.bathrooms,
        "area_sqm": str(property_draft.area_sqm) if property_draft.area_sqm else None,
        "furnished": property_draft.furnished,
        "parking": property_draft.parking,
    }

    context.update(
        {
            field_name: field_value
            for field_name, field_value in optional_fields.items()
            if field_value is not None
        }
    )

    return context

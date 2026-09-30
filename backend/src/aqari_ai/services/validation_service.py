from aqari_ai.models.property import PropertyDraftCreate


def build_verified_property_context(property_draft: PropertyDraftCreate) -> dict[str, object]:
    """Return verified property fields that are safe to send to an AI prompt.

    This context deliberately excludes:
    - internal_notes
    - landlord details
    - watchman details
    - full exact address
    """

    feature_flags = property_draft.features.model_dump()

    enabled_checkbox_features = [
        feature_name.replace("_", " ")
        for feature_name, is_enabled in feature_flags.items()
        if is_enabled
    ]

    verified_features = list(property_draft.verified_features)

    for feature_name in enabled_checkbox_features:
        if feature_name not in verified_features:
            verified_features.append(feature_name)

    context: dict[str, object] = {
        "reference_code": property_draft.reference_code,
        "property_type": property_draft.property_type.value,
        "transaction_type": property_draft.transaction_type.value,
        "location": property_draft.location,
        "price_bhd": str(property_draft.price_bhd),
        "verified_features": verified_features,
        "features": feature_flags,
        "enabled_features": enabled_checkbox_features,
    }

    optional_fields = {
        "bedrooms": property_draft.bedrooms,
        "bathrooms": property_draft.bathrooms,
        "area_sqm": str(property_draft.area_sqm) if property_draft.area_sqm else None,
        "furnished": property_draft.furnished,
        "parking": property_draft.parking,
        "extra_features": property_draft.extra_features or None,
    }

    context.update(
        {
            field_name: field_value
            for field_name, field_value in optional_fields.items()
            if field_value is not None
        }
    )

    return context

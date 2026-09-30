from decimal import Decimal

import pytest
from aqari_ai.models.property import PropertyDraftCreate
from aqari_ai.services.validation_service import build_verified_property_context
from pydantic import ValidationError


def test_joomla_checkbox_features_are_stored_and_added_to_ai_context() -> None:
    property_draft = PropertyDraftCreate(
        reference_code="BH-JUF-FEATURES-001",
        property_type="villa",
        transaction_type="rent",
        location="juffair",
        price_bhd=Decimal("1800.000"),
        bedrooms=4,
        bathrooms=4,
        features={
            "parking": True,
            "garden": True,
            "private_pool": True,
            "balcony": True,
            "maid_room": True,
            "central_ac": True,
            "security": True,
        },
    )

    context = build_verified_property_context(property_draft)

    assert property_draft.location == "Juffair"
    assert property_draft.parking is True
    assert property_draft.features.parking is True
    assert property_draft.features.garden is True
    assert property_draft.features.private_pool is True
    assert property_draft.features.central_ac is True
    assert property_draft.features.common_pool is False

    assert context["features"]["garden"] is True
    assert context["features"]["common_pool"] is False

    assert "garden" in context["enabled_features"]
    assert "private pool" in context["enabled_features"]
    assert "central ac" in context["enabled_features"]

    assert "maid room" in context["verified_features"]
    assert "private pool" in context["verified_features"]
    assert "security" in context["verified_features"]


def test_legacy_parking_value_syncs_to_new_checkbox_features() -> None:
    property_draft = PropertyDraftCreate(
        reference_code="BH-JUF-PARKING-001",
        property_type="apartment",
        transaction_type="rent",
        location="Juffair",
        price_bhd=Decimal("550.000"),
        bedrooms=2,
        bathrooms=2,
        parking=True,
    )

    assert property_draft.parking is True
    assert property_draft.features.parking is True


def test_conflicting_legacy_and_checkbox_parking_is_rejected() -> None:
    with pytest.raises(
        ValidationError,
        match="parking and features.parking must have the same value",
    ):
        PropertyDraftCreate(
            reference_code="BH-JUF-PARKING-002",
            property_type="apartment",
            transaction_type="rent",
            location="Juffair",
            price_bhd=Decimal("550.000"),
            bedrooms=2,
            bathrooms=2,
            parking=False,
            features={"parking": True},
        )


def test_internal_details_are_not_in_ai_context_or_property_data(monkeypatch) -> None:
    from types import SimpleNamespace

    from aqari_ai.handlers import create_property

    class FakeTable:
        def __init__(self) -> None:
            self.items: list[dict] = []

        def put_item(self, **kwargs: object) -> None:
            self.items.append(kwargs)

    fake_table = FakeTable()

    monkeypatch.setattr(create_property, "get_properties_table", lambda: fake_table)

    event = {
        "property": {
            "reference_code": "BH-SEE-PRIVATE-001",
            "property_type": "office",
            "transaction_type": "rent",
            "location": "Seef",
            "price_bhd": 800,
            "internal_details": {
                "landlord": "Private landlord",
                "watchman": "Private watchman",
                "full_address": "Private exact address",
            },
            "internal_notes": "Private internal note.",
        }
    }

    response = create_property.lambda_handler(
        event=event,
        context=SimpleNamespace(aws_request_id="private-details-test"),
    )

    written_item = fake_table.items[0]["Item"]

    assert response["statusCode"] == 201
    assert "internal_notes" not in written_item["property_data"]
    assert "internal_details" not in written_item["property_data"]
    assert "internal_notes" not in written_item["verified_ai_context"]
    assert "internal_details" not in written_item["verified_ai_context"]
    assert "landlord" not in written_item["verified_ai_context"]
    assert "watchman" not in written_item["verified_ai_context"]
    assert "full_address" not in written_item["verified_ai_context"]

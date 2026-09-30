import json
from decimal import Decimal
from types import SimpleNamespace

from aqari_ai.handlers import create_property


class FakeTable:
    def __init__(self) -> None:
        self.items: list[dict] = []

    def put_item(self, **kwargs: object) -> None:
        self.items.append(kwargs)


def test_create_property_draft_returns_created_response(monkeypatch) -> None:
    fake_table = FakeTable()

    monkeypatch.setenv("AQARI_PROPERTIES_TABLE_NAME", "aqari-ai-properties-dev")
    monkeypatch.setattr(create_property, "get_properties_table", lambda: fake_table)

    context = SimpleNamespace(aws_request_id="test-create-property-request")

    event = {
        "property": {
            "reference_code": "BH-JUF-TEST-001",
            "property_type": "apartment",
            "transaction_type": "rent",
            "location": "juffair",
            "price_bhd": Decimal("550.000"),
            "bedrooms": 2,
            "bathrooms": 2,
            "area_sqm": Decimal("120.00"),
            "furnished": True,
            "parking": True,
            "verified_features": [
                "balcony",
                "gym access",
            ],
            "internal_notes": "This text must not be stored in the draft record.",
        }
    }

    response = create_property.lambda_handler(event=event, context=context)
    response_body = json.loads(response["body"])

    assert response["statusCode"] == 201
    assert response_body["message"] == "Property draft created"
    assert response_body["listing_status"] == "draft"
    assert response_body["generation_status"] == "not_requested"
    assert response_body["export_status"] == "not_requested"
    assert response_body["request_id"] == "test-create-property-request"
    assert response_body["property_id"].startswith("PROP-")

    assert len(fake_table.items) == 1

    written_item = fake_table.items[0]["Item"]

    assert written_item["property_data"]["location"] == "Juffair"
    assert written_item["property_data"]["price_bhd"] == Decimal("550.000")
    assert "internal_notes" not in written_item["property_data"]
    assert written_item["verified_ai_context"]["location"] == "Juffair"
    assert written_item["verified_ai_context"]["price_bhd"] == "550.000"


def test_create_property_draft_returns_validation_error() -> None:
    context = SimpleNamespace(aws_request_id="invalid-property-request")

    event = {
        "property": {
            "reference_code": "INVALID REFERENCE",
            "property_type": "apartment",
            "transaction_type": "rent",
            "location": "Juffair",
            "price_bhd": 550,
        }
    }

    response = create_property.lambda_handler(event=event, context=context)
    response_body = json.loads(response["body"])

    assert response["statusCode"] == 400
    assert response_body["message"] == "Invalid property draft payload"
    assert response_body["request_id"] == "invalid-property-request"
    assert response_body["errors"]

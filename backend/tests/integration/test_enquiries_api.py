"""
tests/integration/test_enquiries_api.py
Integration tests for the enquiries API endpoints, using a real
(but isolated, temporary) test database via the `client` fixture.
"""


def test_create_enquiry_success(client):
    payload = {
        "enquiry_text": "We need a chatbot for our ecommerce store, budget around 6 lakh, needed urgently",
        "industry": "E-commerce",
        "budget_inr": 600000,
        "urgency_hint": "High",
    }
    response = client.post("/api/v1/enquiries", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["predicted_category"] in {
        "Website Development", "E-commerce Development", "Training/Courses",
        "Data Analytics", "Chatbot", "Mobile App", "AI/ML Solution", "Automation"
    }
    assert data["predicted_priority"] == "High"
    assert "insight" in data
    assert data["id"] is not None


def test_create_enquiry_fails_with_short_text(client):
    payload = {"enquiry_text": "hi"}
    response = client.post("/api/v1/enquiries", json=payload)
    assert response.status_code == 422  # Pydantic validation error


def test_create_enquiry_fails_with_invalid_urgency(client):
    payload = {
        "enquiry_text": "We need a website redesign for our company soon",
        "urgency_hint": "Super Urgent",
    }
    response = client.post("/api/v1/enquiries", json=payload)
    assert response.status_code == 422


def test_list_enquiries_returns_created_item(client):
    payload = {"enquiry_text": "Looking for data analytics dashboard for our sales team"}
    create_resp = client.post("/api/v1/enquiries", json=payload)
    assert create_resp.status_code == 201

    list_resp = client.get("/api/v1/enquiries")
    assert list_resp.status_code == 200
    items = list_resp.json()
    assert len(items) >= 1


def test_get_enquiry_by_id(client):
    payload = {"enquiry_text": "We want to automate our invoice processing workflow"}
    create_resp = client.post("/api/v1/enquiries", json=payload)
    created_id = create_resp.json()["id"]

    get_resp = client.get(f"/api/v1/enquiries/{created_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["id"] == created_id


def test_get_enquiry_returns_404_for_missing_id(client):
    response = client.get("/api/v1/enquiries/999999")
    assert response.status_code == 404


def test_filter_enquiries_by_priority(client):
    client.post("/api/v1/enquiries", json={
        "enquiry_text": "Urgent mobile app needed, huge budget",
        "budget_inr": 900000,
        "urgency_hint": "High",
    })

    response = client.get("/api/v1/enquiries?priority=High")
    assert response.status_code == 200
    for item in response.json():
        assert item["predicted_priority"] == "High"


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

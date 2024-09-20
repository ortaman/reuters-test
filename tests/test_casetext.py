
from fastapi.testclient import TestClient

from app.main import app
from app.reuters.router import DMSApi


client = TestClient(app)


def test_get_casetext_sync_with_parameters():
    response = client.get("/casetext_sync")
    assert response.status_code == 422



def test_get_casetext_sync_with_wrong_parameters():
    response = client.get("/casetext_sync/?start_date=11-11&end_date=2011-11")
    assert response.status_code == 422


def test_get_casetext(mocker):
    mock_responses = [ """
        {"id": "67e5e9ed-baab-49f7-8290-1e9885ba8fa0", "name": "msj-a", "meta": {"matter": "uber"}}
        {"id": "2b89256a-ae91-420a-ac0b-35b36e45fa4f", "name": "mtd", "meta": {"cat": "old"}}
        {"id": "3b6b7a0e-a16d-4d2c-a2ae-670efcf444a3", "name": "depo","meta": {}}
    """,
    """
        {"id": "67e5e9ed-baab-49f7-8290-1e9885ba8fa0", "name": "msj-a FINAL", "meta": {"matter": "uber"}}
        {"id": "2b89256a-ae91-420a-ac0b-35b36e45fa4f", "name": "mtd", "meta": {"cat": "old", "deleteSoon": true}}
        {"id": "8e1fe401-f031-46be-9437-f00273baca1c", "name": "msj-b", "meta": {}}
    """
    ]

    mocker.patch.object(DMSApi, "get_content_file", side_effect = mock_responses)

    response = client.get("/casetext_sync/?start_date=2011-11-11&end_date=2011-11-11")
    assert response.status_code == 200

    assert response.json() == {
        "createFile": [{"id":"8e1fe401-f031-46be-9437-f00273baca1c","name":"msj-b","meta":{}}],
        "deleteFile": [{"id":"3b6b7a0e-a16d-4d2c-a2ae-670efcf444a3"}],
        "updateFileName": [{"id":"67e5e9ed-baab-49f7-8290-1e9885ba8fa0","name":"msj-a FINAL"}],
        "updateFileMeta": [{"id":"2b89256a-ae91-420a-ac0b-35b36e45fa4f","meta":{"cat":"old","deleteSoon":True}}]
    }

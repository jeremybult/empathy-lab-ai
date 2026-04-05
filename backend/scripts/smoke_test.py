from fastapi.testclient import TestClient

from app.main import app


def main() -> None:
    client = TestClient(app)

    root_resp = client.get('/')
    assert root_resp.status_code == 200, root_resp.text

    health_resp = client.get('/health')
    assert health_resp.status_code == 200, health_resp.text

    personas_resp = client.get('/api/personas')
    assert personas_resp.status_code == 200, personas_resp.text
    personas = personas_resp.json().get('personas', [])
    assert isinstance(personas, list) and len(personas) > 0

    chat_blank_resp = client.post('/api/chat', json={'persona_id': 'andrea_miller', 'message': '   '})
    assert chat_blank_resp.status_code == 400, chat_blank_resp.text

    chat_demo_resp = client.post('/api/chat', json={'persona_id': 'andrea_miller', 'message': 'hello'})
    assert chat_demo_resp.status_code in {200, 502}, chat_demo_resp.text

    reset_resp = client.post('/api/reset', json={'persona_id': 'andrea_miller'})
    assert reset_resp.status_code == 200, reset_resp.text

    print('Backend smoke test passed.')


if __name__ == '__main__':
    main()



def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "<button>Login</button>" in str(response.data)


def test_dashboard_unauthorized(client):
    response = client.get("/dashboard")
    assert response.status_code == 401


def test_dashboard(client, mocker):
    obj = mocker.patch.dict('utils.session', {'k': 'v'})
    response = client.get("/dashboard")
    # TODO assert the response

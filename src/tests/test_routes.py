from auth.data_validation import checkPassword

def testChatRedirectsWhenLoggedOut(client):
    response = client.get("/chat")
    assert response.status_code == 302
    assert response.headers["Location"] == "/"

def testRegisterMissingFields(client):
    response = client.post("/register", json={})
    data = response.get_json()

    assert response.status_code == 400
    assert data["success"] is False
    assert data["message"] == "Missing Fields"

def testLoginMissingFields(client):
    response = client.post("/login", json={})
    data = response.get_json()

    assert response.status_code == 400
    assert data["success"] is False
    assert data["message"] == "Missing Fields"

def testSuccessfulRegisterRoute(client):
    body = {"email": "user@example.com", 
            "password": "password123!", 
            "confirmPassword": "password123!"}
    
    response = client.post("/register", json=body)
    data = response.get_json()

    assert response.status_code == 200
    assert data["success"] is True
    assert data["message"] == "Registration Successful"

def testSuccessfulLoginRoute(client, user):

    body = {"email": "user@example.com",
            "password": "password123!"}

    response = client.post("/login", json=body)
    data = response.get_json()

    assert response.status_code == 200
    assert data["success"] is True
    assert data["message"] == "Login Successful"

    with client.session_transaction() as session:
        assert session["email"] == "user@example.com"

def testChatAfterLoginRoute(client, user):

    body = {"email": "user@example.com",
            "password": "password123!"}
    
    client.post("/login", json=body)
    response = client.get("/chat")

    assert response.status_code == 200

def testFailedLoginRoute(client, user):
        
    body = {"email": "user@example.com",
            "password": "incorrectpassword"}
        
    loginResponse = client.post("/login", json=body)
    response = client.get("/chat")
    
    assert loginResponse.get_json()["success"] is False
    assert response.status_code == 302
    assert response.headers["Location"] == "/"

    with client.session_transaction() as session:
        assert "email" not in session

def testRandomPasswordRoute(client):
    response = client.get("/generate-password")
    password = response.get_json()["password"]

    assert response.status_code == 200
    assert checkPassword(password) is True

def testSessionEmailNormalised(client, user):

    body = {"email": " USER@Example.com", 
            "password": "password123!"}
    
    client.post("/login", json=body)

    with client.session_transaction() as session:
        assert session["email"] == "user@example.com"
    
    
    
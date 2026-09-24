from backend.api.services.auth.client.models.login_response import LoginResponse


def test_login_response_accepts_null_email():
    response = LoginResponse(
        user={
            "id": "8cbabbe9-5fff-4dbe-a77e-104bf4e63dbe",
            "login": "student_1",
            "email": None,
            "fullName": "student_1",
            "createdAt": "2026-09-24T12:00:00.000Z",
            "verified": True,
            "banned": False,
            "roles": ["USER"],
        },
        accessToken="token",
        expiresIn=3600,
    )

    assert response.user.email is None

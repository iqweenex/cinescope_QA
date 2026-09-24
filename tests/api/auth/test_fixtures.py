from uuid import UUID


def test_user_data_factory_uses_uuid(user_data_factory):
    data = user_data_factory()
    email_local, email_domain = data["email"].split("@", maxsplit=1)

    UUID(data["login"])
    UUID(email_local)
    assert email_domain == "example.com"

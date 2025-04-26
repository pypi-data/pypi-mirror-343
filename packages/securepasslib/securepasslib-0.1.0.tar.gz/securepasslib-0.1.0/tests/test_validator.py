from securepasslib import validator

def test_valid_password():
    pwd = "Aa1!aaaa"
    assert validator.is_strong(pwd)

def test_invalid_password():
    pwd = "1234"
    assert not validator.is_strong(pwd)
    assert "Password is too short." in validator.validate(pwd)
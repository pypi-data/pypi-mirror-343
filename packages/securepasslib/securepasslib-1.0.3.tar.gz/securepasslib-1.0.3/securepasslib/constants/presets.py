from securepasslib.policy import PasswordPolicy

# Predefined password security levels
BASIC_POLICY = PasswordPolicy(
    min_length=8,
    min_uppercase=1,
    min_lowercase=1,
    min_digits=1,
    min_special=0
)

MEDIUM_POLICY = PasswordPolicy(
    min_length=10,
    min_uppercase=1,
    min_lowercase=1,
    min_digits=1,
    min_special=1
)

STRICT_POLICY = PasswordPolicy(
    min_length=12,
    min_uppercase=2,
    min_lowercase=2,
    min_digits=2,
    min_special=2
)

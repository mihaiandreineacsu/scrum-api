from typing import Any

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from phonenumber_field import validators as phonenumber_validators

DEFAULT_CHAR_FIELD_MIN_LENGTH = 3
DEFAULT_CHAR_FIELD_MAX_LENGTH = 50

DEFAULT_TEXT_FIELD_MIN_LENGTH = 10
DEFAULT_TEXT_FIELD_MAX_LENGTH = 500

ALPHA_NUMERIC_REGEX = r"^[A-Za-z0-9]+$"
LOWER_ALPHABETIC_REGEX = r"^[a-z]+$"
SPACING_REGEX = r"^\s+|\s+$|\s+(?=\s)"
EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"

ALPHANUMERIC_VALIDATOR_MESSAGE = "Must contain only letters, numbers, and spaces."
LOWER_ALPHABETIC_VALIDATOR_MESSAGE = "Must contain only lowercase letters."
SPACING_VALIDATOR_MESSAGE = "Leading, trailing, or consecutive spaces are not allowed."
EMAIL_REGEX_MESSAGE = "Invalid email address."


def generate_length_regex(
    min_length: int = DEFAULT_CHAR_FIELD_MIN_LENGTH,
    max_length: int = DEFAULT_CHAR_FIELD_MAX_LENGTH,
) -> str:
    """Generate a regex pattern for string length."""
    return rf"^.{{{min_length},{max_length}}}$"


def generate_choice_regex(choices: list[tuple[str, str]]) -> str:
    """Generate a regex pattern for choices."""
    return rf"^({'|'.join([choice[0] for choice in choices])})$"


def char_length_validator(
    message: str | None = None,
    code: str = "input_length_invalid",
    min_length: int = DEFAULT_CHAR_FIELD_MIN_LENGTH,
    max_length: int = DEFAULT_CHAR_FIELD_MAX_LENGTH,
) -> RegexValidator:
    """Create a RegexValidator for string length."""
    if not message:
        message = f"Must be between {min_length} and {max_length} characters long."
    return RegexValidator(
        regex=generate_length_regex(min_length, max_length),
        message=message,
        code=code,
    )


def text_length_validator(
    message: str | None = None,
    code: str = "input_text_length_invalid",
    min_length: int = DEFAULT_TEXT_FIELD_MIN_LENGTH,
    max_length: int = DEFAULT_TEXT_FIELD_MAX_LENGTH,
) -> RegexValidator:
    """Create a RegexValidator for text length."""
    return char_length_validator(message, code, min_length, max_length)


def alphanumeric_validator(
    message: str = ALPHANUMERIC_VALIDATOR_MESSAGE,
    code: str = "input_alphanumeric_invalid",
) -> RegexValidator:
    """Create a RegexValidator for alphanumeric strings with spaces."""
    return RegexValidator(
        regex=ALPHA_NUMERIC_REGEX,
        message=message,
        code=code,
    )


def lower_alphabetic_validator(
    message: str = LOWER_ALPHABETIC_VALIDATOR_MESSAGE,
    code: str = "input_lower_alphabetic_invalid",
) -> RegexValidator:
    """Create a RegexValidator for lowercase alphabetic strings."""
    return RegexValidator(
        regex=LOWER_ALPHABETIC_REGEX,
        message=message,
        code=code,
    )


def spacing_validator(
    message: str = SPACING_VALIDATOR_MESSAGE,
    code: str = "input_spacing_invalid",
) -> RegexValidator:
    """Create a RegexValidator for strings with normalized spacing."""
    return RegexValidator(
        regex=SPACING_REGEX,
        message=message,
        code=code,
        inverse_match=True,  # since we want to DISALLOW matches
    )


def email_validator(
    message: str = EMAIL_REGEX_MESSAGE,
    code: str = "input_email_invalid",
) -> RegexValidator:
    """Create a RegexValidator for email addresses."""
    return RegexValidator(
        regex=EMAIL_REGEX,
        message=message,
        code=code,
    )


def choice_validator(
    choices: list[tuple[str, str]],
    message: str = "Invalid choice.",
    code: str = "input_choice_invalid",
) -> RegexValidator:
    """Create a RegexValidator for choices."""
    return RegexValidator(
        regex=generate_choice_regex(choices),
        message=message,
        code=code,
    )


def validate_phonenumber(value: Any):
    try:
        phonenumber_validators.validate_international_phonenumber(value)
    except ValidationError:
        phonenumber_validators.validate_phonenumber(value)

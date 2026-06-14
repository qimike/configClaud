"""Tests for :mod:`src.api.sample_api`.

These tests demonstrate the standards in ``.claude/rules/testing-rules.md``:

* **AAA pattern** -- each test has clear Arrange / Act / Assert sections.
* **Behavioural names** -- test names describe the behaviour under test.
* **Mock external dependencies** -- the persistence layer is mocked so the
  controller logic can be tested in isolation.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException

# The API module lives at src/api/sample_api.py. Load it by path so the test is
# independent of how pytest is invoked (rootdir / sys.path differences).
_API_PATH = Path(__file__).resolve().parents[1] / "api" / "sample_api.py"
_spec = importlib.util.spec_from_file_location("sample_api", _API_PATH)
assert _spec is not None and _spec.loader is not None
sample_api = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sample_api)


def test_create_user_returns_typed_user_with_assigned_id() -> None:
    # Arrange
    service = sample_api.UserService()
    request = sample_api.CreateUserRequest(name="Ada", email="ada@example.com")

    # Act
    user = service.create_user(request)

    # Assert
    assert isinstance(user, sample_api.UserResponse)
    assert user.id == 1
    assert user.name == "Ada"


def test_create_user_rejects_duplicate_email() -> None:
    # Arrange
    service = sample_api.UserService()
    service.create_user(sample_api.CreateUserRequest(name="Ada", email="dup@example.com"))

    # Act / Assert
    with pytest.raises(ValueError, match="email already registered"):
        service.create_user(
            sample_api.CreateUserRequest(name="Grace", email="dup@example.com")
        )


def test_get_user_controller_maps_missing_user_to_404() -> None:
    # Arrange: mock the external service dependency so the controller is isolated.
    mock_service = MagicMock()
    mock_service.get_user.side_effect = KeyError("missing")
    original = sample_api.service
    sample_api.service = mock_service

    # Act / Assert
    try:
        with pytest.raises(HTTPException) as exc_info:
            sample_api.get_user(user_id=999)
        assert exc_info.value.status_code == 404
    finally:
        sample_api.service = original  # restore global to avoid test bleed-over


def test_create_user_controller_maps_duplicate_to_409() -> None:
    # Arrange
    mock_service = MagicMock()
    mock_service.create_user.side_effect = ValueError("email already registered")
    original = sample_api.service
    sample_api.service = mock_service
    request = sample_api.CreateUserRequest(name="Ada", email="ada@example.com")

    # Act / Assert
    try:
        with pytest.raises(HTTPException) as exc_info:
            sample_api.create_user(request)
        assert exc_info.value.status_code == 409
    finally:
        sample_api.service = original

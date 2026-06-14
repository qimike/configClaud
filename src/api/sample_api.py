"""Sample FastAPI service used to demonstrate Claude Code path-specific rules.

This module intentionally follows the standards declared in the project-level
``CLAUDE.md`` and the path-specific rules in ``.claude/rules/api-rules.md``:

* FastAPI is used as the web framework.
* All request bodies are validated with Pydantic models.
* Endpoints return typed response models.
* Controllers stay thin -- business logic lives in :class:`UserService`.
* Structured logging is used instead of ``print``.
* Functions stay small (well under 50 lines) and use type hints throughout.
"""

from __future__ import annotations

import logging
from typing import Dict

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# Structured logging: emit key=value pairs so logs are machine-parseable.
logging.basicConfig(
    level=logging.INFO,
    format="level=%(levelname)s logger=%(name)s msg=%(message)s",
)
logger = logging.getLogger("sample_api")

app = FastAPI(title="Sample API", version="1.0.0")


class CreateUserRequest(BaseModel):
    """Validated request body for creating a user."""

    name: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=3, max_length=255)


class UserResponse(BaseModel):
    """Typed response model returned by user endpoints."""

    id: int
    name: str
    email: str


class UserService:
    """Business logic for users.

    The service owns all state and rules so that the API controllers below
    contain no business logic (only request/response wiring). This favours
    composition: the controller *uses* a service rather than inheriting from it.
    """

    def __init__(self) -> None:
        self._users: Dict[int, UserResponse] = {}
        self._next_id: int = 1

    def create_user(self, request: CreateUserRequest) -> UserResponse:
        """Create and store a user, returning the typed response model.

        Args:
            request: The validated creation request.

        Returns:
            The newly created user as a :class:`UserResponse`.

        Raises:
            ValueError: If the email is already registered.
        """
        # Complex logic gets an inline comment: enforce email uniqueness.
        if any(user.email == request.email for user in self._users.values()):
            raise ValueError("email already registered")

        user = UserResponse(id=self._next_id, name=request.name, email=request.email)
        self._users[user.id] = user
        self._next_id += 1
        logger.info("user_created user_id=%s", user.id)
        return user

    def get_user(self, user_id: int) -> UserResponse:
        """Return the user for ``user_id`` or raise ``KeyError`` if absent."""
        return self._users[user_id]


service = UserService()


@app.post("/users", response_model=UserResponse, status_code=201)
def create_user(request: CreateUserRequest) -> UserResponse:
    """Controller: delegate to the service, translate errors to HTTP."""
    try:
        return service.create_user(request)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int) -> UserResponse:
    """Controller: fetch a user, mapping a missing user to a 404."""
    try:
        return service.get_user(user_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="user not found") from exc

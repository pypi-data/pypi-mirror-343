"""
Base http-response class.
"""

from __future__ import annotations

from importlib.util import find_spec

if FLASK_AVAILABLE := find_spec("flask") is not None:

    from typing import Any, Callable, Dict, Iterable, Optional, Tuple
    from flask import Response

    FlaskResponseType = (
        int |  # Status code only
        str |  # Response body as string
        bytes |  # Response body as bytes
        None |  # Empty response with default status code
        Dict[str, Any] |  # JSON-like response
        Response |  # Full Flask response object
        Tuple[Dict[str, Any], int] |  # JSON response with status code
        Tuple[str, int] |  # String response with status code
        Tuple[bytes, int] |  # Bytes response with status code
        Tuple[Dict[str, Any], int, Dict[str, str]] |  # JSON response + status + headers
        Tuple[str, int, Dict[str, str]] |  # String response + status + headers
        Tuple[bytes, int, Dict[str, str]] |  # Bytes response + status + headers
        Callable[[], Response | Iterable[bytes]]  # Streaming response
    )
    """
    FlaskResponseType:
    A type representing all possible response formats recognized by Flask route handlers.
    """

    if PYDANTIC_AVAILABLE := find_spec("pydantic") is not None:
        from pydantic import BaseModel, ConfigDict, Field, model_validator

        class HttpResponse(BaseModel):
            """
            Base class for all API responses success or Error.
            """

            model_config = ConfigDict(extra="forbid")
            """
            Pydantic object that restricts the response
            payload to contain only the applicable fields.
            """

            status_code: int = Field(default=0, ge=0, le=504)
            """
            The HTTP status code of the response.
            """

            headers: Dict[str, str] = Field(default_factory=dict)
            """
            Optional dictionary mapping of HTTP headers for the response.
            """

            message: Optional[str] = Field(default=None)
            """
            A message describing the response.
            """

            @model_validator(mode="after")
            def set_default_message(self) -> "HttpResponse":
                """
                Set default message based on status code if not provided.
                Only sets default for success responses (2xx).
                """
                if self.message is None and self.status_code == 200:
                    self.message = "OK"
                return self

            def get_response(self) -> FlaskResponseType:
                """
                Generates a status code and or response tuple for Flask, optionally
                including headers.

                :return: Returns some combination of a status code, response body, and
                response headers.
                """

                response_tuple: tuple[int] = (self.status_code,)  # Start with the status code

                # Create a dictionary of all fields except 'status_code' and 'headers'.
                response_body: Dict[str, Any] = self.model_dump(
                    exclude={"status_code", "headers"}
                )

                if response_body:
                    response_tuple: tuple[Dict[str, Any], int] = (response_body,) + response_tuple

                if self.headers:
                    response_tuple += (self.headers,)

                return (
                    response_tuple[0] if len(response_tuple) == 1
                    else response_tuple
                )

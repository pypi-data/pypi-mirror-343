import uuid

import pytest
import requests
import responses
from freezegun import freeze_time
from responses import matchers

from smoothintegration.exceptions import SIError


class TestRequest:

    def test_can_make_minimal_get_request(self, mocked_responses, test_client):
        mocked_responses.add(
            responses.GET,
            "https://api.smooth-integration.com/v1/request/9d952948-1697-4282-b2d0-e19ea0098723",
            json={
                "example": "response",
            },
            status=200,
        )

        response = test_client.request.make_request(
            uuid.UUID("9d952948-1697-4282-b2d0-e19ea0098723"),
        )
        assert response.status_code == 200
        assert response.json() == {"example": "response"}

    def test_can_pass_query_parameters(self, mocked_responses, test_client):
        mocked_responses.add(
            responses.GET,
            "https://api.smooth-integration.com/v1/request/9d952948-1697-4282-b2d0-e19ea0098723?foo=bar",
            json={
                "example": "response",
            },
            status=200,
        )

        response = test_client.request.make_request(
            uuid.UUID("9d952948-1697-4282-b2d0-e19ea0098723"),
            params={"foo": "bar"},
        )
        assert response.status_code == 200
        assert response.json() == {"example": "response"}

    @freeze_time("2025-03-20 12:00:00", tz_offset=0)
    def test_can_pass_headers(self, mocked_responses, test_client):
        mocked_responses.add(
            responses.GET,
            "https://api.smooth-integration.com/v1/request/9d952948-1697-4282-b2d0-e19ea0098723",
            match=[
                matchers.header_matcher(
                    {
                        "foo": "bar",
                        # The headers produced by the http utility should remain
                        "X-Organisation": "a4a0a676-a645-4efc-bf1e-6f98631ae204",
                        "X-Timestamp": "2025-03-20T12:00:00.000Z",
                        "X-Signature": "3163b80e50a3276c2adc9c77b0a5c570a2af29243c21a0f296ad040f4ba1b7ec",
                    }
                )],
            json={
                "example": "response",
            },
            status=200,
        )

        response = test_client.request.make_request(
            uuid.UUID("9d952948-1697-4282-b2d0-e19ea0098723"),
            headers={"foo": "bar"},
        )
        assert response.status_code == 200
        assert response.json() == {"example": "response"}

    def test_can_make_post_request_with_body(self, mocked_responses, test_client):
        mocked_responses.add(
            responses.POST,
            "https://api.smooth-integration.com/v1/request/9d952948-1697-4282-b2d0-e19ea0098723",
            match=[matchers.json_params_matcher({"foo": "bar"})],
            json={
                "example": "response",
            },
            status=200,
        )

        response = test_client.request.make_request(
            uuid.UUID("9d952948-1697-4282-b2d0-e19ea0098723"),
            method="POST",
            json={"foo": "bar"},
        )
        assert response.status_code == 200
        assert response.json() == {"example": "response"}

    def test_returns_responses_as_is(self, mocked_responses, test_client):
        mocked_responses.add(
            responses.GET,
            "https://api.smooth-integration.com/v1/request/9d952948-1697-4282-b2d0-e19ea0098723",
            json={
                "error": "Internal Server Error",
            },
            status=500,
        )

        # Making the request should return the response as is, without raising any exceptions
        response = test_client.request.make_request(
            uuid.UUID("9d952948-1697-4282-b2d0-e19ea0098723"),
        )
        assert response.status_code == 500
        assert response.json() == {"error": "Internal Server Error"}

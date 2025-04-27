import asyncio
import pytest
import pytest_asyncio
from crypticorn.common import AuthHandler, BaseUrl, Scope
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials

from .envs import *

# ASSERT SCOPE
ALL_SCOPES = list(Scope)
JWT_SCOPE = Scope.READ_PREDICTIONS
API_KEY_SCOPE = Scope.READ_TRADE_BOTS

# ERROR MESSAGES
API_KEY_EXPIRED = "API key expired"
API_KEY_INVALID = "Invalid API key"
BEARER_EXPIRED = "jwt expired"

# Debug
UPDATE_SCOPES = "you probably need to bring the scopes in both the api client and the auth service in sync"

# Each function is tested without credentials, with invalid credentials, and with valid credentials.
# The test is successful if the correct HTTPException is raised.


@pytest_asyncio.fixture
async def auth_handler() -> AuthHandler:
    return AuthHandler(BaseUrl.LOCAL)


# COMBINED AUTH


@pytest.mark.asyncio
async def test_combined_auth_without_credentials(auth_handler: AuthHandler):
    """Without credentials"""
    with pytest.raises(HTTPException) as e:
        await auth_handler.combined_auth(bearer=None, api_key=None)
    assert e.value.status_code == 401
    assert e.value.detail == auth_handler.no_credentials_exception.detail


# BEARER
@pytest.mark.asyncio
async def test_combined_auth_with_invalid_bearer_token(auth_handler: AuthHandler):
    """With invalid bearer token"""
    with pytest.raises(HTTPException) as e:
        await auth_handler.combined_auth(
            bearer=HTTPAuthorizationCredentials(scheme="Bearer", credentials="123"),
            api_key=None,
        )
    assert e.value.status_code == 401


@pytest.mark.asyncio
async def test_combined_auth_with_expired_bearer_token(auth_handler: AuthHandler):
    """With expired bearer token"""
    with pytest.raises(HTTPException) as e:
        await auth_handler.combined_auth(
            bearer=HTTPAuthorizationCredentials(
                scheme="Bearer", credentials=EXPIRED_JWT
            ),
            api_key=None,
        )
    assert e.value.status_code == 401
    assert e.value.detail == BEARER_EXPIRED


@pytest.mark.asyncio
async def test_combined_auth_with_valid_bearer_token(auth_handler: AuthHandler):
    """With valid bearer token"""
    res = await auth_handler.combined_auth(
        bearer=HTTPAuthorizationCredentials(scheme="Bearer", credentials=VALID_JWT),
        api_key=None,
    )
    assert JWT_SCOPE in res.scopes, UPDATE_SCOPES


# API KEY
@pytest.mark.asyncio
async def test_combined_auth_with_invalid_api_key(auth_handler: AuthHandler):
    """With invalid api key"""
    with pytest.raises(HTTPException) as e:
        return await auth_handler.combined_auth(bearer=None, api_key="123")
    assert e.value.status_code == 401


@pytest.mark.asyncio
async def test_combined_auth_with_full_scope_valid_api_key(auth_handler: AuthHandler):
    """With full scope valid api key"""
    res = await auth_handler.combined_auth(bearer=None, api_key=FULL_SCOPE_API_KEY)
    assert res.scopes == ALL_SCOPES, UPDATE_SCOPES


@pytest.mark.asyncio
async def test_combined_auth_with_one_scope_valid_api_key(auth_handler: AuthHandler):
    """With one scope valid api key"""
    res = await auth_handler.combined_auth(bearer=None, api_key=ONE_SCOPE_API_KEY)
    assert API_KEY_SCOPE in res.scopes, UPDATE_SCOPES


@pytest.mark.asyncio
async def test_combined_auth_with_expired_api_key(auth_handler: AuthHandler):
    """With expired api key"""
    with pytest.raises(HTTPException) as e:
        res = await auth_handler.combined_auth(bearer=None, api_key=EXPIRED_API_KEY)
    assert e.value.status_code == 401
    assert e.value.detail == API_KEY_EXPIRED


# API KEY AUTH
@pytest.mark.asyncio
async def test_api_key_auth_without_api_key(auth_handler: AuthHandler):
    """Without api key"""
    with pytest.raises(HTTPException) as e:
        return await auth_handler.api_key_auth(api_key=None)
    assert e.value.status_code == 401


@pytest.mark.asyncio
async def test_api_key_auth_with_invalid_api_key(auth_handler: AuthHandler):
    """With invalid api key"""
    with pytest.raises(HTTPException) as e:
        return await auth_handler.api_key_auth(api_key="123")
    assert e.value.status_code == 401


@pytest.mark.asyncio
async def test_api_key_auth_with_full_scope_valid_api_key(auth_handler: AuthHandler):
    """With full scope valid api key"""
    res = await auth_handler.api_key_auth(api_key=FULL_SCOPE_API_KEY)
    assert res.scopes == ALL_SCOPES, UPDATE_SCOPES


@pytest.mark.asyncio
async def test_api_key_auth_with_one_scope_valid_api_key(auth_handler: AuthHandler):
    """With one scope valid api key"""
    res = await auth_handler.api_key_auth(api_key=ONE_SCOPE_API_KEY)
    assert API_KEY_SCOPE in res.scopes, UPDATE_SCOPES


@pytest.mark.asyncio
async def test_api_key_auth_with_expired_api_key(auth_handler: AuthHandler):
    """With expired api key"""
    with pytest.raises(HTTPException) as e:
        res = await auth_handler.api_key_auth(api_key=EXPIRED_API_KEY)
    assert e.value.status_code == 401
    assert e.value.detail == API_KEY_EXPIRED


# BEARER AUTH
@pytest.mark.asyncio
async def test_bearer_auth_without_bearer(auth_handler: AuthHandler):
    """Without bearer"""
    with pytest.raises(HTTPException) as e:
        return await auth_handler.bearer_auth(bearer=None)
    assert e.value.status_code == 401


@pytest.mark.asyncio
async def test_bearer_auth_with_invalid_bearer(auth_handler: AuthHandler):
    """With invalid bearer"""
    with pytest.raises(HTTPException) as e:
        return await auth_handler.bearer_auth(
            bearer=HTTPAuthorizationCredentials(scheme="Bearer", credentials="123")
        )
    assert e.value.status_code == 401


@pytest.mark.asyncio
async def test_bearer_auth_with_valid_bearer(auth_handler: AuthHandler):
    """With valid bearer"""
    res = await auth_handler.bearer_auth(
        bearer=HTTPAuthorizationCredentials(scheme="Bearer", credentials=VALID_JWT)
    )
    assert JWT_SCOPE in res.scopes, UPDATE_SCOPES


@pytest.mark.asyncio
async def test_bearer_auth_with_expired_bearer(auth_handler: AuthHandler):
    """With expired bearer"""
    with pytest.raises(HTTPException) as e:
        return await auth_handler.bearer_auth(
            bearer=HTTPAuthorizationCredentials(
                scheme="Bearer", credentials=EXPIRED_JWT
            )
        )
    assert e.value.status_code == 401
    assert e.value.detail == BEARER_EXPIRED


# WS COMBINED AUTH
@pytest.mark.asyncio
async def test_ws_combined_auth_without_credentials(auth_handler: AuthHandler):
    """Without credentials"""
    with pytest.raises(HTTPException) as e:
        return await auth_handler.ws_combined_auth(bearer=None, api_key=None)
    assert e.value.status_code == 401
    assert e.value.detail == auth_handler.no_credentials_exception.detail


# BEARER
@pytest.mark.asyncio
async def test_ws_combined_auth_with_invalid_bearer(auth_handler: AuthHandler):
    """With invalid bearer"""
    with pytest.raises(HTTPException) as e:
        return await auth_handler.ws_combined_auth(bearer="123", api_key=None)
    assert e.value.status_code == 401


@pytest.mark.asyncio
async def test_ws_combined_auth_with_valid_bearer(auth_handler: AuthHandler):
    res = await auth_handler.ws_combined_auth(bearer=VALID_JWT, api_key=None)
    assert JWT_SCOPE in res.scopes, UPDATE_SCOPES


@pytest.mark.asyncio
async def test_ws_combined_auth_with_expired_bearer(auth_handler: AuthHandler):
    """With expired bearer"""
    with pytest.raises(HTTPException) as e:
        res = await auth_handler.ws_combined_auth(bearer=EXPIRED_JWT, api_key=None)
    assert e.value.status_code == 401
    assert e.value.detail == BEARER_EXPIRED


# API KEY
@pytest.mark.asyncio
async def test_ws_combined_auth_with_invalid_api_key(auth_handler: AuthHandler):
    """With invalid api key"""
    with pytest.raises(HTTPException) as e:
        res = await auth_handler.ws_combined_auth(bearer=None, api_key="123")
    assert e.value.status_code == 401


@pytest.mark.asyncio
async def test_ws_combined_auth_with_full_scope_valid_api_key(
    auth_handler: AuthHandler,
):
    """With full scope valid api key"""
    res = await auth_handler.ws_combined_auth(bearer=None, api_key=FULL_SCOPE_API_KEY)
    assert res.scopes == ALL_SCOPES, UPDATE_SCOPES


@pytest.mark.asyncio
async def test_ws_combined_auth_with_one_scope_valid_api_key(auth_handler: AuthHandler):
    """With one scope valid api key"""
    res = await auth_handler.ws_combined_auth(bearer=None, api_key=ONE_SCOPE_API_KEY)
    assert API_KEY_SCOPE in res.scopes, UPDATE_SCOPES


@pytest.mark.asyncio
async def test_ws_combined_auth_with_expired_api_key(auth_handler: AuthHandler):
    """With expired api key"""
    with pytest.raises(HTTPException) as e:
        res = await auth_handler.ws_combined_auth(bearer=None, api_key=EXPIRED_API_KEY)
    assert e.value.status_code == 401
    assert e.value.detail == API_KEY_EXPIRED


# WS BEARER AUTH
@pytest.mark.asyncio
async def test_ws_bearer_auth_without_bearer(auth_handler: AuthHandler):
    with pytest.raises(HTTPException) as e:
        return await auth_handler.ws_bearer_auth(bearer=None)
    assert e.value.status_code == 401


@pytest.mark.asyncio
async def test_ws_bearer_auth_with_invalid_bearer(auth_handler: AuthHandler):
    with pytest.raises(HTTPException) as e:
        return await auth_handler.ws_bearer_auth(bearer="123")
    assert e.value.status_code == 401


@pytest.mark.asyncio
async def test_ws_bearer_auth_with_valid_bearer(auth_handler: AuthHandler):
    res = await auth_handler.ws_bearer_auth(bearer=VALID_JWT)
    assert JWT_SCOPE in res.scopes, UPDATE_SCOPES


# WS API KEY AUTH
@pytest.mark.asyncio
async def test_ws_api_key_auth_without_api_key(auth_handler: AuthHandler):
    with pytest.raises(HTTPException) as e:
        return await auth_handler.ws_api_key_auth(api_key=None)
    assert e.value.status_code == 401


@pytest.mark.asyncio
async def test_ws_api_key_auth_with_invalid_api_key(auth_handler: AuthHandler):
    with pytest.raises(HTTPException) as e:
        return await auth_handler.ws_api_key_auth(api_key="123")
    assert e.value.status_code == 401


@pytest.mark.asyncio
async def test_ws_api_key_auth_with_expired_api_key(auth_handler: AuthHandler):
    with pytest.raises(HTTPException) as e:
        return await auth_handler.ws_api_key_auth(api_key=EXPIRED_API_KEY)
    assert e.value.status_code == 401
    assert e.value.detail == API_KEY_EXPIRED


@pytest.mark.asyncio
async def test_ws_api_key_auth_with_full_scope_valid_api_key(auth_handler: AuthHandler):
    res = await auth_handler.ws_api_key_auth(api_key=FULL_SCOPE_API_KEY)
    assert res.scopes == ALL_SCOPES, UPDATE_SCOPES


@pytest.mark.asyncio
async def test_ws_api_key_auth_with_one_scope_valid_api_key(auth_handler: AuthHandler):
    res = await auth_handler.ws_api_key_auth(api_key=ONE_SCOPE_API_KEY)
    assert API_KEY_SCOPE in res.scopes, UPDATE_SCOPES


# print(asyncio.run(test_ws_api_key_auth_with_one_scope_valid_api_key(AuthHandler(BaseUrl.LOCAL))))

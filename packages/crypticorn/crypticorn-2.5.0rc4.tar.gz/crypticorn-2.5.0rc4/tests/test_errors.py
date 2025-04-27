import pytest
from crypticorn.common import ApiError, ApiErrorIdentifier, HttpStatusMapper


@pytest.mark.asyncio
async def test_lengths():
    """Checks that the enums have the same length"""
    assert len(list(ApiError)) == len(
        list(ApiErrorIdentifier)
    ), f"ApiError ({len(list(ApiError))}) and ApiErrorIdentifier ({len(list(ApiErrorIdentifier))}) do not have the same number of elements"
    assert len(list(ApiError)) == len(
        list(HttpStatusMapper._mapping.keys())
    ), f"ApiError ({len(list(ApiError))}) and HttpStatusMapper ({len(list(HttpStatusMapper._mapping.keys()))}) do not have the same number of elements"


@pytest.mark.asyncio
async def test_enum_values():
    """Checks that the enums are string enums"""
    assert (
        ApiError.ALLOCATION_BELOW_MINIMUM.identifier
        == ApiErrorIdentifier.ALLOCATION_BELOW_MINIMUM
    ), "String enum values do not match"


@pytest.mark.asyncio
async def test_sorted():
    """Checks that the enums are sorted"""
    for error, identifier in zip(list(ApiError), list(ApiErrorIdentifier)):
        assert (
            error.identifier == identifier
        ), f"ApiError.{error.name} != ApiErrorIdentifier.{identifier.name}"


@pytest.mark.asyncio
async def test_fallback():
    """Checks that the fallback error is used when the error is not found due to a typo or not publishing the latest version of the client"""
    assert (
        ApiError.NOT_EXISTING_ERROR == ApiError.UNKNOWN_ERROR
    ), "Fallback error is not used"

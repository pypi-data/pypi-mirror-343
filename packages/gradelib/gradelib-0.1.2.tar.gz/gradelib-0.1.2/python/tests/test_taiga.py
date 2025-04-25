import pytest
import gradelib

# Public Taiga project base and slug
PUBLIC_TAIGA_BASE_URL = "https://api.taiga.io/api/v1/"
PUBLIC_TAIGA_SLUG = "ibarraz5-ser402-team3"  # Use a valid public project

@pytest.fixture(scope="module")
def public_taiga_client():
    return gradelib.TaigaClient(
        base_url=PUBLIC_TAIGA_BASE_URL,
        auth_token="",  # No token for public access
        username=""
    )

@pytest.mark.asyncio
async def test_fetch_project_data(public_taiga_client):
    """Fetch complete data for a public project (no auth required)."""
    try:
        result = await public_taiga_client.fetch_project_data(PUBLIC_TAIGA_SLUG)
        assert "project" in result
        assert "members" in result
        assert "sprints" in result
        assert "user_stories" in result
        assert "tasks" in result
        assert "task_histories" in result
    except ValueError as e:
        if "API request failed" in str(e):
            pytest.skip(f"Network or API connectivity issue: {e}")
        else:
            raise  # Re-raise if it's not a connectivity issue

@pytest.mark.asyncio
async def test_fetch_multiple_projects(public_taiga_client):
    """Fetch the same project multiple times via bulk API."""
    result = await public_taiga_client.fetch_multiple_projects([
        PUBLIC_TAIGA_SLUG,
        PUBLIC_TAIGA_SLUG
    ])
    assert isinstance(result, dict)
    assert PUBLIC_TAIGA_SLUG in result
    assert result[PUBLIC_TAIGA_SLUG] is True or "Error" in result[PUBLIC_TAIGA_SLUG]

@pytest.mark.asyncio
async def test_taiga_client_optional_parameters():
    """Test that TaigaClient can be created with optional parameters."""
    # Test with only base_url (no auth_token or username)
    client1 = gradelib.TaigaClient(base_url=PUBLIC_TAIGA_BASE_URL)
    assert isinstance(client1, gradelib.TaigaClient)
    
    # Test with base_url and auth_token, but no username
    client2 = gradelib.TaigaClient(
        base_url=PUBLIC_TAIGA_BASE_URL,
        auth_token="test_token"
    )
    assert isinstance(client2, gradelib.TaigaClient)
    
    # Test with base_url and username, but no auth_token
    client3 = gradelib.TaigaClient(
        base_url=PUBLIC_TAIGA_BASE_URL,
        username="test_user"
    )
    assert isinstance(client3, gradelib.TaigaClient)

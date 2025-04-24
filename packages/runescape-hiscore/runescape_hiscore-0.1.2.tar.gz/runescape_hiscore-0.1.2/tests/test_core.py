import pytest
from unittest.mock import patch
from osrs_hiscore.core import fetch_stats, SKILLS

# A dummy CSV line: rank=1, level=99, xp=13034431
MOCK_LINE = "1,99,13034431"
MOCK_CSV = "\n".join([MOCK_LINE] * len(SKILLS))


@patch("osrs_hiscore.core.requests.get")
def test_fetch_stats_regular(mock_get):
    # Simulate 404 for Ultimate, Hardcore, Ironman; then 200 for Regular
    class R404:
        status_code = 404

    class R200:
        status_code = 200
        text = MOCK_CSV

    mock_get.side_effect = [R404(), R404(), R404(), R200()]

    mode, stats = fetch_stats("anyuser")
    assert mode == "Regular"
    assert len(stats) == len(SKILLS)
    first = stats[0]
    assert first["skill"] == SKILLS[0]
    assert first["level"] == 99
    assert first["xp"] == 13034431


@patch("osrs_hiscore.core.requests.get")
def test_ironman_fallback_to_hardcore(mock_get):
    # Simulate 404 for Ultimate, then 200 for Hardcore Ironman
    class R404:
        status_code = 404

    class R200:
        status_code = 200
        text = MOCK_CSV

    mock_get.side_effect = [R404(), R200()]

    mode, stats = fetch_stats("user123")
    assert mode == "Hardcore Ironman"
    assert len(stats) == len(SKILLS)


@patch("osrs_hiscore.core.requests.get")
def test_user_not_found_raises(mock_get):
    # All endpoints return 404 → should raise HTTPError
    class R404:
        status_code = 404

    mock_get.return_value = R404()

    with pytest.raises(Exception):
        fetch_stats("ghost_user")

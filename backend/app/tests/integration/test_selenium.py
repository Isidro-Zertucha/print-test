import pytest
from app.scrapping.scrape_hn import fetch_realtime_headlines

@pytest.mark.integration
@pytest.mark.skipif(not pytest.config.getoption("--run-integration"),
                    reason="Needs Selenium container")
def test_real_hn_scraping():
    results = fetch_realtime_headlines()
    assert isinstance(results, list)
    if results:  # Might be empty if HN is down
        assert "title" in results[0]
        assert "url" in results[0]
        assert isinstance(results[0]["score"], int)
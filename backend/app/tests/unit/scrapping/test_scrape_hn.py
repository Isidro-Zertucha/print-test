from selenium.webdriver.remote.webelement import WebElement
from app.scrapping.scrape_hn import fetch_realtime_headlines

def test_fetch_realtime_headlines(mock_selenium):
    # Mock story elements
    mock_story = MagicMock(spec=WebElement)
    mock_story.find_element.return_value.text = "Test Story"
    mock_story.find_element.return_value.get_attribute.return_value = "http://test.com"
    
    # Mock score element
    mock_score = MagicMock(spec=WebElement)
    mock_score.text = "123 points"
    
    # Configure mock returns
    mock_selenium.find_elements.return_value = [mock_story]
    mock_story.find_element.return_value = mock_score
    
    results = fetch_realtime_headlines()
    assert len(results) == 1
    assert results[0]["title"] == "Test Story"
    assert results[0]["score"] == 123
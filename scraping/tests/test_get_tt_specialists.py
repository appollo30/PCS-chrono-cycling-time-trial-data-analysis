import pytest
from src.get_tt_specialists import process_rider_sync

@pytest.mark.parametrize(
    "full_name, url",
    [
        ("BISSEGGER Stefan", "https://www.procyclingstats.com/rider/stefan-bissegger"),
        ("GANNA Filippo", "https://www.procyclingstats.com/rider/filippo-ganna"),
        ("BILBAO Pello", "https://www.procyclingstats.com/rider/pello-bilbao")
    ]
)
def test_process_rider_sync_expected_keys(full_name, url):
    expected_keys = {
        "first_name",
        "last_name",
        "full_name",
        "nationality",
        "birth_year",
        "height",
        "weight",
        "onedayraces",
        "gc",
        "tt",
        "sprint",
        "climber",
        "hills",
        "photo_url",
        "url"
    }
     
    result = process_rider_sync(full_name, url, verbose=False)
    
    assert set(result.keys()) == expected_keys
    assert isinstance(result["url"], str)
    assert isinstance(result["first_name"], str)
    assert isinstance(result["last_name"], str)
    assert result["full_name"] == result["first_name"] + " " + result["last_name"]
    assert isinstance(result["full_name"], str)
    assert isinstance(result["nationality"], str)
    assert isinstance(result["birth_year"], int)
    assert isinstance(result["height"], float)
    assert isinstance(result["weight"], float)
    assert isinstance(result["onedayraces"], int)
    assert isinstance(result["gc"], int)
    assert isinstance(result["tt"], int)
    assert isinstance(result["sprint"], int)
    assert isinstance(result["climber"], int)
    assert isinstance(result["hills"], int)
    assert isinstance(result["photo_url"], str)

@pytest.mark.parametrize(
    "full_name, url, expected",
    [
        (
            "BISSEGGER Stefan",
            "https://www.procyclingstats.com/rider/stefan-bissegger",
            {
                "first_name": "Stefan",
                "last_name": "Bissegger",
                "nationality": "Switzerland",
                "birth_year": 1998
            }
        ),
        (
            "GANNA Filippo",
            "https://www.procyclingstats.com/rider/filippo-ganna",
            {
                "first_name": "Filippo",
                "last_name": "Ganna",
                "nationality": "Italy",
                "birth_year": 1996
            }
        ),
        (
            "BILBAO Pello",
            "https://www.procyclingstats.com/rider/pello-bilbao",
            {
                "first_name": "Pello",
                "last_name": "Bilbao",
                "nationality": "Spain",
                "birth_year": 1990
            }
        )
    ]
)  
def test_process_rider_sync_values(full_name, url, expected):
    # Since some stats can change, we only check for a subset of keys
    assertable_keys = {
        "first_name",
        "last_name", # Could change (see Guigui Martin)
        "nationality", # Could change (see Froome or Sivakov)
        "birth_year"
        # Height and weight can change
    }
    
    result = process_rider_sync(full_name, url, verbose=False)
    
    for key in assertable_keys:
        assert result[key] == expected[key]

import pytest
from src.get_tt_races import process_race_sync

@pytest.mark.parametrize(
    "url",
    [
        ("https://www.procyclingstats.com/race/tour-de-france/2024/stage-21"),
        ("https://www.procyclingstats.com/race/uci-world-championships-itt-mj/2022/result"),
        ("https://www.procyclingstats.com/race/nc-belgium-itt/2025/result"),
        ("https://www.procyclingstats.com/race/tour-de-luxembourg/2023/stage-4"),
        ("https://www.procyclingstats.com/race/volta-ao-algarve/2023/stage-5")
    ]
)
def test_process_race_sync_expected_keys(url : str):
    expected_keys = {
        "race_title",
        "date",
        "departure",
        "arrival",
        "class",
        "distance",
        "vertical_meters",
        "startlist_quality",
        "profile_score",
        "temperature",
        "race_ranking",
        "winner_time",
        "winner_speed",
        "profile_image_url",
        "url"
    }
    
    result = process_race_sync(url, verbose=False)
    
    assert set(result.keys()) == expected_keys
    
    assert isinstance(result["race_title"], str)
    assert isinstance(result["date"], str)
    assert isinstance(result["departure"], str)
    assert isinstance(result["arrival"], str)
    assert isinstance(result["class"], str)
    assert isinstance(result["distance"], float)
    assert isinstance(result["vertical_meters"], (int, type(None)))
    assert isinstance(result["startlist_quality"], (int, type(None)))
    assert isinstance(result["profile_score"], (int, type(None)))
    assert isinstance(result["temperature"], (int, type(None)))
    assert isinstance(result["race_ranking"], (int, type(None)))
    assert isinstance(result["winner_time"], (int,float))
    assert isinstance(result["winner_speed"], float)
    assert isinstance(result["profile_image_url"], (str, type(None)))
    assert isinstance(result["url"], str)
    

def test_process_race_sync_values()
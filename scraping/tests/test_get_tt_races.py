from typing import Dict
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
    
@pytest.mark.parametrize(
    "url, expected",
    [
        (
            "https://www.procyclingstats.com/race/tour-de-france/2024/stage-21",
            {
                "race_title": "Tour de France 2024 Stage 21 (ITT)",
                "date": "21 July 2024",
                "departure": "Monaco",
                "arrival": "Nice",
                "class": "2.UWT",
                "distance": 33.7,
                "vertical_meters": 720,
                "startlist_quality": None,
                "profile_score": 73,
                "temperature": 28,
                "race_ranking": 1,
                "winner_time": 2724,
                "winner_speed": 44.537,
                "profile_image_url": "https://www.procyclingstats.com/images/profiles/ca/fb/tour-de-france-2024-stage-21-profile.jpg",
                "url": "https://www.procyclingstats.com/race/tour-de-france/2024/stage-21"
            }
        ),
        (
            "https://www.procyclingstats.com/race/uci-world-championships-itt-mj/2022/result",
            {
                "race_title": "World Championships MJ - ITT 2022 Time Trial",
                "date": "20 September 2022",
                "departure": "Wollongong",
                "arrival": "Wollongong",
                "class": "WC",
                "distance": 28.8,
                "vertical_meters": 306,
                "startlist_quality": 0,
                "profile_score": 18,
                "temperature": None,
                "race_ranking": None,
                "winner_time": 478499,
                "winner_speed": 0.217,
                "profile_image_url": "https://www.procyclingstats.com/images/profiles/ca/ac/uci-world-championships-itt-mj-2022-result-profile.jpg",
                "url": "https://www.procyclingstats.com/race/uci-world-championships-itt-mj/2022/result"
            }
        ),
        (
            "https://www.procyclingstats.com/race/nc-belgium-itt/2025/result",
            {
                "race_title": "National Championships Belgium ME - ITT 2025 Time Trial",
                "date": "27 June 2025",
                "departure": "Brasschaat",
                "arrival": "Brasschaat",
                "class": "NC",
                "distance": 40.5,
                "vertical_meters": 198,
                "startlist_quality": 83,
                "profile_score": 2,
                "temperature": None,
                "race_ranking": 168,
                "winner_time": 419083,
                "winner_speed": 0.348,
                "profile_image_url": "https://www.procyclingstats.com/images/profiles/ca/be/nc-belgium-itt-2025-result-profile.jpg",
                "url": "https://www.procyclingstats.com/race/nc-belgium-itt/2025/result"
            }
        ),
        (
            "https://www.procyclingstats.com/race/tour-de-luxembourg/2023/stage-4",
            {
                "race_title": "\u0160koda Tour Luxembourg 2023 Stage 4 (ITT)",
                "date": "23 September 2023",
                "departure": "P\u00e9tange",
                "arrival": "P\u00e9tange",
                "class": "2.Pro",
                "distance": 23.9,
                "vertical_meters": 237,
                "startlist_quality": None,
                "profile_score": 14,
                "temperature": 15,
                "race_ranking": 35,
                "winner_time": 1686,
                "winner_speed": 51.032,
                "profile_image_url": "https://www.procyclingstats.com/images/profiles/ca/ba/tour-de-luxembourg-2023-stage-4-profile.jpg",
                "url": "https://www.procyclingstats.com/race/tour-de-luxembourg/2023/stage-4"
            }
        ),
        (
            "https://www.procyclingstats.com/race/volta-ao-algarve/2023/stage-5",
            {
                "race_title": "Volta ao Algarve em Bicicleta 2023 Stage 5 (ITT)",
                "date": "19 February 2023",
                "departure": "Lagoa",
                "arrival": "Lagoa",
                "class": "2.Pro",
                "distance": 24.4,
                "vertical_meters": 308,
                "startlist_quality": None,
                "profile_score": 18,
                "temperature": None,
                "race_ranking": 33,
                "winner_time": 1774,
                "winner_speed": 49.515,
                "profile_image_url": "https://www.procyclingstats.com/images/profiles/ca/cb/volta-ao-algarve-2023-stage-5-profile.jpg",
                "url": "https://www.procyclingstats.com/race/volta-ao-algarve/2023/stage-5"
            }
        ),
    ]
)
def test_process_race_sync_values(url : str, expected : Dict):
    result = process_race_sync(url, verbose=False)
    for key, value in expected.items():
        assert result[key] == value
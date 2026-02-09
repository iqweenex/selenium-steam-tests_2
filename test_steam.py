import pytest
import time
from pages.main_page import MainPage
from pages.search_page import SearchPage
from config_reader import config

test_data = config.get("test_data.games", [])
test_cases = []
for game in test_data:
    for language in ['en', 'ru']:
        test_cases.append((language, game["game_name"], game["min_count"]))


# ("Fallout", 20),
#    ("Skyrim", 7),
#    ("GTA", 12),
#    ("Dark Souls", 20)
@pytest.mark.parametrize("language, game_name, min_count", test_cases)
def test_steam_search_and_sort_by_price_desc(wait, language, game_name, min_count):
    main_page = MainPage(wait)
    main_page.open_steam_main_page(language=language)
    search_page = main_page.search_game(game_name)
    assert search_page.select_sort_price_desc(), f"Не удалось отсортировать для игры '{game_name}'"
    assert search_page.is_sorted_by_price_desc(), f"Сортировка не применилась для '{game_name}'"

    games = search_page.get_first_n_games(min_count)

    games_with_price = [g for g in games if g['game_price'] is not None]

    if len(games_with_price) >= 2:
        prices = [game['game_price'] for game in games_with_price]
        assert prices == sorted(prices, reverse=True)

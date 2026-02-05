import pytest
import time
from pages.main_page import MainPage
from pages.search_page import SearchPage


@pytest.mark.parametrize("game_name, count_games", [
    ("The Witcher", 10),
    ("Fallout", 20),
    ("Skyrim", 7),
    ("GTA", 12),
    ("Dark Souls", 20)])
def test_steam_search_and_sort_by_price_desc(driver, wait, game_name, count_games):
    driver.get("https://store.steampowered.com")
    main_page = MainPage(driver, wait)
    search_page = main_page.search_game(game_name)
    assert search_page.select_sort_price_desc(), f"Не удалось отсортировать для игры '{game_name}'"
    assert search_page.is_sorted_by_price_desc(), f"Сортировка не применилась для '{game_name}'"

    games = search_page.get_first_n_games(count_games)

    assert len(games) == count_games, f"Для '{game_name}' найдено {len(games)} игр" \
                                      f"А ожидалось {count_games} игр"
    games_with_price = [g for g in games if g['game_price'] is not None]

    if len(games_with_price) >= 2:
        for i in range(len(games_with_price) - 1):
            current_price = games_with_price[i]['game_price']
            next_price = games_with_price[i + 1]['game_price']
            assert current_price >= next_price, f"Для {game_name} сортировка неверная" \
                                                f"{current_price} < {next_price}"




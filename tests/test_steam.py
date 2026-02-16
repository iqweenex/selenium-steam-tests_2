import pytest
from pages.main_page import MainPage
from pages.search_page import SearchPage
from utils.test_data_reader import TestDataReader
from enums.language import Language


@pytest.fixture(params=[Language.ENGLISH, Language.RUSSIAN], ids=lambda lang: lang.value)
def language(request):
    return request.param


@pytest.fixture(params=TestDataReader.get_games(), ids=lambda game: game["game_name"])
def game(request):
    return request.param


def test_steam_search_and_sort_by_price_desc(wait, language, game):
    game_name = game['game_name']
    min_count = game['min_count']

    main_page = MainPage(wait)
    main_page.change_language(language)

    main_page.search_game(game_name)
    search_page = SearchPage(wait)

    search_page.select_sort_price_desc()

    games = search_page.get_first_n_games(min_count)

    prices = [game['game_price'] for game in games]
    assert prices == sorted(prices, reverse=True), "Сортировка работает неккоректно:\n" \
                                                   f"Ожидалось:{sorted(prices, reverse=True)}\n" \
                                                   f"Фактические результат: {prices}"

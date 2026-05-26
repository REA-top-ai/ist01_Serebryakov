import logging
import requests

logger = logging.getLogger(__name__)

_BASE = 'https://deckofcardsapi.com/api/deck'
_STATIC_BASE = 'https://deckofcardsapi.com/static/img'

_image_cache: dict[str, str] = {}


def _to_api_code(card_id: str) -> str:
    rank = '0' if card_id[0].upper() == 'T' else card_id[0].upper()
    return rank + card_id[1].upper()


def _fallback_images() -> None:
    for rank in ('A', 'K', 'Q', 'J', '0', '9', '8', '7', '6', '5', '4', '3', '2'):
        for suit in ('S', 'H', 'D', 'C'):
            code = rank + suit
            _image_cache[code] = f'{_STATIC_BASE}/{code}.png'


def _load_images() -> None:
    try:
        r = requests.get(f'{_BASE}/new/', timeout=5)
        r.raise_for_status()
        deck_id = r.json()['deck_id']

        r = requests.get(f'{_BASE}/{deck_id}/draw/?count=52', timeout=10)
        r.raise_for_status()
        for card in r.json().get('cards', []):
            _image_cache[card['code']] = card['image']

        logger.info('Loaded %d card images from deckofcardsapi.com', len(_image_cache))
    except Exception as exc:
        logger.warning('deckofcardsapi.com unavailable (%s) — using static fallback URLs', exc)
        _fallback_images()


def _ensure_loaded() -> None:
    if not _image_cache:
        _load_images()


def get_new_deck(shuffled: bool = True) -> dict:
    url = f'{_BASE}/new/{"shuffle/" if shuffled else ""}'
    r = requests.get(url, timeout=5)
    r.raise_for_status()
    return r.json()


def draw_cards(deck_id: str, count: int = 1) -> list[dict]:
    r = requests.get(f'{_BASE}/{deck_id}/draw/?count={count}', timeout=10)
    r.raise_for_status()
    return r.json().get('cards', [])


def return_cards(deck_id: str, codes: list[str]) -> dict:
    r = requests.get(f'{_BASE}/{deck_id}/return/?cards={",".join(codes)}', timeout=5)
    r.raise_for_status()
    return r.json()


def shuffle_deck(deck_id: str) -> dict:
    r = requests.get(f'{_BASE}/{deck_id}/shuffle/', timeout=5)
    r.raise_for_status()
    return r.json()


def image_url(card_id: str) -> str:
    _ensure_loaded()
    code = _to_api_code(card_id)
    return _image_cache.get(code, f'{_STATIC_BASE}/{code}.png')


def all_images() -> dict[str, str]:
    _ensure_loaded()
    return _image_cache

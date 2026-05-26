import json
import logging
import requests

import config

logger = logging.getLogger(__name__)

_URL   = 'https://integrate.api.nvidia.com/v1/chat/completions'
_MODEL = 'moonshotai/kimi-k2.6'
  
def get_ai_recommendation(analysis: dict) -> dict:
    if not config.NVIDIA_API_KEY:
        return _fallback(analysis, 'set NVIDIA_API_KEY for AI coaching')

    try:
        resp = requests.post(
            _URL,
            headers={'Authorization': f'Bearer {config.NVIDIA_API_KEY}', 'Accept': 'application/json'},
            json={
                'model':    _MODEL,
                'messages': [{'role': 'user', 'content': _build_prompt(analysis)}],
                'max_tokens':  512,
                'temperature': 0.4,
                'stream':      False,
            },
            timeout=240,
        )

        logger.warning('Kimi status: %s', resp.status_code)
        logger.warning('Kimi headers: %s', dict(resp.headers))
        logger.warning('Kimi body (first 500): %r', resp.text[:500])
        logger.warning('Kimi body length: %s', len(resp.text))

        resp.raise_for_status()

        try:
            raw = resp.json()
        except json.JSONDecodeError as e:
            logger.warning('Kimi response is not JSON. body=%r', resp.text[:1000])
            return _fallback(analysis, f'AI returned non-JSON body')

        choice = raw['choices'][0]
        content = choice.get('message', {}).get('content')
        finish_reason = choice.get('finish_reason')

        if not content:
            logger.warning('Kimi empty content. finish=%s, raw=%s', finish_reason, raw)
            return _fallback(analysis, 'AI returned empty response')

        content = content.strip()

        if content.startswith('```'):
            content = '\n'.join(
                l for l in content.splitlines() if not l.startswith('```')
            ).strip()

        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            logger.warning('Kimi non-JSON content: %r', content[:300])
            return _fallback(analysis, 'AI returned non-JSON content')

        data['action'] = str(data.get('action', 'CALL')).upper()
        data['ai_powered'] = True
        data.setdefault('confidence', 50)
        data.setdefault('bluff_rating', 0)
        data.setdefault('aggression_rating', 5)
        data.setdefault('key_insight', '')
        return data

    except Exception as e:
        logger.warning('Kimi error (%s): %s', type(e).__name__, e)
        return _fallback(analysis, 'AI temporarily unavailable')


def _build_prompt(a: dict) -> str:
    parts = [
        "=== Texas Hold'em Strategic Analysis ===",
        f'Street:  {a["street"].upper()}',
        f'Hole:    {a["hole_cards"]}',
        f'Board:   {a["board"] or "none (pre-flop)"}',
        f'Hand:    {a["hand_name"]}   Players: {a["players"]}',
        f'Win: {a["win"]}%  Tie: {a["tie"]}%  Lose: {a["lose"]}%',
    ]
    if a.get('outs') is not None: 
        parts.append(f'Outs:    {a["outs"]}')
    if a.get('pot'):              
        parts.append(f'Pot:     ${a["pot"]:.2f}')
    if a.get('bet'):              
        parts.append(f'Bet:     ${a["bet"]:.2f}')
    if a.get('pot_odds'):         
        parts.append(f'Req.eq:  {a["pot_odds"]}%')
    parts += [
        '',
        'Return ONLY valid JSON (no markdown):',
        '{"action":"<FOLD|CALL|CHECK|RAISE|ALL_IN>","confidence":<0-100>,'
        '"reasoning":"<2-3 sentences>","bluff_rating":<0-10>,'
        '"aggression_rating":<0-10>,"key_insight":"<one tactical tip>"}',
    ]
    return '\n'.join(parts)


def _fallback(a: dict, note: str = '') -> dict:
    action = a.get('action', 'call').upper()
    return {
        'action':action,
        'confidence': int(a.get('win', 0)),
        'reasoning': a.get('reason', '') + (f' ({note})' if note else ''),
        'bluff_rating':0,
        'aggression_rating': 7 if action == 'RAISE' else 1 if action == 'FOLD' else 3,
        'key_insight':'AI coach offline — rule-based recommendation.',
        'ai_powered': False,
    }

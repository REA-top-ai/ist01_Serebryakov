from collections import Counter
from itertools import combinations
import random
from typing import Dict, List, Optional, Tuple

RANKS = '23456789TJQKA'
SUITS = 'shdc'

_RANK = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
    '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14,
}
_RANK_STR = {v: k for k, v in _RANK.items()}

HAND_NAMES = {
    8: 'Straight Flush', 7: 'Four of a Kind', 6: 'Full House',
    5: 'Flush',          4: 'Straight',        3: 'Three of a Kind',
    2: 'Two Pair',       1: 'One Pair',         0: 'High Card',
}

Card = Tuple[int, str]


def parse(card: str) -> Card:
    if len(card) != 2:
        raise ValueError(f"Invalid card '{card}' — use rank+suit, e.g. As Td")
    r, s = card[0].upper(), card[1].lower()
    if r not in _RANK:
        raise ValueError(f"Unknown rank '{r}' in '{card}'")
    if s not in SUITS:
        raise ValueError(f"Unknown suit '{s}' in '{card}'")
    return (_RANK[r], s)


def full_deck() -> List[Card]:
    return [(_RANK[r], s) for r in RANKS for s in SUITS]


def _score5(hand: List[Card]) -> Tuple:
    ranks = [c[0] for c in hand]
    suits = [c[1] for c in hand]
    is_flush = len(set(suits)) == 1

    cnt = Counter(ranks)
    by_cnt = sorted(cnt.items(), key=lambda x: (x[1], x[0]), reverse=True)
    groups = tuple(n for _, n in by_cnt)
    g_ranks = [r for r, _ in by_cnt]

    uniq = sorted(set(ranks), reverse=True)
    straight_hi: Optional[int] = None
    if len(uniq) == 5:
        if uniq[0] - uniq[4] == 4:
            straight_hi = uniq[0]
        elif set(uniq) == {14, 2, 3, 4, 5}:
            straight_hi = 5
    is_str = straight_hi is not None

    if is_str and is_flush:    return (8, straight_hi)
    if groups == (4, 1):       return (7,) + tuple(g_ranks)
    if groups == (3, 2):       return (6,) + tuple(g_ranks)
    if is_flush:               return (5,) + tuple(sorted(ranks, reverse=True))
    if is_str:                 return (4, straight_hi)
    if groups == (3, 1, 1):    return (3,) + tuple(g_ranks)
    if groups == (2, 2, 1):    return (2,) + tuple(g_ranks)
    if groups == (2, 1, 1, 1): return (1,) + tuple(g_ranks)
    return (0,) + tuple(sorted(ranks, reverse=True))


def best_hand(cards: List[Card]) -> Tuple:
    if len(cards) < 5:
        return (0,) + tuple(sorted((c[0] for c in cards), reverse=True))
    top = None
    for combo in combinations(cards, 5):
        s = _score5(list(combo))
        if top is None or s > top:
            top = s
    return top  # type: ignore


def hand_name(score: Tuple) -> str:
    return HAND_NAMES.get(score[0], 'High Card')


def _preflop_name(hole: List[Card]) -> str:
    if len(hole) != 2:
        return 'Unknown'
    (r1, s1), (r2, s2) = hole
    if r1 == r2:
        return f'Pocket {_RANK_STR[r1]}s'
    hi, lo = (r1, r2) if r1 > r2 else (r2, r1)
    return f'{_RANK_STR[hi]}{_RANK_STR[lo]}{"s" if s1 == s2 else "o"}'


def equity(hole: List[Card], board: List[Card], players: int = 2, sims: int = 2000) -> Dict:
    used = set(hole + board)
    remaining = [c for c in full_deck() if c not in used]
    need = 5 - len(board)
    draw_size = need + (players - 1) * 2
    wins = ties = losses = 0

    for _ in range(sims):
        draw = random.sample(remaining, min(draw_size, len(remaining)))
        run_board = board + draw[:need]
        left = draw[need:]

        my = best_hand(hole + run_board)
        opp_best = None
        for i in range(players - 1):
            opp = left[i * 2: i * 2 + 2]
            if len(opp) < 2:
                break
            s = best_hand(opp + run_board)
            if opp_best is None or s > opp_best:
                opp_best = s

        if opp_best is None or my > opp_best:
            wins += 1
        elif my == opp_best:
            ties += 1
        else:
            losses += 1

    total = wins + ties + losses or 1
    current = hole + board
    if len(current) >= 5:
        name = hand_name(best_hand(current))
    elif len(current) == 2:
        name = _preflop_name(hole)
    else:
        name = hand_name(best_hand(current))

    return {
        'win':       round(wins   / total * 100, 1),
        'tie':       round(ties   / total * 100, 1),
        'lose':      round(losses / total * 100, 1),
        'hand_name': name,
    }


def count_outs(hole: List[Card], board: List[Card]) -> int:
    if len(board) < 3:
        return 0
    used = set(hole + board)
    remaining = [c for c in full_deck() if c not in used]
    cur = best_hand(hole + board)
    return sum(1 for c in remaining if best_hand(hole + board + [c]) > cur)


def calc_pot_odds(pot: float, bet: float) -> Optional[float]:
    if bet <= 0:
        return None
    total = pot + bet
    return round(bet / total * 100, 1) if total > 0 else None


def street_name(board: List[Card]) -> str:
    return {0: 'preflop', 3: 'flop', 4: 'turn', 5: 'river'}.get(len(board), 'unknown')


def basic_action(win: float, n_outs: int, req: Optional[float], st: str) -> Dict:
    if win >= 70:
        return {'action': 'raise', 'reason': f'Strong equity ({win}%). Raise for value.'}
    if win >= 55:
        return {'action': 'raise', 'reason': f'Above-average equity ({win}%). Thin value raise.'}
    if win >= 40:
        if req and win < req:
            return {'action': 'fold', 'reason': f'Pot odds require {req}% equity; you have {win}%.'}
        return {'action': 'call',  'reason': f'Decent equity ({win}%). Calling is correct.'}
    if st in ('flop', 'turn') and n_outs >= 8:
        return {'action': 'call',  'reason': f'{n_outs} outs — strong draw. Call if price is right.'}
    if req and win >= req:
        return {'action': 'call',  'reason': f'Pot odds ({req}%) justify calling with {win}%.'}
    return {'action': 'fold',      'reason': f'Weak equity ({win}%). Folding is correct.'}


def analyze(hole_str: str, board_str: str = '',
            players: int = 2, pot: float = 0, bet: float = 0,
            sims: int = 2000) -> Dict:
    h_tokens = hole_str.strip().split()
    b_tokens = board_str.strip().split() if board_str else []

    if len(h_tokens) != 2:
        raise ValueError('Provide exactly 2 hole cards e.g. "As Kh"')
    if len(b_tokens) not in (0, 3, 4, 5):
        raise ValueError('Board must be 0 (pre-flop), 3 (flop), 4 (turn), or 5 (river) cards')

    hole  = [parse(c) for c in h_tokens]
    board = [parse(c) for c in b_tokens]

    all_cards = hole + board
    if len(set(all_cards)) != len(all_cards):
        raise ValueError('Duplicate cards detected')

    players = max(2, min(9, int(players)))
    eq= equity(hole, board, players, sims)
    n_out= count_outs(hole, board) if len(board) >= 3 else None
    req= calc_pot_odds(pot, bet)
    st  = street_name(board)
    act= basic_action(eq['win'], n_out or 0, req, st)

    return {
        'hole_cards': hole_str.strip().upper(),
        'board':      board_str.strip().upper() if board_str else '',
        'street':     st,
        'hand_name':  eq['hand_name'],
        'win':        eq['win'],
        'tie':        eq['tie'],
        'lose':       eq['lose'],
        'outs':       n_out,
        'pot_odds':   req,
        'players':    players,
        'pot':        pot,
        'bet':        bet,
        'action':     act['action'],
        'reason':     act['reason'],
    }

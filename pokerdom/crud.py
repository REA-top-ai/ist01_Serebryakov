from datetime import datetime
from typing import Optional
from sqlalchemy import func, desc
from sqlalchemy.orm import Session
from models import Hand


def create_hand(session: Session, result: dict, ai: dict) -> int:
    hand = Hand(
        created_at = datetime.utcnow(),
        hole_cards = result['hole_cards'],
        board = result['board'] or None,
        street= result['street'],
        players = result['players'],
        pot = result['pot'],
        bet = result['bet'],
        hand_name = result['hand_name'],
        win = result['win'],
        tie = result['tie'],
        lose = result['lose'],
        outs = result['outs'],
        pot_odds = result['pot_odds'],
        ai_action = ai.get('action', '').lower(),
        ai_reasoning = ai.get('reasoning', ''),
        ai_confidence= ai.get('confidence'),
        ai_bluff = ai.get('bluff_rating'),
        ai_aggression = ai.get('aggression_rating'),
        ai_insight = ai.get('key_insight', ''),
        ai_powered= bool(ai.get('ai_powered')),
    )
    session.add(hand)
    session.commit()
    session.refresh(hand)
    return hand.id


def get_all_hands(session: Session):
    return session.query(Hand).order_by(desc(Hand.id)).all()


def get_recent_hands(session: Session, limit: int = 8):
    return session.query(Hand).order_by(desc(Hand.id)).limit(limit).all()


def count_hands(session: Session):
    return session.query(func.count(Hand.id)).scalar()


def get_hand(session: Session, hand_id: int) -> Optional[Hand]:
    return session.query(Hand).filter(Hand.id == hand_id).first()

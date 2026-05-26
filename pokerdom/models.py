from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Float, Integer, Text
from database import Base


class Hand(Base):
    __tablename__ = "hands"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    hole_cards = Column(Text, nullable=False)
    board = Column(Text)
    street = Column(Text)
    players = Column(Integer, default=2)
    pot = Column(Float, default=0)
    bet = Column(Float, default=0)
    hand_name = Column(Text)
    win = Column(Float)
    tie = Column(Float)
    lose = Column(Float)
    outs = Column(Integer)
    pot_odds = Column(Float)
    ai_action = Column(Text)
    ai_reasoning = Column(Text)
    ai_confidence = Column(Integer)
    ai_bluff = Column(Integer)
    ai_aggression = Column(Integer)
    ai_insight = Column(Text)
    ai_powered = Column(Boolean, default=False)

    def __repr__(self) -> str:
        return f'<Hand id={self.id} hole={self.hole_cards} street={self.street} action={self.ai_action}>'

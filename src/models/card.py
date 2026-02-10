"""
Module pour gérer les cartes à jouer de la Bélote
"""
from enum import Enum
from dataclasses import dataclass


class Suit(Enum):
    """Les 4 couleurs (enseignes) du jeu de cartes"""
    HEARTS = "♥"
    DIAMONDS = "♦"
    CLUBS = "♣"
    SPADES = "♠"


class Rank(Enum):
    """Les valeurs des cartes"""
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    TEN = "10"
    JACK = "V"
    QUEEN = "D"
    KING = "K"
    ACE = "A"


@dataclass
class Card:
    """Représente une carte à jouer"""
    rank: Rank
    suit: Suit

    def __str__(self) -> str:
        return f"{self.rank.value}{self.suit.value}"

    def __repr__(self) -> str:
        return f"Card({self.rank.name}, {self.suit.name})"

    def get_points_at_suit(self, trump_suit: Suit) -> int:
        """
        Retourne les points de la carte selon si elle est un atout ou non
        
        Args:
            trump_suit: La couleur d'atout
            
        Returns:
            Le nombre de points de la carte
        """
        is_trump = self.suit == trump_suit
        
        if is_trump:
            points_map = {
                Rank.SEVEN: 0,
                Rank.EIGHT: 0,
                Rank.NINE: 14,
                Rank.TEN: 10,
                Rank.JACK: 20,
                Rank.QUEEN: 3,
                Rank.KING: 4,
                Rank.ACE: 11,
            }
        else:
            points_map = {
                Rank.SEVEN: 0,
                Rank.EIGHT: 0,
                Rank.NINE: 0,
                Rank.TEN: 10,
                Rank.JACK: 2,
                Rank.QUEEN: 3,
                Rank.KING: 4,
                Rank.ACE: 11,
            }
        
        return points_map.get(self.rank, 0)

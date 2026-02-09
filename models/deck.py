"""
Module pour gérer le jeu de cartes (paquet)
"""
import random
from typing import List
from .card import Card, Suit, Rank


class Deck:
    """Représente un paquet de cartes"""
    
    def __init__(self, shuffled: bool = True):
        """
        Initialise le paquet
        
        Args:
            shuffled: Si True, les cartes sont mélangées
        """
        self.cards: List[Card] = []
        self._initialize_deck()
        if shuffled:
            self.shuffle()

    def _initialize_deck(self):
        """Crée les 32 cartes du paquet standard"""
        for suit in Suit:
            for rank in Rank:
                self.cards.append(Card(rank, suit))

    def shuffle(self):
        """Mélange le paquet"""
        random.shuffle(self.cards)

    def draw(self) -> Card:
        """
        Tire une carte du paquet
        
        Returns:
            La carte tirée
            
        Raises:
            IndexError: Si le paquet est vide
        """
        if not self.cards:
            raise IndexError("Le paquet est vide")
        return self.cards.pop()

    def deal(self, num_cards: int) -> List[Card]:
        """
        Distribue plusieurs cartes
        
        Args:
            num_cards: Le nombre de cartes à distribuer
            
        Returns:
            Liste des cartes distribuées
        """
        dealt = []
        for _ in range(num_cards):
            dealt.append(self.draw())
        return dealt

    def __len__(self) -> int:
        """Retourne le nombre de cartes restantes"""
        return len(self.cards)

    def is_empty(self) -> bool:
        """Vérifie si le paquet est vide"""
        return len(self.cards) == 0

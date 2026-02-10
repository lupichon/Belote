"""
Module pour gérer les équipes
"""
from dataclasses import dataclass
from models.player import Player


@dataclass
class Team:
    """Représente une équipe de joueurs"""
    _name: str
    _player1 : Player
    _player2 : Player
    _score: int = 0

    @property
    def name(self) -> str:
        """Retourne le nom de l'équipe"""
        return self._name
    
    @property
    def player1(self) -> Player:
        """Retourne le premier joueur de l'équipe"""
        return self._player1
    
    @property
    def player2(self) -> Player:
        """Retourne le second joueur de l'équipe"""
        return self._player2
    
    def add_score(self, score: int): 
        """Ajoute des points au score de l'équipe"""
        self._score += score

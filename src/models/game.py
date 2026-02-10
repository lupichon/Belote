"""
Module pour gérer une partie de Bélote
"""
from dataclasses import dataclass, field
from uuid import uuid4

from models.team import Team

@dataclass
class Game:
    """Représente une partie de Bélote"""
    _team1: Team
    _team2: Team
    _score1: int = 0
    _score2: int = 0
    _id: int = field(default_factory=lambda: uuid4().int) 
    
    @property
    def team1(self) -> Team:
        return self._team1

    @property
    def team2(self) -> Team:
        return self._team2
    
    @property
    def id(self) -> int:
        return self._id
    
    def set_scores(self, score1: int, score2: int):
        """Définit les scores pour les deux équipes"""
        self._score1 = score1
        self._score2 = score2
        self._team1.add_score(score1)
        self._team2.add_score(score2)
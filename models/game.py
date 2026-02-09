"""
Module pour gérer une partie de Bélote
"""
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime
from models.team import Team

@dataclass
class Game:
    """Représente une partie de Bélote"""
    _team1: Team
    _team2: Team
    
    @property
    def team1(self) -> Team:
        return self._team1

    @property
    def team2(self) -> Team:
        return self._team2
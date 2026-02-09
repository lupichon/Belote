"""
Module pour gérer les tournois de Bélote
"""
from dataclasses import dataclass, field
from typing import List
from models.game import Game
from models.team import Team


@dataclass
class Tournament:
    """Représente un tournoi de Bélote"""
    _teams: List[Team] = field(default_factory=list)
    _games: List[Game] = field(default_factory=list)

    @property
    def teams(self) -> List[Team]:
        """Retourne la liste des équipes du tournoi"""
        return self._teams.copy()
    
    @property
    def games(self) -> List[Game]:
        """Retourne la liste des matchs du tournoi"""
        return self._games.copy()
    
    def add_team(self, team: Team):
        """Ajoute une équipe au tournoi"""
        self._teams.append(team)

    def remove_team(self, team_name: str) -> bool: 
        """Supprime une équipe du tournoi par son nom"""
        for team in self._teams:
            if team.name == team_name:
                self._teams.remove(team)
                return True
        return False
    
    def clear_teams(self): 
        """Supprime toutes les équipes du tournoi"""
        self._teams.clear()
    
    def add_game(self, game: Game):
        """Ajoute un match au tournoi"""
        self._games.append(game)

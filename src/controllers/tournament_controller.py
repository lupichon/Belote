"""
Contrôleur pour gérer un tournoi de Bélote
"""
import random
from itertools import combinations
from typing import List, Set, Tuple
from dataclasses import dataclass, field

from models.team import Team
from models.player import Player
from models.tournament import Tournament
from models.game import Game

@dataclass
class TournamentController:
    """Contrôleur pour un tournoi de Bélote"""
    _tournament_model: Tournament = field(default_factory=Tournament)
    
    def add_team(self, team_name: str, player1_name: str, player2_name: str) -> bool: 
        # il faut aussi regarder que le nom d'équipe n'existe pas déjà
        if self._check_team_exists(team_name):
            return False
        
        player1 = Player(player1_name)
        player2 = Player(player2_name)
        team = Team(team_name, player1, player2)
        self._tournament_model.add_team(team)
        return True

    def remove_team(self, team_name: str) -> bool:
        if not self._check_team_exists(team_name):
            return False
        return self._tournament_model.remove_team(team_name)
    
    def remove_all_teams(self):
        self._tournament_model.clear_teams()

    def _check_team_exists(self, team_name: str) -> bool:
        return any(team.name == team_name for team in self._tournament_model.teams)

    def start_tournament(self) -> List[List['Game']]:
        """
        Génère 4 périodes de matchs pour un tournoi en Round-Robin.
        Chaque équipe joue exactement une fois par période et aucun match n'est répété.
        
        Returns:
            List[List[Game]] : liste des périodes, chaque période est une liste de Game
        """
        teams = self._tournament_model.teams
        num_teams = len(teams)
        
        if num_teams % 2 != 0:
            raise ValueError("Le round-robin classique nécessite un nombre pair d'équipes.")

        num_periods = 4  # nombre de périodes souhaité
        all_games: List[List['Game']] = []

        # Round-Robin : on fixe la première équipe et on fait tourner les autres
        fixed_team = teams[0]
        rotating_teams = teams[1:]

        for period in range(num_periods):
            period_games: List['Game'] = []

            # Création des paires
            pairs = []

            # Première paire avec l'équipe fixe
            pair = (fixed_team, rotating_teams[-1])
            pairs.append(pair)

            # Paires pour le reste des équipes
            for i in range(len(rotating_teams) // 2):
                pair = (rotating_teams[i], rotating_teams[-i-2])
                pairs.append(pair)

            # Créer les objets Game et ajouter au tournoi
            for team1, team2 in pairs:
                game = Game(team1, team2)
                period_games.append(game)
                self._tournament_model.add_game(game)

            all_games.append(period_games)

            # Affichage lisible
            print(f"\n=== Période {period + 1} ===")
            for i, game in enumerate(period_games, 1):
                print(f"Table {i}: {game.team1.name} vs {game.team2.name}")
            print(f"Total matchs période {len(period_games)}")

            # Rotation des équipes (excepté la première)
            rotating_teams = [rotating_teams[-1]] + rotating_teams[:-1]

        return all_games

    def validate_match(self, game_id: int, scores: tuple):
        """Valide les scores d'un match"""
        game = next((g for g in self._tournament_model.games if g.id == game_id), None)
        if game: 
            game.set_scores(scores[0], scores[1])

    def clear_tournament(self):
        """Réinitialise le tournoi en supprimant toutes les équipes et tous les matchs"""
        self._tournament_model.clear_teams()
        self._tournament_model.clear_games()
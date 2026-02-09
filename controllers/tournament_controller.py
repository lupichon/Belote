"""
Contrôleur pour gérer un tournoi de Bélote
"""
import random
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
    _number_of_matches_per_team: int = 4
    
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
        Génère 4 périodes de matchs pour le tournoi.
        Chaque équipe joue une fois par période contre une équipe aléatoire.
        Aucun match n'est rejoué.
        
        Returns:
            List[List[Game]] : liste des périodes, chaque période est une liste de Game
        """
        teams = self._tournament_model.teams
        num_periods = 4
        all_games: List[List['Game']] = []
        matchups_seen: Set[Tuple[str, str]] = set()  # pour éviter les doublons
        
        for period in range(1, num_periods + 1):
            print(f"\n=== Période {period} ===")
            available_teams = teams.copy()
            random.shuffle(available_teams)
            period_games: List['Game'] = []

            while available_teams:
                team1 = available_teams.pop(0)
                # Trouver un adversaire valide
                for i, team2 in enumerate(available_teams):
                    matchup_key = tuple(sorted([team1.name, team2.name]))
                    if matchup_key not in matchups_seen:
                        # Créer le match
                        game = Game(team1, team2)
                        period_games.append(game)
                        self._tournament_model.add_game(game)
                        matchups_seen.add(matchup_key)
                        # retirer team2 de la liste dispo
                        available_teams.pop(i)
                        break
                else:
                    # Si aucun adversaire valide n'est trouvé → reshuffle restant
                    random.shuffle(available_teams)

            all_games.append(period_games)

            # Affichage lisible pour cette période
            for i, game in enumerate(period_games, 1):
                print(f"Table {i}: {game.team1.name} vs {game.team2.name}")
            print(f"Total matchs période {period}: {len(period_games)}")


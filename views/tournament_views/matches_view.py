"""
Vue pour afficher les matchs d'un tournoi et saisir les scores
"""
from typing import List, Dict, TYPE_CHECKING
if TYPE_CHECKING:
    from views.main_window import MainWindow

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox,
    QPushButton, QScrollArea, QFrame, QMessageBox
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

from models.game import Game


class MatchCard(QFrame):
    """Widget pour afficher et éditer un match"""
    
    def __init__(self, game: Game, table_number: int, parent=None):
        super().__init__(parent)
        self.game = game
        self.table_number = table_number
        self.setObjectName("matchCard")
        self.setStyleSheet("""
            #matchCard {
                background-color: #2a2a40;
                border-radius: 10px;
                padding: 12px;
                border: 1px solid #3a3a5a;
            }
        """)
        
        layout = QHBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(10, 8, 10, 8)
        
        # Table number
        table_label = QLabel(f"Table {table_number}:")
        table_font = QFont()
        table_font.setBold(True)
        table_label.setFont(table_font)
        table_label.setMinimumWidth(60)
        layout.addWidget(table_label)
        
        # Équipe 1
        team1_label = QLabel(game.team1.name)
        team1_font = QFont()
        team1_font.setBold(True)
        team1_font.setPointSize(11)
        team1_label.setFont(team1_font)
        team1_label.setMinimumWidth(100)
        layout.addWidget(team1_label)
        
        # Score Équipe 1
        self.score1_spinbox = QSpinBox()
        self.score1_spinbox.setMinimum(0)
        self.score1_spinbox.setMaximum(999)
        self.score1_spinbox.setMaximumWidth(70)
        self.score1_spinbox.setStyleSheet("""
            QSpinBox {
                background-color: #3a3a5a;
                color: white;
                border: 1px solid #5a5a7a;
                border-radius: 5px;
                padding: 5px;
            }
        """)
        layout.addWidget(self.score1_spinbox)
        
        # vs
        vs_label = QLabel("vs")
        vs_font = QFont()
        vs_font.setBold(True)
        vs_label.setFont(vs_font)
        vs_label.setAlignment(Qt.AlignCenter)
        vs_label.setMinimumWidth(30)
        layout.addWidget(vs_label)
        
        # Score Équipe 2
        self.score2_spinbox = QSpinBox()
        self.score2_spinbox.setMinimum(0)
        self.score2_spinbox.setMaximum(999)
        self.score2_spinbox.setMaximumWidth(70)
        self.score2_spinbox.setStyleSheet("""
            QSpinBox {
                background-color: #3a3a5a;
                color: white;
                border: 1px solid #5a5a7a;
                border-radius: 5px;
                padding: 5px;
            }
        """)
        layout.addWidget(self.score2_spinbox)
        
        # Équipe 2
        team2_label = QLabel(game.team2.name)
        team2_font = QFont()
        team2_font.setBold(True)
        team2_font.setPointSize(11)
        team2_label.setFont(team2_font)
        team2_label.setMinimumWidth(100)
        layout.addWidget(team2_label)
        
        layout.addStretch()
        self.setMinimumHeight(50)
    
    def get_scores(self) -> tuple:
        """Retourne (score_team1, score_team2)"""
        return (self.score1_spinbox.value(), self.score2_spinbox.value())


class MatchesView(QWidget):
    """Vue pour gérer les matchs et scores du tournoi par périodes"""
    
    def __init__(self, parent: "MainWindow", matches_per_period: int = 4):
        super().__init__(parent)
        self.tournament_controller = parent.tournament_controller
        
        # Récupérer les games du controller
        self.games: List[Game] = self.tournament_controller._tournament_model.games
        self.matches_per_period = matches_per_period
        self.match_cards: List[MatchCard] = []
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        # Header
        header = QLabel("Matchs du tournoi")
        header_font = QFont()
        header_font.setPointSize(18)
        header_font.setBold(True)
        header.setFont(header_font)
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        # Sous-titre
        num_periods = (len(self.games) + matches_per_period - 1) // matches_per_period
        subtitle = QLabel(f"{len(self.games)} matchs - {num_periods} période(s)")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #bbbbbb; font-size: 12px;")
        layout.addWidget(subtitle)
        
        # Zone de scroll pour les matchs
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background-color: #2a2a40;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #5a5a7a;
                border-radius: 6px;
            }
        """)
        
        # Container pour les matchs
        matches_container = QWidget()
        matches_layout = QVBoxLayout(matches_container)
        matches_layout.setSpacing(12)
        matches_layout.setContentsMargins(0, 0, 0, 0)
        
        # Organiser les matchs par périodes
        for period_num in range(num_periods):
            start_idx = period_num * matches_per_period
            end_idx = min(start_idx + matches_per_period, len(self.games))
            
            # Titre de la période
            period_title = QLabel(f"=== Période {period_num + 1} ===")
            period_font = QFont()
            period_font.setPointSize(12)
            period_font.setBold(True)
            period_title.setFont(period_font)
            period_title.setStyleSheet("color: #66ccff; margin-top: 10px;")
            matches_layout.addWidget(period_title)
            
            # Matchs de cette période
            period_games = self.games[start_idx:end_idx]
            for table_num, game in enumerate(period_games, 1):
                match_card = MatchCard(game, table_num)
                self.match_cards.append(match_card)
                matches_layout.addWidget(match_card)
            
            # Nombre de matchs en bas de la période
            match_count = end_idx - start_idx
            count_label = QLabel(f"Total matchs période {period_num + 1}: {match_count}")
            count_label.setStyleSheet("color: #999999; font-size: 11px; margin-bottom: 8px;")
            matches_layout.addWidget(count_label)
        
        matches_layout.addStretch()
        scroll_area.setWidget(matches_container)
        layout.addWidget(scroll_area)
        
        # Boutons en bas
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(12)
        
        standings_btn = QPushButton("📊 Classement")
        standings_btn.setMinimumHeight(45)
        standings_btn.clicked.connect(self.on_view_standings)
        buttons_layout.addWidget(standings_btn)
        
        validate_btn = QPushButton("✓ Valider les scores")
        validate_btn.setMinimumHeight(45)
        validate_btn.clicked.connect(self.on_validate_scores)
        buttons_layout.addWidget(validate_btn)
        
        back_btn = QPushButton("← Retour")
        back_btn.setMinimumHeight(45)
        back_btn.clicked.connect(self.on_back)
        buttons_layout.addWidget(back_btn)
        
        layout.addLayout(buttons_layout)
        
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2f;
                color: white;
            }
            QPushButton {
                background-color: #3a3a5a;
                color: white;
                border-radius: 8px;
                border: none;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #50507a;
            }
            QPushButton:pressed {
                background-color: #2a2a45;
            }
        """)
    
    def get_scores_for_games(self) -> Dict[str, tuple]:
        """
        Retourne un dictionnaire map game_id → (score_team1, score_team2)
        """
        scores = {}
        for i, match_card in enumerate(self.match_cards):
            game_id = self.games[i].game_id
            score_team1, score_team2 = match_card.get_scores()
            scores[game_id] = (score_team1, score_team2)
        return scores
    
    def on_validate_scores(self):
        """Slot pour valider les scores"""
        print("Valider les scores")
        # Cette méthode sera connectée au Controller depuis MainWindow
    
    def on_view_standings(self):
        """Slot pour afficher le classement"""
        print("Afficher le classement")
        # Cette méthode sera connectée au Controller depuis MainWindow
    
    def on_back(self):
        """Slot pour retourner à la vue précédente"""
        print("Retour")
        # Cette méthode sera connectée à MainWindow pour changer de page

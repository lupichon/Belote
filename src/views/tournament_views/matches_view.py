"""
Vue pour afficher les matchs d'un tournoi et saisir les scores
Version UI améliorée - Lisible et claire
"""

from typing import List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from views.main_window import MainWindow

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox,
    QPushButton, QScrollArea, QFrame
)
from PySide6.QtCore import Qt, Signal

from models.game import Game
from views.tournament_views.matches_card import MatchCard

# =====================================================
# MatchesView
# =====================================================
class MatchesView(QWidget):
    """Vue principale affichant les matchs du tournoi"""
    tournament_standings_requested = Signal(bool) # True = tournoi terminé, False = juste afficher le classement

    def __init__(self, parent: "MainWindow", matches_per_period: int = 4):
        super().__init__(parent)

        self.tournament_controller = parent.tournament_controller
        self.games: List[Game] = self.tournament_controller._tournament_model.games
        self.matches_per_period = matches_per_period
        self.match_cards: List[MatchCard] = []

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)

        # =====================
        # Header
        # =====================
        header = QLabel("🏆 Matchs du tournoi")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: white;
        """)
        main_layout.addWidget(header)

        num_periods = (len(self.games) + matches_per_period - 1) // matches_per_period
        # =====================
        # Scroll Area
        # =====================
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("border: none;")

        matches_container = QWidget()
        matches_layout = QVBoxLayout(matches_container)
        matches_layout.setSpacing(15)

        # =====================
        # Génération périodes
        # =====================
        for period_num in range(num_periods):

            start_idx = period_num * matches_per_period
            end_idx = min(start_idx + matches_per_period, len(self.games))
            period_games = self.games[start_idx:end_idx]

            period_frame = QFrame()
            period_frame.setStyleSheet("""
                QFrame {
                    background-color: #252538;
                    border-radius: 12px;
                    border: 1px solid #3a3a5a;
                    padding: 12px;
                }
            """)

            period_layout = QVBoxLayout(period_frame)
            period_layout.setSpacing(10)

            period_title = QLabel(f"🕒 Période {period_num + 1}")
            period_title.setStyleSheet("""
                font-size: 14px;
                font-weight: bold;
                color: #66ccff;
            """)
            period_layout.addWidget(period_title)

            for table_num, game in enumerate(period_games, 1):
                match_card = MatchCard(game, table_num)
                match_card.controller_btn.clicked.connect(lambda _, mc=match_card: self._on_controller_match_btn_clicked(mc))
                self.match_cards.append(match_card)
                period_layout.addWidget(match_card)

            matches_layout.addWidget(period_frame)

        matches_layout.addStretch()
        scroll_area.setWidget(matches_container)
        main_layout.addWidget(scroll_area)

        # =====================
        # Boutons bas
        # =====================
        buttons_layout = QHBoxLayout()

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

        main_layout.addLayout(buttons_layout)

        # =====================
        # Style global
        # =====================
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2f;
                color: white;
                font-size: 13px;
            }

            QPushButton {
                background-color: #3a3a5a;
                border-radius: 8px;
                font-weight: bold;
                padding: 8px;
            }

            QPushButton:hover {
                background-color: #50507a;
            }

            QPushButton:pressed {
                background-color: #2a2a45;
            }
        """)

    # =====================================================
    # Slots UI
    # =====================================================
    def on_validate_scores(self):
        for match_card in self.match_cards:
            if not match_card.match_ended:
                match_card.controller_btn.click()  

        self.tournament_standings_requested.emit(True)
    
    def on_view_standings(self):
        self.tournament_standings_requested.emit(False)

    def on_back(self):
        print("Retour")

    def _on_controller_match_btn_clicked(self, mc: MatchCard):
        if not mc.match_ended:
            mc.match_ended = True
            mc.score1_spinbox.setDisabled(True)
            mc.score2_spinbox.setDisabled(True)
            mc.setStyleSheet("""
            #matchCard {
                background-color: #2a4a2f;   /* vert léger */
                border-radius: 10px;
                padding: 12px;
                border: 2px solid #66cc66;   /* bordure verte */
                }
            """)
            mc.controller_btn.setText("✗ Annuler")
            mc.controller_btn.setStyleSheet("""
                QPushButton {
                    background-color: #cc6666;   /* rouge léger */
                    color: white;
                    border-radius: 8px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #bb5555;
                }
                QPushButton:pressed {
                    background-color: #994444;
                }
            """)
            self.tournament_controller.validate_match(mc.game.id, mc.get_scores())
        else: 
            mc.match_ended = False
            mc.score1_spinbox.setDisabled(False)
            mc.score2_spinbox.setDisabled(False)
            mc.setStyleSheet("""
            #matchCard {
                background-color: #2a2a40;   /* couleur normale */
                border-radius: 10px;
                padding: 12px;
                border: 1px solid #3a3a5a;
                }
            """)
            mc.controller_btn.setText("✓ Valider")
            mc.controller_btn.setStyleSheet("""
                QPushButton {
                    background-color: #66cc66;
                    color: white;
                    border-radius: 8px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #55bb55;
                }
                QPushButton:pressed {
                    background-color: #449944;
                }
            """)

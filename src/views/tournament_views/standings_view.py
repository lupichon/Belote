"""
Vue pour afficher le classement final du tournoi
Affiche les équipes triées par score décroissant
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from views.main_window import MainWindow

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QFrame
)
from PySide6.QtCore import Qt


# =====================================================
# StandingsCard
# =====================================================
class StandingsCard(QFrame):
    """Carte visuelle pour afficher le classement d'une équipe"""

    def __init__(self, rank: int, team_name: str, score: int, parent=None):
        super().__init__(parent)

        self.setObjectName("standingsCard")
        self.setMinimumHeight(80)

        # Couleur de fond selon le rang
        if rank == 1:
            bg_color = "#3a5a2a"  # Vert
            border_color = "#5a7a4a"
            medal = "🥇"
        elif rank == 2:
            bg_color = "#3a4a5a"  # Bleu
            border_color = "#5a6a7a"
            medal = "🥈"
        elif rank == 3:
            bg_color = "#5a3a2a"  # Orange
            border_color = "#7a5a4a"
            medal = "🥉"
        else:
            bg_color = "#2a2a40"
            border_color = "#3a3a5a"
            medal = "  "

        self.setStyleSheet(f"""
            #standingsCard {{
                background-color: {bg_color};
                border-radius: 10px;
                border: 2px solid {border_color};
                padding: 12px;
            }}
        """)

        main_layout = QHBoxLayout(self)
        main_layout.setSpacing(20)

        # =====================
        # Rang et médaille
        # =====================
        rank_label = QLabel(f"{medal} #{rank}")
        rank_label.setAlignment(Qt.AlignCenter)
        rank_label.setStyleSheet("font-weight:bold; font-size: 18px; color:#66ccff; min-width: 80px;")
        main_layout.addWidget(rank_label)

        # =====================
        # Nom de l'équipe
        # =====================
        name_label = QLabel(team_name)
        name_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        name_label.setStyleSheet("font-weight:bold; font-size: 15px; color: white;")
        main_layout.addWidget(name_label)

        main_layout.addStretch()

        # =====================
        # Score
        # =====================
        score_label = QLabel(f"{score} pts")
        score_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        score_label.setStyleSheet("font-weight:bold; font-size: 16px; color:#ffcc66;")
        main_layout.addWidget(score_label)


# =====================================================
# StandingsView
# =====================================================
class StandingsView(QWidget):
    """Vue affichant le classement final du tournoi"""

    def __init__(self, parent: "MainWindow", tournament_ended: bool):
        super().__init__(parent)

        self.tournament_controller = parent.tournament_controller
        self.teams = self.tournament_controller._tournament_model.teams

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)

        # =====================
        # Header
        # =====================
        header = QLabel("🏆 Classement Final du Tournoi")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #ffcc66;
        """)
        main_layout.addWidget(header)

        # =====================
        # Scroll Area
        # =====================
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("border: none;")

        standings_container = QWidget()
        standings_layout = QVBoxLayout(standings_container)
        standings_layout.setSpacing(12)
        standings_layout.setContentsMargins(10, 10, 10, 10)

        # =====================
        # Trier les équipes par score décroissant
        # =====================
        sorted_teams = sorted(self.teams, key=lambda t: t._score, reverse=True)

        # =====================
        # Afficher chaque équipe
        # =====================
        for rank, team in enumerate(sorted_teams, 1):
            standings_card = StandingsCard(rank, team.name, team._score)
            standings_layout.addWidget(standings_card)

        standings_layout.addStretch()
        scroll_area.setWidget(standings_container)
        main_layout.addWidget(scroll_area)

        # =====================
        # Boutons bas
        # =====================
        buttons_layout = QHBoxLayout()

        self.back_button = QPushButton("← Retour")
        self.back_button.setMinimumHeight(45)
        buttons_layout.addWidget(self.back_button)

        self.restart_btn = None
        if tournament_ended: 
            self.restart_btn = QPushButton("🔄 Nouveau tournoi")
            self.restart_btn.setMinimumHeight(45)
            buttons_layout.addWidget(self.restart_btn)

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

            QScrollArea {
                background-color: transparent;
            }
        """)
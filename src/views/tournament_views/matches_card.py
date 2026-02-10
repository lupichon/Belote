from PySide6.QtWidgets import (
    QHBoxLayout, QLabel, QSpinBox,
    QPushButton, QFrame
)
from PySide6.QtCore import Qt

from models.game import Game

# =====================================================
# MatchCard
# =====================================================
class MatchCard(QFrame):
    """Carte visuelle pour afficher un match proprement"""

    def __init__(self, game: Game, table_number: int, parent=None):
        super().__init__(parent)

        self.game = game
        self.table_number = table_number
        self.match_ended = False

        self.setObjectName("matchCard")
        self.setMinimumHeight(100)

        self.setStyleSheet("""
            #matchCard {
                background-color: #2a2a40;
                border-radius: 10px;
                border: 1px solid #3a3a5a;
                padding: 12px;
            }
        """)

        main_layout = QHBoxLayout(self)
        main_layout.setSpacing(20)

        # =====================
        # Table
        # =====================
        table_label = QLabel(f"🪑 Table {table_number}")
        table_label.setStyleSheet("font-weight:bold; color:#bbbbff;")
        main_layout.addWidget(table_label)

        # =====================
        # Zone centrale match
        # =====================
        match_layout = QHBoxLayout()
        match_layout.setSpacing(15)

        team1_label = QLabel(game.team1.name)
        team1_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        team1_label.setStyleSheet("font-weight:bold;")

        self.score1_spinbox = QSpinBox()
        self.score1_spinbox.setMaximum(999)
        self.score1_spinbox.setFixedWidth(90)

        vs_label = QLabel("vs")
        vs_label.setAlignment(Qt.AlignCenter)
        vs_label.setStyleSheet("font-weight:bold; color:#aaaaaa;")

        self.score2_spinbox = QSpinBox()
        self.score2_spinbox.setMaximum(999)
        self.score2_spinbox.setFixedWidth(90)

        team2_label = QLabel(game.team2.name)
        team2_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        team2_label.setStyleSheet("font-weight:bold;")

        self.controller_btn = QPushButton("✓ Valider")
        self.controller_btn.setStyleSheet("""
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

        match_layout.addStretch()
        match_layout.addWidget(team1_label)
        match_layout.addWidget(self.score1_spinbox)
        match_layout.addWidget(vs_label)
        match_layout.addWidget(self.score2_spinbox)
        match_layout.addWidget(team2_label)
        match_layout.addStretch()
        #match_layout.addWidget(validate_btn)

        main_layout.addLayout(match_layout)
        main_layout.addStretch()
        main_layout.addWidget(self.controller_btn)

    def get_scores(self):
        return (
            self.score1_spinbox.value(),
            self.score2_spinbox.value()
        )
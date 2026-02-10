from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QStackedWidget, QFrame
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

from views.tournament_views.teams_creation_view import TeamsCreationView
from views.tournament_views.matches_view import MatchesView
from views.tournament_views.standings_view import StandingsView

from controllers.tournament_controller import TournamentController

class MainWindow(QMainWindow):
    """Fenêtre principale de l'application"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Application Bélote")
        self.tournament_controller = TournamentController()
        self.matches_view = None

        # =====================
        # Widget central
        # =====================
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(30, 20, 30, 20)
        main_layout.setSpacing(20)

        # =====================
        # Header / Title
        # =====================
        title = QLabel("🃏 Belote Manager")
        title_font = QFont()
        title_font.setPointSize(22)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        title.setObjectName("titleLabel")
        main_layout.addWidget(title)

        subtitle = QLabel("Gestion des matchs et des tournois")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setObjectName("subtitleLabel")
        main_layout.addWidget(subtitle)

        # =====================
        # Zone centrale (pages)
        # =====================
        self.stacked_widget = QStackedWidget()

        content_frame = QFrame()
        content_layout = QVBoxLayout(content_frame)
        content_layout.addWidget(self.stacked_widget)

        content_frame.setObjectName("contentFrame")
        main_layout.addWidget(content_frame)

        # =====================
        # Boutons navigation
        # =====================
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)

        self.tournament_button = self.create_menu_button("🏆 Tournoi")
        self.tournament_button.clicked.connect(self.on_init_tournament)
        button_layout.addWidget(self.tournament_button)

        main_layout.addLayout(button_layout)

        # =====================
        # Style global
        # =====================
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e2f;
            }

            #titleLabel {
                color: white;
            }

            #subtitleLabel {
                color: #bbbbbb;
                font-size: 14px;
            }

            #contentFrame {
                background-color: #2a2a40;
                border-radius: 12px;
                padding: 15px;
            }

            QPushButton {
                background-color: #3a3a5a;
                color: white;
                border-radius: 10px;
                padding: 14px;
                font-size: 14px;
            }

            QPushButton:hover {
                background-color: #50507a;
            }

            QPushButton:pressed {
                background-color: #2a2a45;
            }
        """)

        # Ouvrir maximisé
        self.showMaximized()

    # =====================
    # Factory bouton stylé
    # =====================
    def create_menu_button(self, text):
        btn = QPushButton(text)
        btn.setMinimumHeight(60)
        return btn

    # =====================
    # Slots (à compléter)
    # =====================
    def on_init_tournament(self):
        self.matches_view = None
        self.tournament_controller.clear_tournament()
        team_creation_view = TeamsCreationView(self)
        team_creation_view.start_btn.clicked.connect(self.go_to_matches_view)
        self.stacked_widget.addWidget(team_creation_view)
        self.stacked_widget.setCurrentWidget(team_creation_view)
        self.hide_selection_buttons()

    def go_to_matches_view(self):
        if self.matches_view is None: 
            self.matches_view = MatchesView(self)
            self.matches_view.tournament_standings_requested.connect(self.go_to_standings_view)
            self.stacked_widget.addWidget(self.matches_view)

        self.stacked_widget.setCurrentWidget(self.matches_view)
        self.hide_selection_buttons()

    def go_to_standings_view(self, is_tournament_ended):
        standings_view = StandingsView(self, is_tournament_ended)
        standings_view.back_button.clicked.connect(self.go_to_matches_view)
        if is_tournament_ended:
            standings_view.restart_btn.clicked.connect(self.on_init_tournament)

        self.stacked_widget.addWidget(standings_view)
        self.stacked_widget.setCurrentWidget(standings_view)
        self.hide_selection_buttons()

    # Méthodes
    # =====================
    def hide_selection_buttons(self):
        self.tournament_button.hide()

    def show_selection_buttons(self):
        self.tournament_button.show()

    
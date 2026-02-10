"""
Vue minimale pour créer un tournoi :
- Créer autant d'équipes que souhaité
- Ajouter pour chaque équipe deux joueurs (nom)

Cette vue ne lance pas encore le tournoi, elle collecte uniquement les équipes.
"""

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main_window import MainWindow

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QListWidget, QListWidgetItem, QMessageBox
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

class TeamsCreationView(QWidget):
    """Vue pour créer des équipes de tournoi"""

    def __init__(self, parent: MainWindow): 
        super().__init__(parent)
        self.tournament_controller = parent.tournament_controller

        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        header = QLabel("Création du tournoi")
        header_font = QFont()
        header_font.setPointSize(16)
        header_font.setBold(True)
        header.setFont(header_font)
        header.setAlignment(Qt.AlignLeft)

        layout.addWidget(header)

        # Formulaire d'ajout d'équipe
        form_layout = QHBoxLayout()

        self.team_name_edit = QLineEdit()
        self.team_name_edit.setPlaceholderText("Nom de l'équipe")
        form_layout.addWidget(self.team_name_edit)

        self.player1_edit = QLineEdit()
        self.player1_edit.setPlaceholderText("Joueur 1")
        form_layout.addWidget(self.player1_edit)

        self.player2_edit = QLineEdit()
        self.player2_edit.setPlaceholderText("Joueur 2")
        form_layout.addWidget(self.player2_edit)

        add_btn = QPushButton("Ajouter l'équipe")
        add_btn.clicked.connect(self._add_team)
        form_layout.addWidget(add_btn)

        layout.addLayout(form_layout)

        # Liste des équipes ajoutées
        self.teams_list = QListWidget()
        layout.addWidget(self.teams_list)

        # Boutons de gestion
        btn_layout = QHBoxLayout()
        remove_btn = QPushButton("Supprimer équipe sélectionnée")
        remove_btn.clicked.connect(self._remove_selected_team)
        btn_layout.addWidget(remove_btn)

        clear_btn = QPushButton("Tout effacer")
        clear_btn.clicked.connect(self._clear_teams)
        btn_layout.addWidget(clear_btn)

        self.start_btn = QPushButton("Lancer le tournoi")
        self.start_btn.setEnabled(False)
        self.start_btn.clicked.connect(self._start_tournament)
        btn_layout.addWidget(self.start_btn)

        layout.addLayout(btn_layout)

        self.auto_add_teams()  # TODO : A supprimer c'est juste pour les testes

    def _add_team(self):
        """Ajoute une équipe avec deux joueurs si le formulaire est valide"""
        team_name = self.team_name_edit.text().strip()
        p1 = self.player1_edit.text().strip()
        p2 = self.player2_edit.text().strip()

        if not team_name:
            QMessageBox.warning(self, "Erreur", "Le nom de l'équipe est requis.")
            return
        if not p1 or not p2:
            QMessageBox.warning(self, "Erreur", "Deux joueurs sont requis par équipe.")
            return

        #ajouter l'équipe au tournoi 
        if not self.tournament_controller.add_team(team_name, p1, p2): 
            QMessageBox.warning(self, "Erreur", f"Impossible d'ajouter l'équipe '{team_name}' : une équipe avec ce nom existe déjà.")
            return

        item = self._create_team_list_item(team_name, p1, p2)
        self.teams_list.addItem(item)
        self.start_btn.setEnabled(self._check_start_conditions())

        # Réinitialiser le formulaire
        self.team_name_edit.clear()
        self.player1_edit.clear()
        self.player2_edit.clear()
        self.team_name_edit.setFocus()

    def _remove_selected_team(self):
        idx = self.teams_list.currentRow()
        if idx < 0:
            return
        self.tournament_controller.remove_team(self._get_team_name_from_item(self.teams_list.item(idx)))
        self.teams_list.takeItem(idx)
        self.start_btn.setEnabled(self._check_start_conditions())

    def _clear_teams(self):
        self.teams_list.clear()
        self.tournament_controller.remove_all_teams()
        self.start_btn.setEnabled(self._check_start_conditions())

    def _create_team_list_item(self, team_name: str, p1: str, p2: str) -> QListWidgetItem:
        return QListWidgetItem(f"{team_name} — ({p1} / {p2})")
    
    def _get_team_name_from_item(self, item: QListWidgetItem) -> str:
        text = item.text()
        return text.split(" — ")[0]

    def _check_start_conditions(self) -> bool:
        return self.teams_list.count() >= 2
    
    def _start_tournament(self):
        self.tournament_controller.start_tournament()
        
        





    # TODO : A supprimer c'est juste pour les testes:
    def auto_add_teams(self):
        """Ajoute automatiquement des équipes pour les tests"""
        for i in range(1, 9):
            team_name = f"Team {i}"
            p1 = f"Player{i}A"
            p2 = f"Player{i}B"
            self.tournament_controller.add_team(team_name, p1, p2)
            item = self._create_team_list_item(team_name, p1, p2)
            self.teams_list.addItem(item)
        self.start_btn.setEnabled(self._check_start_conditions())

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QMenu,
    QMessageBox,
)

from PyQt6.QtCore import QDate, Qt

import database.project_db as project_db
from dialogs.edit_project_dialog import EditProjectDialog
from widgets.project_card import ProjectCard


class ProjectsPage(QWidget):

    def __init__(self, parent=None):
        super().__init__()

        self.main_window = parent

        layout = QVBoxLayout()

        toolbar = QHBoxLayout()

        title = QLabel("Projects")
        title.setStyleSheet("""
            font-size:26px;
            font-weight:bold;
            color:#1EA7FF;
        """)

        self.new_project_btn = QPushButton("+ New Project")

        toolbar.addWidget(title)
        toolbar.addStretch()
        toolbar.addWidget(self.new_project_btn)

        layout.addLayout(toolbar)

        self.project_list = QListWidget()

        layout.addWidget(self.project_list)

        self.setLayout(layout)

        self.load_projects()

        self.new_project_btn.clicked.connect(
        self.main_window.open_add_project
        )
        self.project_list.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu
        )

        self.project_list.customContextMenuRequested.connect(
            self.project_context_menu
        )

    def load_projects(self):

        self.project_list.clear()

        projects = project_db.get_all_projects()

      

        for project in projects:

            (
                project_id,
                name,
                deadline,
                estimated,
                worked,
                priority,
                progress,
                status
            ) = project

            remaining = max(0, estimated - worked)

            date = QDate.fromString(
                deadline,
                "yyyy-MM-dd"
            ).toString("dd MMM yyyy")


            card = ProjectCard(
            name,
            date,
            priority,
            estimated,
            worked,
            remaining,
            progress,
            status
            )


            item = QListWidgetItem()

            item.setSizeHint(card.sizeHint())

            item.setData(
                Qt.ItemDataRole.UserRole,
                project_id
            )

            card.edit_clicked.connect(
                lambda checked=False, i=item:
                self.edit_project(i)
            )


            card.delete_clicked.connect(
                lambda checked=False, pid=project_id:
                self.delete_project(pid)
            )

            self.project_list.addItem(item)

            self.project_list.setItemWidget(
                item,
                card
            )
            

    def project_context_menu(self, position):

        item = self.project_list.itemAt(position)

        if not item:
            return

        menu = QMenu()

        edit_action = menu.addAction("Edit Project")
        delete_action = menu.addAction("Delete Project")

        action = menu.exec(
            self.project_list.mapToGlobal(position)
        )

        if action == delete_action:

            project_id = item.data(
                Qt.ItemDataRole.UserRole
            )

            project_db.delete_project(project_id)

            self.load_projects()

            self.main_window.refresh_status_panels()

        elif action == edit_action:
            self.edit_project(item)

    def edit_project(self, item):

        project_id = item.data(
            Qt.ItemDataRole.UserRole
        )

        project = project_db.get_project(project_id)

        if project:

            (
                name,
                deadline,
                estimated_hours,
                priority
            ) = project

            dialog = EditProjectDialog(
                name,
                QDate.fromString(
                    deadline,
                    "yyyy-MM-dd"
                ),
                estimated_hours,
                priority
            )

            if dialog.exec():

                project_db.update_project(
                    project_id,
                    dialog.name_input.text(),
                    dialog.deadline_input.date().toString(
                        "yyyy-MM-dd"
                    ),
                    dialog.hours_input.value(),
                    dialog.priority_input.currentText()
                )

                self.load_projects()
                self.main_window.refresh_all()

    def delete_project(self, project_id):

        reply = QMessageBox.question(
            self,
            "Delete Project",
            "Are you sure you want to delete this project?\n\nThis action cannot be undone.",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )


        if reply == QMessageBox.StandardButton.Yes:

            project_db.delete_project(
                project_id
            )

            self.load_projects()

            self.main_window.refresh_status_panels()
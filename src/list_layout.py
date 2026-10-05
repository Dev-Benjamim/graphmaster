from dialogs import BaseDialog
from PySide6.QtWidgets import (
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout
)


class ListLayout(QVBoxLayout):
    """layout for a list"""

    def __init__(self, label: str, dialog: BaseDialog, update_slot) -> None:
        """
        :param label: text in the label
        :param dialog: BaseDialog object that will execute when the '+' is pressed
        :param update_slot: function that runs every the +/- is pressed
        """
        super().__init__()
        self.visual_list: QListWidget = QListWidget()
        self.list: list[tuple] = []
        self.active_soldier_index: None | int = None
        self.update = update_slot
        self.dialog: BaseDialog = dialog

        self.addWidget(QLabel(label.capitalize() + ':'))
        self.addWidget(self.visual_list)

        self.plus: QPushButton = QPushButton("+")
        self.minus: QPushButton = QPushButton("-")

        self.plus.clicked.connect(self.add_value_dialog)
        self.minus.clicked.connect(self.delete_value)

        buttons_layout: QHBoxLayout = QHBoxLayout()
        buttons_layout.addWidget(self.plus)
        buttons_layout.addWidget(self.minus)

        self.addLayout(buttons_layout)

    def get_list(self) -> list[tuple]:
        """
        :return: a list of tuples containing the values of the visual/actual list
        """
        return self.list

    def get_selected(self) -> int:
        """
        :return: selected QListWidgetItem index
        """
        return self.visual_list.currentRow()

    def get_active(self) -> None | int:
        """
        :return: active soldier
        """
        return self.active_soldier_index

    def add_value_dialog(self) -> None:
        """execute the dialog and add the response"""
        self.dialog.exec()
        if self.dialog.get_response() == ():
            return
        self.add_value(self.dialog.get_response())

    def add_value(self, value: tuple) -> None:
        """
        adds value to lists
        :param value: value to be added
        """
        self.list.append(value)
        self.visual_list.addItem(QListWidgetItem(str(value)))
        self.update()

    def delete_value(self) -> None:
        """deletes current row"""
        if self.get_selected() < 0:
            return

        if self.active_soldier_index == self.get_selected():
            self.active_soldier_index = None

        if self.active_soldier_index is not None and self.active_soldier_index > self.get_selected():
            self.active_soldier_index -= 1

        self.visual_list.takeItem(self.get_selected())
        self.list.pop(self.get_selected())
        self.update()

    def update_active(self) -> None:
        """sets active soldier to current row"""
        self.active_soldier_index = self.get_selected() if self.get_selected() >= 0 else None

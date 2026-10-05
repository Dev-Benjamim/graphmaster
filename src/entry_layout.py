from PySide6.QtWidgets import (
    QLineEdit,
    QHBoxLayout,
    QPushButton
)


class EntryLayout(QHBoxLayout):
    """layout for an entry"""

    def __init__(self, input_slot, button_slot) -> None:
        """
        :param input_slot: function that will be called when the text changes
        :param button_slot: function that will be called when button is pressed
        """
        super().__init__()
        self.input: QLineEdit = QLineEdit(placeholderText="Enter function", text="sin(x)")
        self.input.textChanged.connect(input_slot)
        self.addWidget(self.input)
        self.button: QPushButton = QPushButton("set active")
        self.button.clicked.connect(button_slot)
        self.addWidget(self.button)

    def text(self) -> str:
        """
        :return: text in input
        """
        return self.input.text()

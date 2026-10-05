from PySide6.QtCore import QSize
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QDoubleSpinBox,
    QWidget,
    QPushButton,
)


class BaseDialog(QDialog):
    """Dialog window."""

    def __init__(
        self,
        parent: QWidget | None = None,
        add_layout: bool = True,
    ) -> None:
        """
        :param parent: parent
        :param add_layout: automatically add layout?
        """
        super().__init__(parent)

        self.response: list[float | int] = []
        self.widgets: list[QWidget] = []

        self.x_spinbox = QDoubleSpinBox(minimum=-25, maximum=25)
        self.y_spinbox = QDoubleSpinBox(minimum=-15, maximum=15)
        self.submit_button = QPushButton("submit")

        self.widgets.extend([
            QLabel("x:"),
            self.x_spinbox,
            QLabel("y:"),
            self.y_spinbox,
            self.submit_button,
        ])

        self.submit_button.clicked.connect(self.submit)

        self.setWindowTitle("Adding item")
        self.setFixedSize(QSize(280, 50))

        if add_layout:
            self.add_layout()

    def submit(self) -> None:
        """update response and close the window"""
        self.response = [
            widget.value()
            for widget in self.widgets
            if isinstance(widget, QDoubleSpinBox)
        ]
        self.accept()

    def add_layout(self) -> None:
        """add all the widgets to a layout and set this layout"""
        layout = QHBoxLayout()

        for widget in self.widgets:
            layout.addWidget(widget)

        self.setLayout(layout)

    def get_response(self) -> tuple[float | int]:
        """
        :return: response as a tuple
        """
        return tuple(self.response)

class ObstacleDialog(BaseDialog):
    """Obstacle list layout dialog."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """
        :param parent: parent
        """
        super().__init__(parent, False)

        self.radius_spinbox = QDoubleSpinBox(
            minimum=0,
            maximum=50,
        )

        self.widgets.insert(4, QLabel("r:"))
        self.widgets.insert(5, self.radius_spinbox)

        self.add_layout()
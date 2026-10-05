from dialogs import BaseDialog, ObstacleDialog
from entry_layout import EntryLayout
from list_layout import ListLayout
from graph import Graph
from PySide6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QWidget
)


class Window(QMainWindow):
    """Main application window"""

    def __init__(self) -> None:
        super().__init__()

        main_layout = QVBoxLayout()

        self.soldiers: ListLayout = ListLayout("soldier", BaseDialog(self), self.plot_graph)
        self.obstacles: ListLayout = ListLayout("obstacle", ObstacleDialog(self), self.plot_graph)

        self.graph: Graph = Graph()
        self.entry: EntryLayout = EntryLayout(self.plot_graph, self.update_active)

        self.graph.clicked_signal.connect(self.add_soldier)

        main_layout.addWidget(self.graph)
        main_layout.addLayout(self.entry)

        lists_layout: QHBoxLayout = QHBoxLayout()

        lists_layout.addLayout(self.soldiers)
        lists_layout.addLayout(self.obstacles)

        main_layout.addLayout(lists_layout)

        main_container: QWidget = QWidget()
        main_container.setLayout(main_layout)

        self.setWindowTitle("GraphMaster")
        self.setCentralWidget(main_container)

        self.plot_graph()

    def plot_graph(self) -> None:
        """updates the graph"""
        self.graph.plot_graph(self.entry.text(), self.soldiers.get_list(), self.obstacles.get_list(), self.soldiers.get_active())

    def update_active(self) -> None:
        """updates the active soldier"""
        self.soldiers.update_active()
        self.plot_graph()

    def add_soldier(self, x: float | int, y: float | int) -> None:
        """
        adds a soldier to soldiers
        :param x: x position of the soldier
        :param y: y position of the soldier
        """
        self.soldiers.add_value((x, y))

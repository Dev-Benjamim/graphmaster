from PySide6.QtCore import QSize, Signal
from config import Config
import pyqtgraph as pg
import sympy as sp
import numpy as np


class Graph(pg.PlotWidget):
    """Graph widget"""
    clicked_signal = Signal(float, float)

    def __init__(self):
        super().__init__()
        self.showGrid(x=True, y=True)
        # noinspection argument-list
        self.setRange(xRange=(-25, 25), yRange=(-15, 15), padding=0)
        self.setBackground(Config.graph_color)
        self.setMouseEnabled(x=False, y=False)
        self.getViewBox().menu.clear()
        self.setFixedSize(QSize(800, 600))
        self.setAspectLocked(True)
        # noinspection unresolved-references
        self.scene().sigMouseClicked.connect(self.click)

    def plot_graph(self, text: str, soldiers: list[tuple], obstacles: list[tuple], active: None | int) -> None:
        """
        tries to update the graph
        :param text: function text
        :param soldiers: list of soldiers - soldier format: (x,y)
        :param obstacles: list of obstacles - obstacle format: (x,y,r)
        :param active: active solder index
        """
        try:
            # add ^ support as power operator
            text = text.replace("^", "**")

            # clear graph
            self.clear()

            # draw soldiers
            theta = np.linspace(0, 2 * np.pi, Config.precision)
            for i, soldier in enumerate(soldiers):
                color = Config.soldier_color
                if i == active:
                    color = Config.active_color
                self.plot(
                    soldier[0] + np.cos(theta),
                    soldier[1] + np.sin(theta),
                    pen=pg.mkPen(color, width=Config.soldier_width)
                )

            # draw obstacles
            for obstacle in obstacles:
                self.plot(
                    obstacle[0] + obstacle[2] * np.cos(theta),
                    obstacle[1] + obstacle[2] * np.sin(theta),
                    pen=pg.mkPen(Config.obstacle_color, width=Config.obstacle_width)
                )

            # generate function (can easily fail)
            f = sp.lambdify(
                sp.symbols("x"),
                text,
                "numpy"
            )

            # generate x & y arrays
            xs: np.ndarray = np.linspace(-25, 25, Config.precision)
            ys: np.ndarray = np.asarray(f(xs), dtype=float)

            # move function so it passes through the active soldier
            if active is not None and 0 <= active < len(soldiers):
                soldier_x, soldier_y = soldiers[active]
                function_y = float(f(soldier_x))
                offset = soldier_y - function_y
                ys += offset

            # update graph
            self.plot(
                xs,
                ys,
                pen=pg.mkPen(color=Config.function_color, width=Config.function_width)
            )

        except (SyntaxError, TypeError, NameError, RuntimeWarning) as e:
            print(e)
            pass

    def click(self, event) -> None:
        """send signal and position of the click"""
        # noinspection unresolved-references
        point = self.plotItem.vb.mapSceneToView(event.scenePos())
        self.clicked_signal.emit(point.x(), point.y())

from dataclasses import dataclass

@dataclass
class Config:
    """configuration values data class"""
    graph_color: str = "black"
    soldier_color: str = "yellow"
    obstacle_color: str = "white"
    active_color: str = "red"
    function_color: str = "green"
    soldier_width: float | int = 1
    obstacle_width: float | int = 2
    function_width: float | int = 3
    precision: int = 10000
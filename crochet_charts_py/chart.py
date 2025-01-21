import dearpygui.dearpygui as dpg
from enum import Enum, auto
from typing import Optional, List, Tuple
from stitch import PlacedStitch, Stitch

class ChartStyle(Enum):
    ROWS = auto()    # flat chart rows calculated based on grid
    ROUNDS = auto()  # round chart rows calculated with trig
    BLANK = auto()   # start with no stitches and allow anything

class Chart:
    def __init__(self, style: ChartStyle = ChartStyle.BLANK, width: int = 20, height: int = 20):
        self.style = style
        self.grid_size = 20  # pixels per grid cell
        self.width = width   # number of grid cells
        self.height = height # number of grid cells
        self.grid_visible = True
        self.guidelines_visible = True
        self.stitches: List[PlacedStitch] = []
        
    def add_stitch(self, stitch: Stitch, grid_x: int, grid_y: int) -> bool:
        """Add a stitch to the chart at the given grid position"""
        if 0 <= grid_x < self.width and 0 <= grid_y < self.height:
            # Remove any existing stitch at this position
            self.remove_stitch_at(grid_x, grid_y)
            # Add the new stitch
            placed_stitch = PlacedStitch(stitch, grid_x, grid_y)
            self.stitches.append(placed_stitch)
            return True
        return False
    
    def get_stitch_at(self, grid_x: int, grid_y: int) -> Optional[PlacedStitch]:
        """Get the stitch at the given grid position"""
        for stitch in reversed(self.stitches):  # Reverse to get top-most stitch
            if stitch.grid_x == grid_x and stitch.grid_y == grid_y:
                return stitch
        return None
    
    def remove_stitch_at(self, grid_x: int, grid_y: int) -> bool:
        """Remove the stitch at the given grid position"""
        stitch = self.get_stitch_at(grid_x, grid_y)
        if stitch:
            self.stitches.remove(stitch)
            return True
        return False
    
    def pixel_to_grid(self, x: float, y: float) -> Tuple[int, int]:
        """Convert pixel coordinates to grid coordinates"""
        # Account for padding in the drawlist (8px on each side)
        # Use round() instead of int() to get to the nearest grid point
        grid_x = round((x - 8) / self.grid_size)
        grid_y = round((y - 8) / self.grid_size)
        return (grid_x, grid_y)
        
    def draw(self, drawlist_id: str):
        """Draw the chart on the given drawlist"""
        # Clear existing items in drawlist
        dpg.delete_item(drawlist_id, children_only=True)
        
        # Draw grid if visible
        if self.grid_visible:
            color = [128, 128, 128, 64]  # light gray, semi-transparent
            # Vertical lines
            for i in range(0, self.width * self.grid_size + 1, self.grid_size):
                dpg.draw_line(parent=drawlist_id,
                            p1=[i, 0],
                            p2=[i, self.height * self.grid_size],
                            color=color)
            # Horizontal lines
            for i in range(0, self.height * self.grid_size + 1, self.grid_size):
                dpg.draw_line(parent=drawlist_id,
                            p1=[0, i],
                            p2=[self.width * self.grid_size, i],
                            color=color)
        
        # Draw guidelines if visible and in ROWS style
        if self.guidelines_visible and self.style == ChartStyle.ROWS:
            color = [0, 128, 255, 128]  # blue, semi-transparent
            for i in range(0, self.height * self.grid_size, self.grid_size * 2):
                dpg.draw_line(parent=drawlist_id,
                            p1=[0, i],
                            p2=[self.width * self.grid_size, i],
                            color=color,
                            thickness=2)
        
        # Draw all stitches
        for stitch in self.stitches:
            stitch.draw(drawlist_id, self.grid_size)

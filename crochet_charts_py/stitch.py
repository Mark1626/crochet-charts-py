from dataclasses import dataclass
from pathlib import Path
import dearpygui.dearpygui as dpg
from cairosvg import svg2png
from io import BytesIO
from PIL import Image
from typing import Optional
import numpy as np

@dataclass
class Stitch:
    name: str
    svg_file: str
    color: tuple[int, int, int, int] = (255, 255, 255, 255)
    width: int = 1
    height: int = 1
    _texture_id: Optional[int] = None

    def __post_init__(self):
        self._load_texture()

    def _load_texture(self):
        if self._texture_id is not None:
            return

        # Get the path to the SVG file
        assets_dir = Path(__file__).parent.parent / "assets" / "stitches"
        svg_path = assets_dir / self.svg_file

        # Convert SVG to PNG in memory
        png_data = svg2png(url=str(svg_path), output_width=20, output_height=20)
        
        # Convert PNG to RGBA using PIL
        img = Image.open(BytesIO(png_data))
        img = img.convert("RGBA")
        
        # Convert to numpy array and normalize to 0-1 range
        img_array = np.array(img)
        img_array = img_array.astype(np.float32) / 255.0
        
        # Create texture registry if it doesn't exist
        if not dpg.does_alias_exist("__texture_registry"):
            with dpg.texture_registry() as registry:
                dpg.add_alias("__texture_registry", registry)
        
        # Create DPG texture
        width, height = img.size
        self._texture_id = dpg.add_static_texture(
            width=width,
            height=height,
            default_value=img_array.ravel().tolist(),
            parent="__texture_registry",
            tag=self.name
        )

class PlacedStitch:
    def __init__(self, stitch: Stitch, grid_x: int, grid_y: int, rotation: float = 0.0):
        self.stitch = stitch
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.rotation = rotation

    def draw(self, drawlist_id: int, grid_size: int):
        # Calculate position (center of grid cell)
        x = (self.grid_x + 0.5) * grid_size
        y = (self.grid_y + 0.5) * grid_size

        # Draw the stitch texture
        dpg.draw_image(
            self.stitch.name,
            parent=drawlist_id,
            pmin=[x - grid_size/2, y - grid_size/2],  # Top-left corner
            pmax=[x + grid_size/2, y + grid_size/2],  # Bottom-right corner
        )

class StitchLibrary:
    def __init__(self):
        dpg.create_context()  # Ensure DPG context exists
        self.stitches = {
            "ch": Stitch("Chain", "ch.svg"),
            "sc": Stitch("Single Crochet", "sc.svg"),
            "dc": Stitch("Double Crochet", "dc.svg"),
            "tr": Stitch("Triple Crochet", "tr.svg"),
            "sl": Stitch("Slip Stitch", "sl_st.svg"),
            "hdc": Stitch("Half Double Crochet", "hdc.svg")
        }
        self.selected_stitch = "ch"

    def get_stitch(self, stitch_name: str) -> Optional[Stitch]:
        return self.stitches.get(stitch_name)

    def get_selected_stitch(self) -> Stitch:
        return self.get_stitch(self.selected_stitch)

    def set_selected_stitch(self, stitch_name: str):
        if stitch_name in self.stitches:
            self.selected_stitch = stitch_name

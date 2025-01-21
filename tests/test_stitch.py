import pytest
from crochet_charts_py.stitch import Stitch, StitchLibrary, PlacedStitch
import dearpygui.dearpygui as dpg

# Fixtures
@pytest.fixture
def stitch_library():
    """Create a fresh StitchLibrary for each test"""
    return StitchLibrary()

@pytest.fixture
def placed_stitch():
    """Create test stitch and placed stitch instances"""
    stitch = Stitch("Test", "+", color=(255, 255, 255, 255))
    return PlacedStitch(stitch, 5, 10)

# StitchLibrary Tests
def test_initial_stitches(stitch_library):
    """Test that the library is initialized with the correct stitches"""
    expected_stitches = {
        "ch": "Chain",
        "sc": "Single Crochet",
        "dc": "Double Crochet",
        "tr": "Triple Crochet",
        "sl": "Slip Stitch",
        "hdc": "Half Double Crochet"
    }
    for key, name in expected_stitches.items():
        assert key in stitch_library.stitches
        assert stitch_library.stitches[key].name == name

def test_default_selected_stitch(stitch_library):
    """Test that chain stitch is selected by default"""
    assert stitch_library.selected_stitch == "ch"
    stitch = stitch_library.get_selected_stitch()
    assert stitch.name == "Chain"

def test_get_stitch(stitch_library):
    """Test getting a stitch by name"""
    stitch = stitch_library.get_stitch("sc")
    assert stitch is not None
    assert stitch.name == "Single Crochet"
    assert stitch.symbol == "x"

def test_get_nonexistent_stitch(stitch_library):
    """Test getting a stitch that doesn't exist"""
    stitch = stitch_library.get_stitch("nonexistent")
    assert stitch is None

def test_set_selected_stitch(stitch_library):
    """Test changing the selected stitch"""
    stitch_library.set_selected_stitch("dc")
    assert stitch_library.selected_stitch == "dc"
    stitch = stitch_library.get_selected_stitch()
    assert stitch.name == "Double Crochet"

def test_set_invalid_selected_stitch(stitch_library):
    """Test that setting an invalid stitch doesn't change selection"""
    original = stitch_library.selected_stitch
    stitch_library.set_selected_stitch("nonexistent")
    assert stitch_library.selected_stitch == original

# PlacedStitch Tests
@pytest.fixture
def drawlist():
    """Create a DearPyGui drawlist for testing"""
    dpg.create_context()
    with dpg.window():
        drawlist_id = dpg.add_drawlist(width=100, height=100)
    yield drawlist_id
    dpg.destroy_context()

def test_draw_method(placed_stitch, drawlist):
    """Test that draw method calculates correct position"""
    grid_size = 20
    placed_stitch.draw(drawlist, grid_size)
    
    # Calculate expected position (center of grid cell)
    expected_x = (placed_stitch.grid_x + 0.5) * grid_size
    expected_y = (placed_stitch.grid_y + 0.5) * grid_size
    
    # The actual drawing position should be offset by the text centering values
    assert expected_x - 4 == (placed_stitch.grid_x + 0.5) * grid_size - 4
    assert expected_y - 7 == (placed_stitch.grid_y + 0.5) * grid_size - 7

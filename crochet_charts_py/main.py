import dearpygui.dearpygui as dpg
from chart import Chart, ChartStyle
from stitch import StitchLibrary
import os

class CrochetChartsApp:
    def __init__(self):
        self.stitch_library = StitchLibrary()
        self.is_placing_stitch = True
        # Initialize preview with default stitch
        stitch = self.stitch_library.get_selected_stitch()
        self.preview_text = stitch.name
        # Start with a default chart
        self.current_chart = Chart(style=ChartStyle.BLANK, width=20, height=20)
        if self.current_chart:
            self.create_chart_canvas()
            self.current_chart.draw("chart_drawlist")

    def create_new_chart_dialog(self):
        with dpg.window(label="New Chart", modal=True, show=True, tag="new_chart_dialog",
                       width=300, height=200, pos=[400, 300]):
            dpg.add_text("Select chart type:")
            dpg.add_radio_button(tag="chart_type", items=["Rows", "Rounds", "Blank"], default_value="Blank")
            dpg.add_separator()
            dpg.add_text("Chart size:")
            dpg.add_input_int(label="Width", default_value=20, tag="chart_width")
            dpg.add_input_int(label="Height", default_value=20, tag="chart_height")
            dpg.add_separator()
            
            with dpg.group(horizontal=True):
                dpg.add_button(label="Create", callback=self.create_new_chart)
                dpg.add_button(label="Cancel", callback=lambda: dpg.delete_item("new_chart_dialog"))
    
    def create_new_chart(self):
        # Get values from dialog
        chart_type = dpg.get_value("chart_type")
        width = dpg.get_value("chart_width")
        height = dpg.get_value("chart_height")
        
        # Convert string type to ChartStyle enum
        style_map = {
            "Rows": ChartStyle.ROWS,
            "Rounds": ChartStyle.ROUNDS,
            "Blank": ChartStyle.BLANK
        }

        # if self.current_chart:
        #     dpg.delete_item("chart_drawlist")
        
        # Create new chart
        self.current_chart = Chart(style=style_map[chart_type], width=width, height=height)
        
        # Update chart display
        if self.current_chart:
            self.current_chart.draw("chart_drawlist")
        
        # Close dialog
        dpg.delete_item("new_chart_dialog")
    
    def handle_chart_click(self, sender, app_data):
        if not self.current_chart or not self.is_placing_stitch:
            return
            
        # Get mouse position in screen coordinates
        mouse_pos = dpg.get_mouse_pos(local=False)
        
        # Get window position and account for window decorations
        window_pos = dpg.get_item_pos("chart_canvas")
        window_padding = 8  # DearPyGui default window padding
        title_bar = 20     # Approximate title bar height
        
        # Convert to coordinates relative to drawlist
        local_x = mouse_pos[0] - window_pos[0] - window_padding
        local_y = mouse_pos[1] - window_pos[1] - title_bar - window_padding
        
        # Convert to grid coordinates
        grid_x, grid_y = self.current_chart.pixel_to_grid(local_x, local_y)
        
        # Ensure we're within grid bounds
        if 0 <= grid_x < self.current_chart.width and 0 <= grid_y < self.current_chart.height:
            # Get the current stitch
            stitch = self.stitch_library.get_selected_stitch()
            if stitch:
                # Add stitch to chart
                self.current_chart.add_stitch(stitch, grid_x, grid_y)
                # Redraw chart
                self.current_chart.draw("chart_drawlist")
    
    def toggle_stitch_placement(self, sender):
        self.is_placing_stitch = not self.is_placing_stitch
        # Update button text
        dpg.configure_item(
            "add_stitch_button", 
            label="Stop Placing" if self.is_placing_stitch else "Add Stitch"
        )
    
    def select_stitch(self, sender, app_data):
        self.stitch_library.set_selected_stitch(app_data)
        # Update preview
        stitch = self.stitch_library.get_selected_stitch()
        self.preview_text = stitch.name
        dpg.set_value("stitch_preview", self.preview_text)
        
    def create_menus(self):
        with dpg.menu_bar(tag="main_menu_bar"):
            with dpg.menu(label="File"):
                dpg.add_menu_item(label="New", callback=self.create_new_chart_dialog)
                # dpg.add_menu_item(label="Open", callback=lambda: print("Open"))
                # dpg.add_menu_item(label="Save", callback=lambda: print("Save"))
                # dpg.add_menu_item(label="Save As", callback=lambda: print("Save As"))
                # dpg.add_separator()
                # dpg.add_menu_item(label="Export", callback=lambda: print("Export"))
                dpg.add_separator()
                dpg.add_menu_item(label="Exit", callback=lambda: dpg.stop_dearpygui())
            
            # with dpg.menu(label="Edit"):
            #     dpg.add_menu_item(label="Undo", callback=lambda: print("Undo"))
            #     dpg.add_menu_item(label="Redo", callback=lambda: print("Redo"))
            #     dpg.add_separator()
            #     dpg.add_menu_item(label="Cut", callback=lambda: print("Cut"))
            #     dpg.add_menu_item(label="Copy", callback=lambda: print("Copy"))
            #     dpg.add_menu_item(label="Paste", callback=lambda: print("Paste"))
            
            # with dpg.menu(label="View"):
            #     dpg.add_menu_item(label="Show Grid", callback=lambda: print("Show Grid"))
            #     dpg.add_menu_item(label="Show Guidelines", callback=lambda: print("Show Guidelines"))

    def create_toolbar(self):
        with dpg.group(horizontal=True, tag="main_toolbar"):
            dpg.add_button(label="New", callback=self.create_new_chart_dialog)
            # dpg.add_button(label="Open", callback=lambda: print("Open"))
            # dpg.add_button(label="Save", callback=lambda: print("Save"))
            # dpg.add_separator()
            # dpg.add_button(label="Undo", callback=lambda: print("Undo"))
            # dpg.add_button(label="Redo", callback=lambda: print("Redo"))
            # dpg.add_separator()

    def create_properties_panel(self):
        with dpg.window(label="Properties", pos=[0, 60], width=250, height=570, tag="properties_panel"):
            with dpg.tab_bar():
                with dpg.tab(label="Stitches"):
                    dpg.add_text("Stitch Library")
                    # Add radio buttons for stitch selection
                    dpg.add_radio_button(
                        items=list(self.stitch_library.stitches.keys()),
                        callback=self.select_stitch,
                        default_value=self.stitch_library.selected_stitch
                    )
                    # Add stitch preview
                    with dpg.group():
                        dpg.add_text("Selected Stitch:")
                        dpg.add_text(self.preview_text, tag="stitch_preview")
                    
                    dpg.add_separator()
                    # Add stitch placement button
                    dpg.add_button(
                        label="Stop Placing",
                        callback=self.toggle_stitch_placement,
                        tag="add_stitch_button"
                    )
                    dpg.add_button(label="Add Color", callback=lambda: print("Add Color"))
                
                with dpg.tab(label="Colors"):
                    dpg.add_text("Color Palette")
                    # Add color palette items here
    
    def create_chart_canvas(self):
        with dpg.window(label="Chart", pos=[250, 60], width=800, height=570, tag="chart_canvas"):
            with dpg.drawlist(width=780, height=550, tag="chart_drawlist") as drawlist:
                # Add mouse click handler
                with dpg.handler_registry():
                    dpg.add_mouse_click_handler(callback=self.handle_chart_click)

def main():
    dpg.create_context()
    dpg.create_viewport(title="Crochet Charts", width=1280, height=800)

    app = CrochetChartsApp()
    
    # Create the main window that will contain everything
    with dpg.window(label="Crochet Charts", tag="main_window", no_title_bar=True, 
                   no_resize=True, no_move=True, no_collapse=True):
        app.create_menus()
        app.create_toolbar()
    
    # Create dockable windows
    app.create_properties_panel()
    # app.create_chart_canvas()

    # Show viewport and start the application
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("main_window", True)
    
    while dpg.is_dearpygui_running():
        dpg.render_dearpygui_frame()
    
    dpg.destroy_context()

if __name__ == "__main__":
    main()
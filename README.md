# Crochet Charts Py

A Python-based application for creating and editing crochet charts. Built using DearPyGui.

This project is a complete rewrite of [CrochetCharts](https://github.com/iPenguin/CrochetCharts). Credits to the original author(s) for their work. Stitch artwork is taken from the original repo, licensed by the author [iPenguin](https://github.com/iPenguin) under Creative Commons Attribution-ShareAlike ( cc by-sa 4.0 ).


## Installation

1. Make sure you have Python 3.11+ and Poetry installed
2. Clone the repository:
   ```bash
   git clone https://github.com/mark1626/crochet-charts-py.git
   cd crochet-charts-py
   ```
3. Install dependencies:
   ```bash
   poetry install
   ```

## Development

### Running the Application
```bash
poetry run python crochet_charts_py/main.py
```

### Running Tests
```bash
poetry run pytest tests/
```

## Usage

1. Launch the application
2. Click "New" to create a new chart
3. Select a stitch type from the Properties panel
4. Click on the grid to place stitches
5. Click "Stop Placing" to exit stitch placement mode

## License

This project is open source and available under the [GNU GPL License](LICENSE).

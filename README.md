# Directory Size Analyzer

A modern, user-friendly GUI application built with PyQt5 that helps you analyze and visualize directory sizes on your system. The application provides an interactive tree view of directory structures with customizable depth and expansion options.

![image](https://github.com/user-attachments/assets/6c19b6af-1796-46a1-b3dd-36bd91ba820e)


## Features

- 📊 Visual directory size analysis
- 🎯 Customizable scan depth and expansion options
- 🚀 Non-blocking scan operations
- 🎯 Directory size visualization in human-readable format

## Requirements

- Python 3.6 or higher
- PyQt5
- qt-material

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ayushd08/directory-size-analyzer.git
cd directory-size-analyzer
```

2. Create and activate a virtual environment (optional but recommended):
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python dir_size_analyzer.py
```

### Using the Application

1. Click the "Browse" button to select a directory to analyze
2. Adjust the scan parameters:
   - "Expand Top N": Number of largest subdirectories to show at each level
   - "Maximum Scan Depth": How deep the scan should go into subdirectories
3. Click "Start Scan" to begin the analysis
4. The results will be displayed in a tree view, with directory sizes shown in human-readable format

### Tips

- Hover over directory names to see their full paths
- The tree view supports keyboard navigation
- Use the status bar at the bottom for feedback during operations
- The scan operation is non-blocking, so you can still interact with the application during scanning

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [PyQt5](https://www.riverbankcomputing.com/software/pyqt/)
- Styled with [Qt-Material](https://github.com/UN-GCPDS/qt-material)

## Troubleshooting

### Common Issues

1. **ImportError: No module named 'PyQt5'**
   - Ensure you've installed all requirements: `pip install -r requirements.txt`

2. **High DPI Display Issues**
   - The application supports high DPI scaling by default. If you experience any scaling issues, try setting the environment variable `QT_AUTO_SCREEN_SCALE_FACTOR=1`

3. **Permission Errors**
   - Ensure you have read permissions for the directories you're trying to scan
   - On Linux/macOS, you might need to run with sudo for system directories

### Getting Help

If you encounter any issues:
1. Check the existing GitHub issues
2. Create a new issue with:
   - Your operating system and Python version
   - Steps to reproduce the problem
   - Any error messages you received

## Development

### Building from Source

1. Clone the repository
2. Install development dependencies:
```bash
pip install -r requirements.txt
```

### Running Tests

```bash
python -m unittest tests/
```

### Code Style

This project follows PEP 8 guidelines. Before submitting a pull request:
1. Format your code using black
2. Run flake8 for linting

import os
import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from qt_material import apply_stylesheet

class CustomTreeWidget(QtWidgets.QTreeWidget):
    def __init__(self):
        super().__init__()
        # Enable alternating row colors for better readability
        self.setAlternatingRowColors(True)
        # Custom styling
        self.setStyleSheet("""
            QTreeWidget {
                border-radius: 8px;
                padding: 5px;
            }
            QTreeWidget::item {
                padding: 5px;
                min-height: 25px;
            }
        """)

class DirSizeWidget(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Directory Size Analyzer")
        self.resize(1000, 700)
        self.setMinimumSize(800, 500)
        
        # Set window icon (using system icon)
        self.setWindowIcon(self.style().standardIcon(QtWidgets.QStyle.SP_DirIcon))
        
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        layout = QtWidgets.QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header with title and description
        header_layout = QtWidgets.QVBoxLayout()
        title_label = QtWidgets.QLabel("Directory Size Analyzer")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 10px;")
        desc_label = QtWidgets.QLabel("Analyze and visualize directory sizes with customizable depth and expansion options")
        desc_label.setStyleSheet("font-size: 14px; color: #666;")
        header_layout.addWidget(title_label)
        header_layout.addWidget(desc_label)
        layout.addLayout(header_layout)
        
        # Folder Selection Card
        folder_card = self.create_card("Folder Selection")
        folder_layout = QtWidgets.QHBoxLayout(folder_card)
        folder_layout.setContentsMargins(15, 15, 15, 15)
        folder_layout.setSpacing(10)
        
        self.folder_line_edit = QtWidgets.QLineEdit()
        self.folder_line_edit.setPlaceholderText("Select a folder to analyze...")
        self.folder_line_edit.setMinimumHeight(35)
        self.folder_line_edit.setStyleSheet("border-radius: 4px;")
        
        self.folder_button = QtWidgets.QPushButton("Browse")
        self.folder_button.setMinimumHeight(35)
        self.folder_button.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_DirIcon))
        self.folder_button.clicked.connect(self.select_folder)
        
        folder_layout.addWidget(QtWidgets.QLabel("Folder:"))
        folder_layout.addWidget(self.folder_line_edit)
        folder_layout.addWidget(self.folder_button)
        layout.addWidget(folder_card)
        
        # Parameters Card
        param_card = self.create_card("Scan Parameters")
        param_layout = QtWidgets.QHBoxLayout(param_card)
        param_layout.setContentsMargins(15, 15, 15, 15)
        param_layout.setSpacing(20)
        
        # Spinboxes with better styling
        self.top_spinbox = self.create_styled_spinbox(1, 10, 3)
        self.max_depth_spinbox = self.create_styled_spinbox(1, 10, 3)
        
        param_layout.addWidget(QtWidgets.QLabel("Expand Top N Directories:"))
        param_layout.addWidget(self.top_spinbox)
        param_layout.addStretch()
        param_layout.addWidget(QtWidgets.QLabel("Maximum Scan Depth:"))
        param_layout.addWidget(self.max_depth_spinbox)
        param_layout.addStretch()
        layout.addWidget(param_card)
        
        # Scan Button with loading indicator
        button_layout = QtWidgets.QHBoxLayout()
        self.scan_button = QtWidgets.QPushButton("Start Scan")
        self.scan_button.setMinimumHeight(45)
        self.scan_button.setMinimumWidth(150)
        self.scan_button.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_BrowserReload))
        self.scan_button.clicked.connect(self.scan_folder)
        
        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setMaximumHeight(45)
        self.progress_bar.hide()
        
        button_layout.addWidget(self.scan_button)
        button_layout.addWidget(self.progress_bar)
        layout.addLayout(button_layout)
        
        # Results Tree
        self.tree_widget = CustomTreeWidget()
        self.tree_widget.setHeaderLabels(["Directory", "Size"])
        self.tree_widget.setAnimated(True)
        self.tree_widget.setIndentation(20)
        self.tree_widget.header().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.tree_widget.header().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        layout.addWidget(self.tree_widget)
        
        # Status bar
        self.statusBar().showMessage("Ready")
        
        # Internal cache
        self.size_cache = {}
        
    def create_card(self, title):
        group = QtWidgets.QGroupBox(title)
        group.setStyleSheet("""
            QGroupBox {
                border: 1px solid #ccc;
                border-radius: 8px;
                margin-top: 1ex;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
            }
        """)
        return group
    
    def create_styled_spinbox(self, min_val, max_val, default):
        spinbox = QtWidgets.QSpinBox()
        spinbox.setMinimum(min_val)
        spinbox.setMaximum(max_val)
        spinbox.setValue(default)
        spinbox.setMinimumWidth(80)
        spinbox.setMinimumHeight(35)
        return spinbox

    def compute_dir_size(self, path):
        if path in self.size_cache:
            return self.size_cache[path]
        total = 0
        try:
            for entry in os.scandir(path):
                if entry.is_file(follow_symlinks=False):
                    try:
                        total += entry.stat().st_size
                    except Exception:
                        pass
                elif entry.is_dir(follow_symlinks=False):
                    total += self.compute_dir_size(entry.path)
        except Exception as e:
            self.statusBar().showMessage(f"Error scanning {path}: {str(e)}")
        self.size_cache[path] = total
        return total

    def human_readable_size(self, num, suffix='B'):
        for unit in ['','K','M','G','T','P']:
            if abs(num) < 1024.0:
                return f"{num:3.1f} {unit}{suffix}"
            num /= 1024.0
        return f"{num:.1f} Y{suffix}"

    def populate_tree(self, parent_item, path, current_depth, max_depth, top_n):
        folder_size = self.compute_dir_size(path)
        item = QtWidgets.QTreeWidgetItem([
            os.path.basename(path) or path,
            self.human_readable_size(folder_size)
        ])
        
        # Add tooltip with full path
        item.setToolTip(0, path)
        
        # Set icon for directory
        item.setIcon(0, self.style().standardIcon(QtWidgets.QStyle.SP_DirIcon))
        
        item.setData(0, QtCore.Qt.UserRole, path)
        if parent_item is None:
            self.tree_widget.addTopLevelItem(item)
        else:
            parent_item.addChild(item)
            
        if current_depth >= max_depth:
            return
            
        subdirs = []
        try:
            for entry in os.scandir(path):
                if entry.is_dir(follow_symlinks=False):
                    size = self.compute_dir_size(entry.path)
                    subdirs.append((entry.path, size))
        except Exception as e:
            self.statusBar().showMessage(f"Error scanning subdirectories: {str(e)}")
            
        subdirs.sort(key=lambda x: x[1], reverse=True)
        for subdir_path, _ in subdirs[:top_n]:
            self.populate_tree(item, subdir_path, current_depth + 1, max_depth, top_n)

    def select_folder(self):
        folder = QtWidgets.QFileDialog.getExistingDirectory(
            self,
            "Select Directory to Analyze",
            os.getcwd(),
            QtWidgets.QFileDialog.ShowDirsOnly
        )
        if folder:
            self.folder_line_edit.setText(folder)
            self.statusBar().showMessage(f"Selected folder: {folder}")

    def scan_folder(self):
        self.progress_bar.show()
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        self.scan_button.setEnabled(False)
        self.statusBar().showMessage("Scanning...")
        
        # Clear previous results
        self.tree_widget.clear()
        self.size_cache.clear()
        
        # Get parameters
        folder = self.folder_line_edit.text() or os.getcwd()
        top_n = self.top_spinbox.value()
        max_depth = self.max_depth_spinbox.value()
        
        # Use QTimer to prevent UI freeze
        QtCore.QTimer.singleShot(100, lambda: self._perform_scan(folder, top_n, max_depth))

    def _perform_scan(self, folder, top_n, max_depth):
        try:
            self.populate_tree(None, folder, 0, max_depth, top_n)
            self.tree_widget.expandAll()
            self.statusBar().showMessage("Scan completed successfully")
        except Exception as e:
            self.statusBar().showMessage(f"Error during scan: {str(e)}")
        finally:
            self.progress_bar.hide()
            self.scan_button.setEnabled(True)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    
    # Enable High DPI scaling
    app.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)
    
    # Apply Material Design theme with custom colors
    apply_stylesheet(app, theme='light_blue.xml')
    
    # Custom style adjustments
    app.setStyle('Fusion')
    
    window = DirSizeWidget()
    window.show()
    sys.exit(app.exec_())

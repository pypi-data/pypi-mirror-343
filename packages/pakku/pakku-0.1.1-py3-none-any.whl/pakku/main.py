import sys
import subprocess
import threading
import importlib.metadata
import requests
import json
import os
import psutil
import site

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QLabel, QHeaderView, QTabWidget, QProgressBar,
    QFrame, QSplitter, QTextBrowser, QComboBox, QMenu, QFileDialog,
    QCheckBox
)
from PyQt5.QtGui import QColor, QFont, QIcon, QPalette, QCursor
from PyQt5.QtCore import Qt, pyqtSignal, QObject, QSize, QTimer, QPoint


class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(str, str)
    success = pyqtSignal(str, str)
    search_results = pyqtSignal(list)
    progress = pyqtSignal(int)
    log_update = pyqtSignal(str)


class PackageManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Python Package Manager")
        self.setGeometry(100, 100, 900, 600)
        self.setup_styles()

        # Check for required modules
        self.check_required_modules()

        self.signals = WorkerSignals()
        self.signals.success.connect(self.show_success_message)
        self.signals.error.connect(self.show_error_message)
        self.signals.finished.connect(self.update_table)
        self.signals.search_results.connect(self.display_search_results)
        self.signals.log_update.connect(self.update_log)

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # Create tab widget
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #3d3d3d;
                border-radius: 5px;
                background-color: #2d2d2d;
            }
            QTabBar::tab {
                background-color: #1e1e1e;
                color: #cccccc;
                padding: 8px 15px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #2d2d2d;
                color: white;
                border-bottom: 2px solid #007BFF;
            }
        """)

        # Create tabs
        self.tutorial_tab = QWidget()
        self.installed_tab = QWidget()
        self.search_tab = QWidget()
        self.advanced_tab = QWidget()
        self.logs_tab = QWidget()

        self.setup_tutorial_tab()
        self.setup_installed_tab()
        self.setup_search_tab()
        self.setup_advanced_tab()
        self.setup_logs_tab()

        # Check if tutorial has been completed
        if not self.has_completed_tutorial():
            self.tabs.addTab(self.tutorial_tab, "Tutorial")

        self.tabs.addTab(self.installed_tab, "Installed Packages")
        self.tabs.addTab(self.search_tab, "Search Packages")
        self.tabs.addTab(self.advanced_tab, "Advanced Options")
        self.tabs.addTab(self.logs_tab, "Logs")

        self.main_layout.addWidget(self.tabs)

        # Status bar
        self.status_bar = QLabel("Ready")
        self.status_bar.setStyleSheet("color: #aaaaaa; padding: 5px;")
        self.main_layout.addWidget(self.status_bar)

        self.all_packages = []
        self.load_packages()
        
        # Load activation file if it exists
        self.load_activation_file()

    def setup_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: white;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                background-color: #2d2d2d;
                color: white;
            }
            QPushButton {
                padding: 8px 15px;
                border: none;
                border-radius: 4px;
                background-color: #2d2d2d;
                color: white;
            }
            QPushButton:hover {
                background-color: #3d3d3d;
            }
            QTableWidget {
                background-color: #2d2d2d;
                alternate-background-color: #333333;
                gridline-color: #3d3d3d;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
            }
            QHeaderView::section {
                background-color: #252525;
                padding: 5px;
                border: 1px solid #3d3d3d;
                color: #cccccc;
            }
            QTableWidget::item {
                padding: 5px;
            }
        """)

    def setup_installed_tab(self):
        layout = QVBoxLayout(self.installed_tab)

        # Search bar for installed packages
        search_frame = QFrame()
        search_frame.setStyleSheet("background-color: #252525; border-radius: 5px; padding: 10px;")
        search_layout = QHBoxLayout(search_frame)

        search_label = QLabel("Filter:")
        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("Filter installed packages...")
        self.filter_input.textChanged.connect(self.filter_packages)

        refresh_btn = QPushButton("Refresh")
        refresh_btn.setStyleSheet("background-color: #0066cc; color: white;")
        refresh_btn.clicked.connect(self.load_packages)

        search_layout.addWidget(search_label)
        search_layout.addWidget(self.filter_input, 1)
        search_layout.addWidget(refresh_btn)

        layout.addWidget(search_frame)

        # Install bar
        install_frame = QFrame()
        install_frame.setStyleSheet("background-color: #252525; border-radius: 5px; padding: 10px;")
        install_layout = QHBoxLayout(install_frame)

        install_label = QLabel("Install:")
        self.install_input = QLineEdit()
        self.install_input.setPlaceholderText("Enter package name to install...")

        self.install_btn = QPushButton("Install")
        self.install_btn.setStyleSheet("background-color: #007BFF; color: white;")
        self.install_btn.clicked.connect(self.install_package)

        install_layout.addWidget(install_label)
        install_layout.addWidget(self.install_input, 1)
        install_layout.addWidget(self.install_btn)

        layout.addWidget(install_frame)

        # Package table
        self.table = QTableWidget()
        self.table.setColumnCount(2)  # Changed to 2 columns since we removed the Actions column
        self.table.setHorizontalHeaderLabels(["Package Name", "Version"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.setAlternatingRowColors(True)
        
        # Set up context menu policy for the table
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.show_context_menu)
        
        # Enable selection
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        
        # Store the currently highlighted row
        self.highlighted_row = -1

        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #2d2d2d;
                alternate-background-color: #333333;
                gridline-color: #3d3d3d;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
            }
            QHeaderView::section {
                background-color: #252525;
                padding: 5px;
                border: 1px solid #3d3d3d;
                color: #cccccc;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #007BFF;
                color: white;
            }
        """)

        layout.addWidget(self.table)

        # Progress bar (hidden by default)
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)  # Indeterminate
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                background-color: #2d2d2d;
                height: 10px;
            }
            QProgressBar::chunk {
                background-color: #007BFF;
                border-radius: 4px;
            }
        """)
        self.progress_bar.hide()

        layout.addWidget(self.progress_bar)

    def setup_search_tab(self):
        layout = QVBoxLayout(self.search_tab)

        # Search frame
        search_frame = QFrame()
        search_frame.setStyleSheet("""
            QFrame {
                background-color: #252525;
                border-radius: 5px;
                padding: 10px;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                background-color: #2d2d2d;
                color: white;
                font-size: 14px;
            }
            QPushButton {
                padding: 8px 15px;
                border: none;
                border-radius: 4px;
                background-color: #007BFF;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        search_layout = QHBoxLayout(search_frame)

        self.pypi_search_input = QLineEdit()
        self.pypi_search_input.setPlaceholderText("Search PyPI packages...")
        self.pypi_search_input.returnPressed.connect(self.search_pypi)
        self.pypi_search_input.setMinimumWidth(300)

        self.search_btn = QPushButton("Search")
        self.search_btn.clicked.connect(self.search_pypi)

        search_layout.addWidget(self.pypi_search_input, 1)
        search_layout.addWidget(self.search_btn)

        layout.addWidget(search_frame)

        # Search results
        self.search_results_table = QTableWidget()
        self.search_results_table.setColumnCount(3)  # Changed to 3 columns since we removed the Actions column
        self.search_results_table.setHorizontalHeaderLabels(["Package Name", "Version", "Description"])
        self.search_results_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.search_results_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.search_results_table.setAlternatingRowColors(True)
        
        # Set up context menu policy for the table
        self.search_results_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.search_results_table.customContextMenuRequested.connect(self.show_search_context_menu)
        
        # Enable selection
        self.search_results_table.setSelectionMode(QTableWidget.SingleSelection)
        self.search_results_table.setSelectionBehavior(QTableWidget.SelectRows)
        
        # Store the currently highlighted row
        self.search_highlighted_row = -1
        
        self.search_results_table.setStyleSheet("""
            QTableWidget {
                background-color: #2d2d2d;
                alternate-background-color: #333333;
                gridline-color: #3d3d3d;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
            }
            QHeaderView::section {
                background-color: #252525;
                padding: 8px;
                border: 1px solid #3d3d3d;
                color: #cccccc;
                font-weight: bold;
            }
            QTableWidget::item:selected {
                background-color: #007BFF;
                color: white;
            }
        """)

        layout.addWidget(self.search_results_table)

        # Package details
        details_frame = QFrame()
        details_frame.setStyleSheet("""
            QFrame {
                background-color: #252525;
                border-radius: 5px;
                padding: 10px;
            }
            QLabel {
                color: #cccccc;
                font-weight: bold;
                font-size: 14px;
            }
            QTextBrowser {
                background-color: #2d2d2d;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                padding: 8px;
                color: #ffffff;
            }
        """)
        details_layout = QVBoxLayout(details_frame)

        details_label = QLabel("Package Details")
        self.package_details = QTextBrowser()
        self.package_details.setMaximumHeight(150)

        details_layout.addWidget(details_label)
        details_layout.addWidget(self.package_details)

        layout.addWidget(details_frame)

        # Search progress bar
        self.search_progress_bar = QProgressBar()
        self.search_progress_bar.setRange(0, 0)
        self.search_progress_bar.setTextVisible(False)
        self.search_progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                background-color: #2d2d2d;
                height: 10px;
            }
            QProgressBar::chunk {
                background-color: #007BFF;
                border-radius: 4px;
            }
        """)
        self.search_progress_bar.hide()

        layout.addWidget(self.search_progress_bar)

    def setup_advanced_tab(self):
        """Set up the advanced options tab."""
        layout = QVBoxLayout(self.advanced_tab)
        
        # Virtual Environment section
        venv_frame = QFrame()
        venv_frame.setStyleSheet("""
            QFrame {
                background-color: #252525;
                border-radius: 5px;
                padding: 10px;
            }
            QLabel {
                color: #cccccc;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton {
                padding: 8px 15px;
                border: none;
                border-radius: 4px;
                background-color: #007BFF;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                background-color: #2d2d2d;
                color: white;
            }
        """)
        venv_layout = QVBoxLayout(venv_frame)
        
        venv_label = QLabel("Virtual Environment Management")
        venv_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #cccccc;")
        
        # Environment activation file selection
        activate_layout = QHBoxLayout()
        activate_label = QLabel("Activation File:")
        self.activate_path_input = QLineEdit()
        self.activate_path_input.setPlaceholderText("Path to environment activation file")
        self.activate_path_input.setReadOnly(True)
        select_activate_btn = QPushButton("Select Activation File")
        select_activate_btn.clicked.connect(self.select_activation_file)
        
        activate_layout.addWidget(activate_label)
        activate_layout.addWidget(self.activate_path_input)
        activate_layout.addWidget(select_activate_btn)
        
        # Create virtual environment
        create_venv_layout = QHBoxLayout()
        venv_name_label = QLabel("Environment Name:")
        self.venv_name_input = QLineEdit()
        self.venv_name_input.setPlaceholderText("Enter environment name")
        create_venv_btn = QPushButton("Create Virtual Environment")
        create_venv_btn.clicked.connect(self.create_virtual_environment)
        
        create_venv_layout.addWidget(venv_name_label)
        create_venv_layout.addWidget(self.venv_name_input)
        create_venv_layout.addWidget(create_venv_btn)
        
        # Export virtual environment
        export_venv_btn = QPushButton("Export Current Environment")
        export_venv_btn.clicked.connect(self.export_virtual_environment)
        
        venv_layout.addWidget(venv_label)
        venv_layout.addLayout(activate_layout)
        venv_layout.addLayout(create_venv_layout)
        venv_layout.addWidget(export_venv_btn)
        
        # Requirements.txt section
        requirements_frame = QFrame()
        requirements_frame.setStyleSheet("""
            QFrame {
                background-color: #252525;
                border-radius: 5px;
                padding: 10px;
            }
            QLabel {
                color: #cccccc;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton {
                padding: 8px 15px;
                border: none;
                border-radius: 4px;
                background-color: #007BFF;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        requirements_layout = QVBoxLayout(requirements_frame)
        
        requirements_label = QLabel("Requirements.txt Management")
        requirements_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #cccccc;")
        
        requirements_buttons = QHBoxLayout()
        create_btn = QPushButton("Create requirements.txt")
        import_btn = QPushButton("Import from requirements.txt")
        create_btn.clicked.connect(self.create_requirements_file)
        import_btn.clicked.connect(self.import_requirements_file)
        
        requirements_buttons.addWidget(create_btn)
        requirements_buttons.addWidget(import_btn)
        
        requirements_layout.addWidget(requirements_label)
        requirements_layout.addLayout(requirements_buttons)
        
        # System Information section
        sysinfo_frame = QFrame()
        sysinfo_frame.setStyleSheet("""
            QFrame {
                background-color: #252525;
                border-radius: 5px;
                padding: 10px;
            }
            QLabel {
                color: #cccccc;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton {
                padding: 8px 15px;
                border: none;
                border-radius: 4px;
                background-color: #007BFF;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        sysinfo_layout = QVBoxLayout(sysinfo_frame)
        
        sysinfo_label = QLabel("System Information")
        sysinfo_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #cccccc;")
        
        self.sysinfo_text = QTextBrowser()
        self.sysinfo_text.setStyleSheet("""
            QTextBrowser {
                background-color: #2d2d2d;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                padding: 8px;
                color: #ffffff;
            }
        """)
        
        refresh_sysinfo_btn = QPushButton("Refresh System Info")
        refresh_sysinfo_btn.clicked.connect(self.update_system_info)
        
        sysinfo_layout.addWidget(sysinfo_label)
        sysinfo_layout.addWidget(self.sysinfo_text)
        sysinfo_layout.addWidget(refresh_sysinfo_btn)
        
        # Add all sections to main layout
        layout.addWidget(venv_frame)
        layout.addWidget(requirements_frame)
        layout.addWidget(sysinfo_frame)
        layout.addStretch()
        
        # Initialize system info
        self.update_system_info()

    def select_activation_file(self):
        """Select a virtual environment activation file and restart the application."""
        activate_file = QFileDialog.getOpenFileName(
            self,
            "Select Environment Activation File",
            os.path.expanduser("~"),
            "Activation Files (activate*);;All Files (*.*)"
        )[0]
        
        if activate_file:
            if os.path.exists(activate_file):
                # Save the activation file path to a config file
                try:
                    config_dir = os.path.join(os.path.expanduser("~"), ".python_package_manager")
                    os.makedirs(config_dir, exist_ok=True)
                    config_file = os.path.join(config_dir, "config.json")
                    
                    config = {}
                    if os.path.exists(config_file):
                        with open(config_file, 'r') as f:
                            config = json.load(f)
                    
                    config['activation_file'] = activate_file
                    
                    with open(config_file, 'w') as f:
                        json.dump(config, f)
                    
                    # Update the input field
                    self.activate_path_input.setText(activate_file)
                    
                    # Show restart message
                    reply = QMessageBox.question(
                        self,
                        "Restart Required",
                        "The application needs to restart to use the selected environment. Restart now?",
                        QMessageBox.Yes | QMessageBox.No,
                        QMessageBox.Yes
                    )
                    
                    if reply == QMessageBox.Yes:
                        # Restart the application
                        self.restart_application(activate_file)
                except Exception as e:
                    self.show_error_message("Error", f"Failed to save activation file path: {str(e)}")
            else:
                self.show_error_message("Error", "Selected file does not exist")

    def restart_application(self, activate_file):
        """Restart the application with the selected virtual environment."""
        try:
            # Get the current script path
            script_path = os.path.abspath(sys.argv[0])
            
            # Create a restart script
            restart_script = os.path.join(os.path.expanduser("~"), ".python_package_manager", "restart.sh")
            
            # Determine the shell to use based on the activation file
            if activate_file.endswith(".bat") or activate_file.endswith(".cmd"):
                # Windows batch file
                with open(restart_script, 'w') as f:
                    f.write(f'@echo off\n')
                    f.write(f'call "{activate_file}"\n')
                    f.write(f'python -m pip install requests psutil PyQt5\n')
                    f.write(f'python "{script_path}"\n')
                os.chmod(restart_script, 0o755)
                subprocess.Popen([restart_script], shell=True)
            else:
                # Unix shell script
                with open(restart_script, 'w') as f:
                    f.write(f'#!/bin/bash\n')
                    f.write(f'source "{activate_file}"\n')
                    f.write(f'python -m pip install requests psutil PyQt5\n')
                    f.write(f'python "{script_path}"\n')
                os.chmod(restart_script, 0o755)
                subprocess.Popen(['bash', restart_script])
            
            # Close the current application
            self.close()
        except Exception as e:
            self.show_error_message("Error", f"Failed to restart application: {str(e)}")

    def load_activation_file(self):
        """Load the activation file path from config if it exists."""
        try:
            config_dir = os.path.join(os.path.expanduser("~"), ".python_package_manager")
            config_file = os.path.join(config_dir, "config.json")
            
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    if 'activation_file' in config and os.path.exists(config['activation_file']):
                        self.activate_path_input.setText(config['activation_file'])
        except Exception:
            pass

    def get_current_python(self):
        """Get the path to the currently active Python executable."""
        return sys.executable

    def run_pip_install(self, *args):
        """Install package(s) using pip."""
        try:
            python_exe = self.get_current_python()
            # If args is a tuple with two elements, it's a requirements file installation
            if len(args) == 2 and args[0] == "-r":
                process = subprocess.Popen(
                    [python_exe, "-m", "pip", "install", "-r", args[1]],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    universal_newlines=True
                )
                self.signals.log_update.emit(f"Installing packages from {args[1]}...")
            else:
                # Single package installation
                package_name = args[0]
                process = subprocess.Popen(
                    [python_exe, "-m", "pip", "install", package_name],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    universal_newlines=True
                )
                self.signals.log_update.emit(f"Installing {package_name}...")

            # Read output in real-time
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    self.signals.log_update.emit(output.strip())

            if process.returncode == 0:
                if len(args) == 2:
                    self.signals.success.emit("Success", "Successfully installed packages from requirements.txt\n\nCheck the Logs tab for detailed installation information.")
                else:
                    self.signals.success.emit("Success", f"Successfully installed {args[0]}\n\nCheck the Logs tab for detailed installation information.")
            else:
                self.signals.error.emit("Error", "Installation failed")
        except Exception as e:
            self.signals.error.emit("Error", f"Failed to install package(s): {e}")
        finally:
            self.progress_bar.hide()
            self.status_bar.setText("Ready")
            self.load_packages()  # Refresh the package list

    def run_pip_uninstall(self, package_name):
        """Uninstall the package using pip."""
        try:
            python_exe = self.get_current_python()
            process = subprocess.Popen(
                [python_exe, "-m", "pip", "uninstall", "-y", package_name],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )
            
            self.signals.log_update.emit(f"Uninstalling {package_name}...")
            
            # Read output in real-time
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    self.signals.log_update.emit(output.strip())

            if process.returncode == 0:
                self.signals.success.emit("Success", f"Successfully removed {package_name}\n\nCheck the Logs tab for detailed uninstallation information.")
            else:
                self.signals.error.emit("Error", "Uninstallation failed")
        except subprocess.CalledProcessError as e:
            self.signals.error.emit("Error", f"Failed to remove {package_name}: {e}")
        finally:
            self.progress_bar.hide()
            self.status_bar.setText("Ready")
            self.load_packages()  # Refresh the package list

    def run_pip_update(self, package_name):
        """Update the package using pip."""
        try:
            python_exe = self.get_current_python()
            process = subprocess.Popen(
                [python_exe, "-m", "pip", "install", "--upgrade", package_name],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )
            
            self.signals.log_update.emit(f"Updating {package_name}...")
            
            # Read output in real-time
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    self.signals.log_update.emit(output.strip())

            if process.returncode == 0:
                self.signals.success.emit("Success", f"Successfully updated {package_name}\n\nCheck the Logs tab for detailed update information.")
            else:
                self.signals.error.emit("Error", "Update failed")
        except subprocess.CalledProcessError as e:
            self.signals.error.emit("Error", f"Failed to update {package_name}: {e}")
        finally:
            self.progress_bar.hide()
            self.status_bar.setText("Ready")
            self.load_packages()  # Refresh the package list

    def get_installed_packages(self):
        """Fetch list of installed packages."""
        try:
            python_exe = self.get_current_python()
            if not python_exe or not os.path.exists(python_exe):
                self.signals.error.emit("Error", "Invalid Python executable path")
                return
                
            installed_packages = subprocess.check_output([python_exe, "-m", "pip", "list", "--format=json"]).decode()
            packages_json = json.loads(installed_packages)
            self.all_packages = [[pkg["name"], pkg["version"]] for pkg in packages_json]
            self.signals.finished.emit()
        except subprocess.CalledProcessError as e:
            self.signals.error.emit("Error", f"Failed to load installed packages: {e}")
        except Exception as e:
            self.signals.error.emit("Error", f"An error occurred: {str(e)}")
        finally:
            self.progress_bar.hide()
            self.status_bar.setText("Ready")

    def setup_logs_tab(self):
        """Set up the logs tab."""
        layout = QVBoxLayout(self.logs_tab)
        
        # Log display
        self.log_text = QTextBrowser()
        self.log_text.setStyleSheet("""
            QTextBrowser {
                background-color: #1e1e1e;
                color: #00ff00;
                font-family: 'Courier New', monospace;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                padding: 8px;
            }
        """)
        
        # Controls frame
        controls_frame = QFrame()
        controls_frame.setStyleSheet("""
            QFrame {
                background-color: #252525;
                border-radius: 5px;
                padding: 10px;
            }
            QLabel {
                color: #cccccc;
            }
            QPushButton {
                padding: 8px 15px;
                border: none;
                border-radius: 4px;
                background-color: #007BFF;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QCheckBox {
                color: #cccccc;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #3d3d3d;
                background-color: #2d2d2d;
                border-radius: 3px;
            }
            QCheckBox::indicator:checked {
                border: 2px solid #007BFF;
                background-color: #007BFF;
                border-radius: 3px;
            }
        """)
        controls_layout = QHBoxLayout(controls_frame)
        
        # Persistent logs toggle
        self.persistent_logs = QCheckBox("Persistent Logs")
        self.persistent_logs.setChecked(False)
        self.persistent_logs.stateChanged.connect(self.toggle_persistent_logs)
        
        # Clear logs button
        clear_btn = QPushButton("Clear Logs")
        clear_btn.clicked.connect(self.clear_logs)
        
        controls_layout.addWidget(self.persistent_logs)
        controls_layout.addStretch()
        controls_layout.addWidget(clear_btn)
        
        layout.addWidget(self.log_text)
        layout.addWidget(controls_frame)
        
        # Load previous logs if they exist
        self.load_previous_logs()

    def toggle_persistent_logs(self, state):
        """Toggle persistent logs on/off."""
        if state == Qt.Checked:
            self.show_success_message("Persistent Logs", "Logs will now be saved between sessions")
        else:
            self.show_success_message("Persistent Logs", "Logs will no longer be saved between sessions")

    def load_previous_logs(self):
        """Load previous logs from file if they exist."""
        try:
            log_file = os.path.join(os.path.expanduser("~"), ".python_package_manager", "logs.txt")
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    logs = f.read()
                    self.log_text.setPlainText(logs)
                    # Scroll to the bottom
                    self.log_text.verticalScrollBar().setValue(
                        self.log_text.verticalScrollBar().maximum()
                    )
        except Exception as e:
            self.show_error_message("Error", f"Failed to load previous logs: {str(e)}")

    def save_logs(self):
        """Save current logs to file."""
        if not self.persistent_logs.isChecked():
            return
            
        try:
            # Create directory if it doesn't exist
            log_dir = os.path.join(os.path.expanduser("~"), ".python_package_manager")
            os.makedirs(log_dir, exist_ok=True)
            
            # Save logs to file
            log_file = os.path.join(log_dir, "logs.txt")
            with open(log_file, 'w') as f:
                f.write(self.log_text.toPlainText())
        except Exception as e:
            self.show_error_message("Error", f"Failed to save logs: {str(e)}")

    def update_log(self, message):
        """Update the log display with a new message."""
        self.log_text.append(message)
        # Scroll to the bottom
        self.log_text.verticalScrollBar().setValue(
            self.log_text.verticalScrollBar().maximum()
        )
        # Save logs if persistent logging is enabled
        self.save_logs()

    def clear_logs(self):
        """Clear the log display and saved logs."""
        self.log_text.clear()
        if self.persistent_logs.isChecked():
            try:
                log_file = os.path.join(os.path.expanduser("~"), ".python_package_manager", "logs.txt")
                if os.path.exists(log_file):
                    os.remove(log_file)
            except Exception as e:
                self.show_error_message("Error", f"Failed to clear saved logs: {str(e)}")

    def closeEvent(self, event):
        """Handle window close event."""
        # Save logs before closing if persistent logging is enabled
        self.save_logs()
        event.accept()

    def create_requirements_file(self):
        """Create a requirements.txt file with all installed packages."""
        try:
            # Get list of installed packages
            installed_packages = subprocess.check_output([sys.executable, "-m", "pip", "freeze"]).decode()
            
            # Write to requirements.txt
            with open("requirements.txt", "w") as f:
                f.write(installed_packages)
            
            self.show_success_message("Success", "requirements.txt file has been created successfully!")
        except Exception as e:
            self.show_error_message("Error", f"Failed to create requirements.txt: {str(e)}")

    def import_requirements_file(self):
        """Import packages from requirements.txt file."""
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Select requirements.txt file",
            "",
            "Text Files (*.txt);;All Files (*)"
        )
        
        if file_name:
            try:
                self.status_bar.setText("Installing packages from requirements.txt...")
                self.progress_bar.show()
                threading.Thread(target=self.run_pip_install, args=("-r", file_name), daemon=True).start()
            except Exception as e:
                self.show_error_message("Error", f"Failed to import requirements: {str(e)}")

    def create_virtual_environment(self):
        """Create a new virtual environment."""
        env_name = self.venv_name_input.text().strip()
        if not env_name:
            self.show_error_message("Error", "Please enter an environment name")
            return
            
        try:
            self.status_bar.setText(f"Creating virtual environment '{env_name}'...")
            self.progress_bar.show()
            
            # Create virtual environment
            subprocess.check_call([sys.executable, "-m", "venv", env_name])
            
            self.show_success_message("Success", f"Virtual environment '{env_name}' created successfully!")
            self.venv_name_input.clear()
        except Exception as e:
            self.show_error_message("Error", f"Failed to create virtual environment: {str(e)}")
        finally:
            self.progress_bar.hide()
            self.status_bar.setText("Ready")

    def export_virtual_environment(self):
        """Export current virtual environment to requirements.txt."""
        try:
            # Get the active virtual environment path
            venv_path = os.environ.get('VIRTUAL_ENV')
            if not venv_path:
                self.show_error_message("Error", "No active virtual environment found")
                return
                
            # Create requirements.txt in the virtual environment directory
            output_file = os.path.join(venv_path, "requirements.txt")
            installed_packages = subprocess.check_output([sys.executable, "-m", "pip", "freeze"]).decode()
            
            with open(output_file, "w") as f:
                f.write(installed_packages)
            
            self.show_success_message("Success", f"Virtual environment exported to {output_file}")
        except Exception as e:
            self.show_error_message("Error", f"Failed to export virtual environment: {str(e)}")

    def update_system_info(self):
        """Update system information display."""
        try:
            # Python version
            python_version = sys.version.split()[0]
            
            # Disk space
            disk = psutil.disk_usage('/')
            disk_space = f"Total: {self.format_size(disk.total)}\nUsed: {self.format_size(disk.used)}\nFree: {self.format_size(disk.free)}"
            
            # Package installation paths
            site_packages = site.getsitepackages()
            user_site = site.getusersitepackages()
            
            # Format the information
            info_text = f"""
            <h3>Python Information</h3>
            <p><b>Python Version:</b> {python_version}</p>
            <p><b>Virtual Environment:</b> {os.environ.get('VIRTUAL_ENV', 'Not active')}</p>
            
            <h3>Disk Space</h3>
            <p>{disk_space}</p>
            
            <h3>Package Installation Paths</h3>
            <p><b>Site Packages:</b></p>
            <ul>
                {''.join(f'<li>{path}</li>' for path in site_packages)}
            </ul>
            <p><b>User Site Packages:</b></p>
            <p>{user_site}</p>
            """
            
            self.sysinfo_text.setHtml(info_text)
        except Exception as e:
            self.sysinfo_text.setPlainText(f"Error getting system information: {str(e)}")

    def format_size(self, size):
        """Format size in bytes to human readable format."""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} PB"

    def load_packages(self):
        """Load installed packages into the table."""
        self.all_packages = []
        self.table.setRowCount(0)
        self.status_bar.setText("Loading packages...")
        self.progress_bar.show()
        self.filter_input.clear()  # Clear any existing filter
        threading.Thread(target=self.get_installed_packages, daemon=True).start()

    def filter_packages(self):
        """Filter the packages based on user input."""
        query = self.filter_input.text().lower()
        self.table.setRowCount(0)
        filtered_packages = [pkg for pkg in self.all_packages if query in pkg[0].lower()]
        for package in filtered_packages:
            self.add_package_to_table(package[0], package[1])

    def add_package_to_table(self, name, version):
        """Add a package to the installed packages table with action buttons."""
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        
        # Create items and store package name as data
        name_item = QTableWidgetItem(name)
        name_item.setData(Qt.UserRole, name)  # Store package name for context menu
        version_item = QTableWidgetItem(version)
        
        self.table.setItem(row_position, 0, name_item)
        self.table.setItem(row_position, 1, version_item)

    def show_context_menu(self, position):
        """Show context menu for package actions."""
        # Get the selected row
        selected_items = self.table.selectedItems()
        if not selected_items:
            return
            
        # Get the package name from the first column of selected row
        package_name = self.table.item(selected_items[0].row(), 0).data(Qt.UserRole)
        
        # Create context menu
        menu = QMenu(self.table)
        update_action = menu.addAction("Update")
        remove_action = menu.addAction("Remove")
        
        # Style the menu
        menu.setStyleSheet("""
            QMenu {
                background-color: #2d2d2d;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                padding: 5px;
            }
            QMenu::item {
                padding: 8px 20px;
                color: white;
                border-radius: 4px;
            }
            QMenu::item:selected {
                background-color: #3d3d3d;
            }
        """)
        
        # Show menu at cursor position
        action = menu.exec_(self.table.mapToGlobal(position))
        
        # Handle menu actions
        if action == update_action:
            self.update_package(package_name)
        elif action == remove_action:
            self.remove_package(package_name)

    def update_package(self, package_name):
        """Update a package to the latest version."""
        self.status_bar.setText(f"Updating {package_name}...")
        self.progress_bar.show()
        threading.Thread(target=self.run_pip_update, args=(package_name,)).start()

    def remove_package(self, package_name):
        """Remove a package."""
        reply = QMessageBox.question(
            self, 
            "Confirm Removal", 
            f"Are you sure you want to uninstall {package_name}?",
            QMessageBox.Yes | QMessageBox.No, 
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.status_bar.setText(f"Removing {package_name}...")
            self.progress_bar.show()
            threading.Thread(target=self.run_pip_uninstall, args=(package_name,)).start()

    def search_pypi(self):
        """Search for packages on PyPI."""
        search_query = self.pypi_search_input.text().strip()
        if not search_query:
            self.show_error_message("Input Error", "Please enter a search query.")
            return
        self.status_bar.setText(f"Searching for {search_query}...")
        self.search_progress_bar.show()
        self.search_results_table.setRowCount(0)
        threading.Thread(target=self.run_pypi_search, args=(search_query,), daemon=True).start()

    def run_pypi_search(self, query):
        """Search PyPI for packages."""
        try:
            # Use the PyPI JSON API to search for packages
            url = f"https://pypi.org/search/?q={query}&format=json"
            headers = {
                'Accept': 'application/json',
                'User-Agent': 'Python Package Manager'
            }
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    results = []
                    
                    # Process search results from the JSON API
                    for item in data.get('results', []):
                        name = item.get('name', 'Unknown')
                        version = item.get('version', 'N/A')
                        summary = item.get('description', 'No description available')
                        if summary is None:
                            summary = 'No description available'
                        results.append((name, version, summary))
                    
                    if not results:
                        self.signals.error.emit("No Results", f"No packages found matching '{query}'")
                    else:
                        self.signals.search_results.emit(results)
                except json.JSONDecodeError:
                    # If JSON parsing fails, try alternative search method
                    self.alternative_search(query)
            else:
                self.signals.error.emit("Search Error", f"Failed to search for '{query}'. PyPI search API returned status code {response.status_code}")
        except Exception as e:
            self.signals.error.emit("Error", f"Search failed: {str(e)}")
        finally:
            self.search_progress_bar.hide()
            self.status_bar.setText("Ready")

    def alternative_search(self, query):
        """Alternative search method using direct package info."""
        try:
            # Try to get package info directly if the query might be a package name
            pkg_url = f"https://pypi.org/pypi/{query}/json"
            response = requests.get(pkg_url)
            
            if response.status_code == 200:
                pkg_data = response.json()
                name = pkg_data["info"]["name"]
                version = pkg_data["info"]["version"]
                summary = pkg_data["info"].get("summary", "No description available")
                if summary is None:
                    summary = 'No description available'
                results = [(name, version, summary)]
                self.signals.search_results.emit(results)
            else:
                self.signals.error.emit("No Results", f"No packages found matching '{query}'")
        except Exception:
            self.signals.error.emit("No Results", f"No packages found matching '{query}'")

    def display_search_results(self, results):
        """Display PyPI search results."""
        self.search_results_table.setRowCount(0)
        if not results:
            self.package_details.setText("No packages found matching your search criteria.")
            return
            
        for idx, result in enumerate(results):
            name, version, description = result
            
            row_position = self.search_results_table.rowCount()
            self.search_results_table.insertRow(row_position)
            
            # Create items and store package name as data
            name_item = QTableWidgetItem(name)
            name_item.setData(Qt.UserRole, name)  # Store package name for context menu
            version_item = QTableWidgetItem(version)
            description_item = QTableWidgetItem(description)
            
            self.search_results_table.setItem(row_position, 0, name_item)
            self.search_results_table.setItem(row_position, 1, version_item)
            self.search_results_table.setItem(row_position, 2, description_item)
        
        self.package_details.setText(f"Found {len(results)} packages matching your search criteria.")

    def show_search_context_menu(self, position):
        """Show context menu for search result actions."""
        # Get the selected row
        selected_items = self.search_results_table.selectedItems()
        if not selected_items:
            return
            
        # Get the package name from the first column of selected row
        package_name = self.search_results_table.item(selected_items[0].row(), 0).data(Qt.UserRole)
        
        # Create context menu
        menu = QMenu(self.search_results_table)
        install_action = menu.addAction("Install")
        
        # Style the menu
        menu.setStyleSheet("""
            QMenu {
                background-color: #2d2d2d;
                border: 1px solid #3d3d3d;
                    border-radius: 4px;
                padding: 5px;
                }
            QMenu::item {
                padding: 8px 20px;
                    color: white;
                    border-radius: 4px;
            }
            QMenu::item:selected {
                background-color: #3d3d3d;
                }
            """)
        
        # Show menu at cursor position
        action = menu.exec_(self.search_results_table.mapToGlobal(position))
        
        # Handle menu actions
        if action == install_action:
            self.install_from_search(package_name)

    def install_from_search(self, package_name):
        """Install a package from the search results."""
        reply = QMessageBox.question(
            self,
            "Confirm Installation",
            f"Are you sure you want to install {package_name}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.status_bar.setText(f"Installing {package_name}...")
            self.progress_bar.show()
            threading.Thread(target=self.run_pip_install, args=(package_name,), daemon=True).start()

    def show_package_info(self, package_name):
        """Show detailed information about a package."""
        self.status_bar.setText(f"Fetching info for {package_name}...")
        # Create a new thread for fetching package info
        thread = threading.Thread(target=self.fetch_package_info, args=(package_name,), daemon=True)
        thread.start()

    def fetch_package_info(self, package_name):
        """Fetch detailed package information from PyPI."""
        try:
            url = f"https://pypi.org/pypi/{package_name}/json"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                info = data["info"]
                
                # Format the package information
                details = f"""
                <h3>{info['name']} {info['version']}</h3>
                <p><strong>Author:</strong> {info.get('author', 'Unknown')}</p>
                <p><strong>License:</strong> {info.get('license', 'Unknown')}</p>
                <p><strong>Project URL:</strong> <a href="{info.get('project_url', '#')}">{info.get('project_url', 'N/A')}</a></p>
                <p><strong>Summary:</strong> {info.get('summary', 'No summary available')}</p>
                <p><strong>Requires Python:</strong> {info.get('requires_python', 'Not specified')}</p>
                """
                
                # Use QTimer to update UI in the main thread
                QTimer.singleShot(0, lambda: self.update_package_details(details))
            else:
                QTimer.singleShot(0, lambda: self.package_details.setText(f"Failed to fetch information for {package_name}"))
        except Exception as e:
            QTimer.singleShot(0, lambda: self.package_details.setText(f"Error fetching package info: {str(e)}"))
        finally:
            QTimer.singleShot(0, lambda: self.status_bar.setText("Ready"))

    def update_package_details(self, details):
        """Update package details in the UI (called from main thread)."""
        self.package_details.setHtml(details)

    def show_error_message(self, title, message):
        """Show error messages."""
        QMessageBox.critical(self, title, message)

    def show_success_message(self, title, message):
        """Show success messages."""
        QMessageBox.information(self, title, message)

    def update_table(self):
        """Update the table with all packages."""
        self.table.setRowCount(0)
        for package in self.all_packages:
            self.add_package_to_table(package[0], package[1])
        self.status_bar.setText(f"Loaded {len(self.all_packages)} packages")

    def has_completed_tutorial(self):
        """Check if the tutorial has been completed before."""
        try:
            config_dir = os.path.join(os.path.expanduser("~"), ".python_package_manager")
            os.makedirs(config_dir, exist_ok=True)
            config_file = os.path.join(config_dir, "config.json")
            
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    return config.get('tutorial_completed', False)
            return False
        except Exception:
            return False

    def save_tutorial_completion(self):
        """Save the tutorial completion state."""
        try:
            config_dir = os.path.join(os.path.expanduser("~"), ".python_package_manager")
            os.makedirs(config_dir, exist_ok=True)
            config_file = os.path.join(config_dir, "config.json")
            
            config = {}
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    config = json.load(f)
            
            config['tutorial_completed'] = True
            
            with open(config_file, 'w') as f:
                json.dump(config, f)
        except Exception as e:
            self.show_error_message("Error", f"Failed to save tutorial state: {str(e)}")

    def finish_tutorial(self):
        """Finish the tutorial and remove the tutorial tab."""
        self.tabs.removeTab(0)  # Remove tutorial tab
        self.save_tutorial_completion()  # Save the completion state
        self.show_success_message("Welcome", "You're all set to use the Python Package Manager!")

    def setup_tutorial_tab(self):
        """Set up the tutorial tab with step-by-step instructions."""
        layout = QVBoxLayout(self.tutorial_tab)
        
        # Tutorial content
        self.tutorial_content = QTextBrowser()
        self.tutorial_content.setStyleSheet("""
            QTextBrowser {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                padding: 20px;
                font-size: 14px;
                line-height: 1.6;
            }
        """)
        
        # Navigation buttons
        nav_frame = QFrame()
        nav_frame.setStyleSheet("""
            QFrame {
                background-color: #252525;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton {
                padding: 8px 15px;
                border: none;
                border-radius: 4px;
                background-color: #007BFF;
                color: white;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:disabled {
                background-color: #3d3d3d;
            }
        """)
        nav_layout = QHBoxLayout(nav_frame)
        
        self.prev_btn = QPushButton("Previous")
        self.next_btn = QPushButton("Next")
        self.finish_btn = QPushButton("Finish")
        
        self.prev_btn.clicked.connect(self.show_previous_tutorial)
        self.next_btn.clicked.connect(self.show_next_tutorial)
        self.finish_btn.clicked.connect(self.finish_tutorial)
        
        nav_layout.addWidget(self.prev_btn)
        nav_layout.addStretch()
        nav_layout.addWidget(self.next_btn)
        nav_layout.addWidget(self.finish_btn)
        
        layout.addWidget(self.tutorial_content)
        layout.addWidget(nav_frame)
        
        # Initialize tutorial
        self.tutorial_pages = [
            """
            <h2>Welcome to Python Package Manager!</h2>
            <p>This tool helps you manage Python packages easily. Let's go through the main features:</p>
            <ul>
                <li>View and manage installed packages</li>
                <li>Search and install new packages</li>
                <li>Manage Python environments</li>
                <li>Advanced package management options</li>
                <li>Real-time operation logs</li>
            </ul>
            <p>Click "Next" to learn about each feature in detail.</p>
            """,
            """
            <h2>Environment Management</h2>
            <p>This tool allows you to work with different Python environments:</p>
            <ul>
                <li>Select any Python environment using its activation file</li>
                <li>The application will automatically install required dependencies</li>
                <li>Switch between environments seamlessly</li>
                <li>All package operations will use the selected environment</li>
            </ul>
            <p>To switch environments:</p>
            <ol>
                <li>Go to the Advanced Options tab</li>
                <li>Click "Select Activation File"</li>
                <li>Choose your environment's activation script</li>
                <li>The application will restart in the new environment</li>
            </ol>
            """,
            """
            <h2>Installed Packages Tab</h2>
            <p>This tab shows all your installed Python packages:</p>
            <ul>
                <li>View package names and versions</li>
                <li>Filter packages using the search box</li>
                <li>Right-click on a package to:
                    <ul>
                        <li>Update to the latest version</li>
                        <li>Remove the package</li>
                    </ul>
                </li>
                <li>Install new packages using the input field at the top</li>
            </ul>
            """,
            """
            <h2>Search Packages Tab</h2>
            <p>Search and install packages from PyPI:</p>
            <ul>
                <li>Enter package name to search</li>
                <li>View package details including description</li>
                <li>Right-click on a package to:
                    <ul>
                        <li>Install the package</li>
                    </ul>
                </li>
                <li>See real-time installation progress</li>
            </ul>
            """,
            """
            <h2>Advanced Options Tab</h2>
            <p>Access advanced package management features:</p>
            <ul>
                <li>Environment Management:
                    <ul>
                        <li>Select and switch between Python environments</li>
                        <li>Create new virtual environments</li>
                        <li>Export environment settings</li>
                    </ul>
                </li>
                <li>Requirements Management:
                    <ul>
                        <li>Create requirements.txt files</li>
                        <li>Import packages from requirements.txt</li>
                    </ul>
                </li>
                <li>System Information:
                    <ul>
                        <li>Python version</li>
                        <li>Disk space</li>
                        <li>Package installation paths</li>
                    </ul>
                </li>
            </ul>
            """,
            """
            <h2>Logs Tab</h2>
            <p>Monitor package operations in real-time:</p>
            <ul>
                <li>View detailed installation logs</li>
                <li>See error messages and warnings</li>
                <li>Enable persistent logs to save between sessions</li>
                <li>Clear logs when needed</li>
            </ul>
            <p>Click "Finish" to start using the Package Manager!</p>
            """
        ]
        
        self.current_tutorial_page = 0
        self.update_tutorial_buttons()
        self.show_tutorial_page()

    def show_tutorial_page(self):
        """Show the current tutorial page."""
        self.tutorial_content.setHtml(self.tutorial_pages[self.current_tutorial_page])
        self.update_tutorial_buttons()

    def show_next_tutorial(self):
        """Show the next tutorial page."""
        if self.current_tutorial_page < len(self.tutorial_pages) - 1:
            self.current_tutorial_page += 1
            self.show_tutorial_page()

    def show_previous_tutorial(self):
        """Show the previous tutorial page."""
        if self.current_tutorial_page > 0:
            self.current_tutorial_page -= 1
            self.show_tutorial_page()

    def update_tutorial_buttons(self):
        """Update tutorial navigation buttons state."""
        self.prev_btn.setEnabled(self.current_tutorial_page > 0)
        self.next_btn.setEnabled(self.current_tutorial_page < len(self.tutorial_pages) - 1)
        self.finish_btn.setEnabled(self.current_tutorial_page == len(self.tutorial_pages) - 1)

    def install_package(self):
        """Install a package via pip."""
        package_name = self.install_input.text().strip()
        if not package_name:
            self.show_error_message("Input Error", "Please enter a package name.")
            return
        self.status_bar.setText(f"Installing {package_name}...")
        self.progress_bar.show()
        threading.Thread(target=self.run_pip_install, args=(package_name,)).start()

    def check_required_modules(self):
        """Check if required modules are installed and install them if missing."""
        required_modules = ['requests', 'psutil', 'PyQt5']
        missing_modules = []
        
        for module in required_modules:
            try:
                importlib.import_module(module)
            except ImportError:
                missing_modules.append(module)
        
        if missing_modules:
            try:
                self.status_bar.setText(f"Installing required modules: {', '.join(missing_modules)}...")
                self.progress_bar.show()
                
                for module in missing_modules:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", module])
                
                self.show_success_message("Success", f"Successfully installed required modules: {', '.join(missing_modules)}")
            except Exception as e:
                self.show_error_message("Error", f"Failed to install required modules: {str(e)}")
            finally:
                self.progress_bar.hide()
                self.status_bar.setText("Ready")


def main():
    app = QApplication(sys.argv)
    window = PackageManager()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

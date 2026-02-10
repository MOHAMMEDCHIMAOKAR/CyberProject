"""
Unified DoS Detection & Testing Environment
Integrates both the detection system and simulator for comprehensive testing
Run this file to start the integrated testing environment
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from datetime import datetime
import subprocess
import sys
import os
import ctypes

class IntegratedEnvironment:
    """Unified DoS Detection & Testing Environment"""
    
    @staticmethod
    def run_as_admin(script_name):
        """Run a Python script with administrator privileges"""
        try:
            # Get the full path to the script
            script_path = os.path.join(r'c:\Users\admin\HMM\CyberProject', script_name)
            python_exe = sys.executable
            
            # Use ctypes to run with admin privileges on Windows
            if sys.platform == 'win32':
                # Create the command to run Python script as admin
                ctypes.windll.shell32.ShellExecuteW(None, "runas", python_exe, f'"{script_path}"', None, 1)
            else:
                # For non-Windows systems, just run normally
                subprocess.Popen([python_exe, script_path])
            
            return True
        except Exception as e:
            print(f"Error running as admin: {e}")
            return False
    
    def __init__(self, root):
        self.root = root
        self.root.title("DoS Detection & Testing Environment - Integrated")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)
        
        self.detector_process = None
        self.simulator_process = None
        self.detector_running = False
        self.simulator_running = False
        
        self._setup_styles()
        self._create_widgets()
        
    def _setup_styles(self):
        """Configure ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('TFrame', background='#F5F5F5')
        style.configure('TLabel', background='#F5F5F5')
        style.configure('Title.TLabel', font=('Segoe UI', 16, 'bold'), foreground='#333')
        style.configure('Subtitle.TLabel', font=('Segoe UI', 11, 'bold'), foreground='#666')
        style.configure('Status.TLabel', font=('Segoe UI', 10), foreground='#666')
        style.configure('Start.TButton', font=('Segoe UI', 10, 'bold'), foreground='#4CAF50')
        style.configure('Stop.TButton', font=('Segoe UI', 10, 'bold'), foreground='#F44336')
        style.configure('Action.TButton', font=('Segoe UI', 9))
        
    def _create_widgets(self):
        """Create all GUI widgets"""
        main_container = ttk.Frame(self.root, padding=15)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header = ttk.Frame(main_container)
        header.pack(fill=tk.X, pady=(0, 15))
        
        title = ttk.Label(
            header,
            text="🛡️ DoS Detection & Testing Environment",
            style='Title.TLabel'
        )
        title.pack(side=tk.LEFT)
        
        subtitle = ttk.Label(
            header,
            text="Integrated Detection System + Simulator",
            style='Subtitle.TLabel'
        )
        subtitle.pack(side=tk.LEFT, padx=(20, 0))
        
        # Content area with two columns
        content = ttk.Frame(main_container)
        content.pack(fill=tk.BOTH, expand=True)
        
        # Left column - Detector
        left_column = ttk.LabelFrame(content, text="🛡️ DoS Detection System", padding=15)
        left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 7))
        
        self._create_detector_panel(left_column)
        
        # Right column - Simulator
        right_column = ttk.LabelFrame(content, text="⚠️ DoS Simulator", padding=15)
        right_column.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(7, 0))
        
        self._create_simulator_panel(right_column)
        
        # Status bar
        self._create_status_bar(main_container)
        
    def _create_detector_panel(self, parent):
        """Create detector control panel"""
        # Description
        desc = ttk.Label(
            parent,
            text="Monitor network traffic for DoS attacks",
            foreground='#666'
        )
        desc.pack(fill=tk.X, pady=(0, 15))
        
        # Status
        status_frame = ttk.Frame(parent)
        status_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(status_frame, text="Status:").pack(side=tk.LEFT, padx=(0, 10))
        self.detector_status = ttk.Label(
            status_frame,
            text="⚫ Stopped",
            font=('Segoe UI', 10, 'bold'),
            foreground='#999'
        )
        self.detector_status.pack(side=tk.LEFT)
        
        # Control buttons
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.detector_start_btn = ttk.Button(
            button_frame,
            text="▶ Start Detector",
            style='Start.TButton',
            command=self._start_detector
        )
        self.detector_start_btn.pack(fill=tk.X, pady=(0, 5))
        
        self.detector_stop_btn = ttk.Button(
            button_frame,
            text="⏹ Stop Detector",
            style='Stop.TButton',
            command=self._stop_detector,
            state=tk.DISABLED
        )
        self.detector_stop_btn.pack(fill=tk.X)
        
        # Info text
        info_text = tk.Text(parent, height=8, width=50, wrap=tk.WORD, state=tk.DISABLED)
        info_text.pack(fill=tk.BOTH, expand=True)
        
        info_text.config(state=tk.NORMAL)
        info_text.insert(tk.END, 
            "DoS Detection System Features:\n\n"
            "✓ Real-time network monitoring\n"
            "✓ Multiple attack detection:\n"
            "  - High request rates\n"
            "  - Connection floods\n"
            "  - SYN floods\n"
            "  - Abnormal packet sizes\n"
            "✓ Live statistics dashboard\n"
            "✓ Alert notifications\n"
            "✓ System logging\n\n"
            "Requires administrator privileges"
        )
        info_text.config(state=tk.DISABLED)
        
    def _create_simulator_panel(self, parent):
        """Create simulator control panel"""
        # Description
        desc = ttk.Label(
            parent,
            text="Generate synthetic DoS traffic for testing",
            foreground='#666'
        )
        desc.pack(fill=tk.X, pady=(0, 15))
        
        # Status
        status_frame = ttk.Frame(parent)
        status_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(status_frame, text="Status:").pack(side=tk.LEFT, padx=(0, 10))
        self.simulator_status = ttk.Label(
            status_frame,
            text="⚫ Stopped",
            font=('Segoe UI', 10, 'bold'),
            foreground='#999'
        )
        self.simulator_status.pack(side=tk.LEFT)
        
        # Control buttons
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.simulator_start_btn = ttk.Button(
            button_frame,
            text="▶ Start Simulator",
            style='Start.TButton',
            command=self._start_simulator
        )
        self.simulator_start_btn.pack(fill=tk.X, pady=(0, 5))
        
        self.simulator_stop_btn = ttk.Button(
            button_frame,
            text="⏹ Stop Simulator",
            style='Stop.TButton',
            command=self._stop_simulator,
            state=tk.DISABLED
        )
        self.simulator_stop_btn.pack(fill=tk.X)
        
        # Info text
        info_text = tk.Text(parent, height=8, width=50, wrap=tk.WORD, state=tk.DISABLED)
        info_text.pack(fill=tk.BOTH, expand=True)
        
        info_text.config(state=tk.NORMAL)
        info_text.insert(tk.END, 
            "DoS Simulator Features:\n\n"
            "✓ 4 Attack Types:\n"
            "  - High Request Rate\n"
            "  - Connection Flood\n"
            "  - SYN Flood\n"
            "  - Abnormal Packet Sizes\n"
            "✓ Configurable intensity (0.5x - 5.0x)\n"
            "✓ Custom duration (1-300 seconds)\n"
            "✓ Target IP configuration\n"
            "✓ Real-time status monitoring\n\n"
            "⚠️ Use only on authorized networks"
        )
        info_text.config(state=tk.DISABLED)
        
    def _create_status_bar(self, parent):
        """Create status bar"""
        status_bar = ttk.Frame(parent, relief=tk.SUNKEN)
        status_bar.pack(fill=tk.X, pady=(10, 0))
        
        self.status_text = ttk.Label(
            status_bar,
            text="Ready - Click 'Start Detector' and 'Start Simulator' to begin testing",
            font=('Segoe UI', 9)
        )
        self.status_text.pack(side=tk.LEFT, padx=5, pady=2)
        
    def _start_detector(self):
        """Start the detection system with admin privileges"""
        try:
            messagebox.showinfo(
                "Starting Detector",
                "The DoS Detection System will open with administrator privileges.\n\n"
                "A UAC prompt may appear - click 'Yes' to allow admin access.\n"
                "The detector requires admin privileges for packet capture."
            )
            
            # Run detector as admin
            if self.run_as_admin('gui_main.py'):
                self.detector_running = True
                self.detector_status.config(text="🟢 Running", foreground='#4CAF50')
                self.detector_start_btn.config(state=tk.DISABLED)
                self.detector_stop_btn.config(state=tk.NORMAL)
                self.status_text.config(text="Detector: Running | Simulator: " + 
                                       ("Running" if self.simulator_running else "Stopped"))
            else:
                messagebox.showerror("Error", "Failed to start detector with admin privileges")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start detector: {e}")
            
    def _stop_detector(self):
        """Stop the detection system"""
        try:
            if self.detector_process:
                self.detector_process.terminate()
                self.detector_process.wait(timeout=5)
            
            self.detector_running = False
            self.detector_status.config(text="⚫ Stopped", foreground='#999')
            self.detector_start_btn.config(state=tk.NORMAL)
            self.detector_stop_btn.config(state=tk.DISABLED)
            self.status_text.config(text="Detector: Stopped | Simulator: " + 
                                   ("Running" if self.simulator_running else "Stopped"))
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stop detector: {e}")
            
    def _start_simulator(self):
        """Start the simulator"""
        try:
            messagebox.showinfo(
                "Starting Simulator",
                "The DoS Simulator window will open.\n\n"
                "⚠️ WARNING: Only use on networks you own or have authorization to test!\n"
                "Configure target IP, attack type, and intensity before starting."
            )
            
            # Start dos_simulator.py
            self.simulator_process = subprocess.Popen(
                [sys.executable, 'dos_simulator.py'],
                cwd=r'c:\Users\admin\HMM\CyberProject'
            )
            
            self.simulator_running = True
            self.simulator_status.config(text="🟢 Running", foreground='#4CAF50')
            self.simulator_start_btn.config(state=tk.DISABLED)
            self.simulator_stop_btn.config(state=tk.NORMAL)
            self.status_text.config(text="Detector: " + 
                                   ("Running" if self.detector_running else "Stopped") + 
                                   " | Simulator: Running")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start simulator: {e}")
            
    def _stop_simulator(self):
        """Stop the simulator"""
        try:
            if self.simulator_process:
                self.simulator_process.terminate()
                self.simulator_process.wait(timeout=5)
            
            self.simulator_running = False
            self.simulator_status.config(text="⚫ Stopped", foreground='#999')
            self.simulator_start_btn.config(state=tk.NORMAL)
            self.simulator_stop_btn.config(state=tk.DISABLED)
            self.status_text.config(text="Detector: " + 
                                   ("Running" if self.detector_running else "Stopped") + 
                                   " | Simulator: Stopped")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stop simulator: {e}")


def main():
    """Main entry point"""
    root = tk.Tk()
    app = IntegratedEnvironment(root)
    
    def on_closing():
        """Handle window close"""
        if messagebox.askokcancel("Quit", "Stop all running processes and quit?"):
            try:
                if app.detector_running:
                    app._stop_detector()
                if app.simulator_running:
                    app._stop_simulator()
            except:
                pass
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == '__main__':
    main()

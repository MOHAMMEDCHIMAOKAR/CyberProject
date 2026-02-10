"""
DoS Detection System - Professional GUI
Main application window with dashboard and controls
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from gui_components import StatCard, AlertItem, LogViewer, StatusIndicator, ConfigSlider
from gui_detector import GUIDetector
from config import Config

class DoSDetectionGUI:
    """Main GUI application for DoS Detection System"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("DoS Detection System - Professional Edition")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Initialize detector
        self.detector = GUIDetector()
        self.running = False
        
        # Alert storage
        self.recent_alerts = []
        self.max_alerts = 10
        
        # Setup GUI
        self._setup_styles()
        self._create_widgets()
        
        # Start update loop
        self.root.after(1000, self._update_loop)
        
    def _setup_styles(self):
        """Configure ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('TFrame', background='#F5F5F5')
        style.configure('Card.TFrame', background='#FFFFFF', relief=tk.RAISED)
        style.configure('TLabel', background='#F5F5F5')
        style.configure('Title.TLabel', font=('Segoe UI', 16, 'bold'), foreground='#333')
        style.configure('Subtitle.TLabel', font=('Segoe UI', 11, 'bold'), foreground='#666')
        
        # Button styles
        style.configure('Start.TButton', font=('Segoe UI', 10, 'bold'), foreground='#4CAF50')
        style.configure('Stop.TButton', font=('Segoe UI', 10, 'bold'), foreground='#F44336')
        style.configure('Action.TButton', font=('Segoe UI', 9))
        
    def _create_widgets(self):
        """Create all GUI widgets"""
        # Main container
        main_container = ttk.Frame(self.root, padding=10)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Header
        self._create_header(main_container)
        
        # Content area with two columns
        content = ttk.Frame(main_container)
        content.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Left column (statistics and controls)
        left_column = ttk.Frame(content)
        left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        self._create_statistics_panel(left_column)
        self._create_control_panel(left_column)
        self._create_config_panel(left_column)
        
        # Right column (alerts and logs)
        right_column = ttk.Frame(content)
        right_column.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        self._create_alerts_panel(right_column)
        self._create_logs_panel(right_column)
        
        # Status bar
        self._create_status_bar(main_container)
        
    def _create_header(self, parent):
        """Create header with title and status"""
        header = ttk.Frame(parent)
        header.pack(fill=tk.X, pady=(0, 10))
        
        # Title
        title = ttk.Label(
            header,
            text="🛡️ DoS Detection System",
            style='Title.TLabel'
        )
        title.pack(side=tk.LEFT)
        
        # Status indicator
        status_frame = ttk.Frame(header)
        status_frame.pack(side=tk.RIGHT)
        
        self.status_indicator = StatusIndicator(status_frame)
        self.status_indicator.pack(side=tk.LEFT, padx=(0, 10))
        
        self.status_label = ttk.Label(
            status_frame,
            text="Stopped",
            font=('Segoe UI', 10, 'bold'),
            foreground='#999'
        )
        self.status_label.pack(side=tk.LEFT)
        
    def _create_statistics_panel(self, parent):
        """Create statistics dashboard"""
        panel = ttk.LabelFrame(parent, text="📊 Real-Time Statistics", padding=15)
        panel.pack(fill=tk.X, pady=(0, 10))
        
        # Statistics grid
        stats_grid = ttk.Frame(panel)
        stats_grid.pack(fill=tk.X)
        
        # Create stat cards
        self.stat_active_ips = StatCard(stats_grid, "Active IPs", "0", "#2196F3")
        self.stat_active_ips.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        
        self.stat_packets = StatCard(stats_grid, "Total Packets", "0", "#4CAF50")
        self.stat_packets.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        self.stat_connections = StatCard(stats_grid, "Connections", "0", "#FF9800")
        self.stat_connections.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        
        self.stat_alerts = StatCard(stats_grid, "Alerts", "0", "#F44336")
        self.stat_alerts.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        stats_grid.columnconfigure(0, weight=1)
        stats_grid.columnconfigure(1, weight=1)
        
    def _create_control_panel(self, parent):
        """Create control panel"""
        panel = ttk.LabelFrame(parent, text="🎮 Controls", padding=15)
        panel.pack(fill=tk.X, pady=(0, 10))
        
        # Interface selection
        interface_frame = ttk.Frame(panel)
        interface_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(interface_frame, text="Network Interface:").pack(side=tk.LEFT, padx=(0, 10))
        
        self.interface_var = tk.StringVar(value="All Interfaces")
        self.interface_combo = ttk.Combobox(
            interface_frame,
            textvariable=self.interface_var,
            state='readonly',
            width=30
        )
        self.interface_combo['values'] = self._get_interfaces()
        self.interface_combo.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Target IP scanning option
        target_frame = ttk.Frame(panel)
        target_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(target_frame, text="Target IP (optional):").pack(side=tk.LEFT, padx=(0, 10))
        
        self.target_ip_var = tk.StringVar(value="")
        self.target_ip_entry = ttk.Entry(
            target_frame,
            textvariable=self.target_ip_var,
            width=30
        )
        self.target_ip_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        ttk.Label(target_frame, text="(Leave empty to monitor all IPs)", foreground='#999').pack(side=tk.LEFT)
        
        # Control buttons
        button_frame = ttk.Frame(panel)
        button_frame.pack(fill=tk.X)
        
        self.start_button = ttk.Button(
            button_frame,
            text="▶ Start Monitoring",
            style='Start.TButton',
            command=self._start_monitoring
        )
        self.start_button.pack(side=tk.LEFT, padx=(0, 5), fill=tk.X, expand=True)
        
        self.stop_button = ttk.Button(
            button_frame,
            text="⏹ Stop Monitoring",
            style='Stop.TButton',
            command=self._stop_monitoring,
            state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
    def _create_config_panel(self, parent):
        """Create configuration panel"""
        panel = ttk.LabelFrame(parent, text="⚙️ Configuration", padding=15)
        panel.pack(fill=tk.BOTH, expand=True)
        
        # Sliders
        self.slider_requests = ConfigSlider(
            panel,
            "Max Requests/sec",
            from_=50,
            to=500,
            initial=Config.MAX_REQUESTS_PER_SECOND
        )
        self.slider_requests.pack(fill=tk.X, pady=5)
        
        self.slider_connections = ConfigSlider(
            panel,
            "Max Connections",
            from_=10,
            to=200,
            initial=Config.MAX_CONNECTIONS_PER_IP
        )
        self.slider_connections.pack(fill=tk.X, pady=5)
        
        self.slider_syn = ConfigSlider(
            panel,
            "SYN Flood Threshold",
            from_=20,
            to=200,
            initial=Config.SYN_FLOOD_THRESHOLD
        )
        self.slider_syn.pack(fill=tk.X, pady=5)
        
        # Apply button
        ttk.Button(
            panel,
            text="Apply Configuration",
            style='Action.TButton',
            command=self._apply_config
        ).pack(pady=(10, 0))
        
    def _create_alerts_panel(self, parent):
        """Create alerts panel"""
        panel = ttk.LabelFrame(parent, text="🚨 Recent Alerts", padding=10)
        panel.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Scrollable frame for alerts
        canvas = tk.Canvas(panel, bg='#FFFFFF', highlightthickness=0)
        scrollbar = ttk.Scrollbar(panel, orient="vertical", command=canvas.yview)
        
        self.alerts_frame = ttk.Frame(canvas)
        self.alerts_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.alerts_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Clear button
        ttk.Button(
            panel,
            text="Clear Alerts",
            style='Action.TButton',
            command=self._clear_alerts
        ).pack(pady=(5, 0))
        
    def _create_logs_panel(self, parent):
        """Create logs panel"""
        panel = ttk.LabelFrame(parent, text="📝 System Logs", padding=10)
        panel.pack(fill=tk.BOTH, expand=True)
        
        self.log_viewer = LogViewer(panel)
        self.log_viewer.pack(fill=tk.BOTH, expand=True)
        
        # Log controls
        log_controls = ttk.Frame(panel)
        log_controls.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Button(
            log_controls,
            text="Clear Logs",
            style='Action.TButton',
            command=self._clear_logs
        ).pack(side=tk.LEFT)
        
        # Initial log message
        self.log_viewer.add_log("DoS Detection System initialized", "SUCCESS")
        self.log_viewer.add_log(f"Configuration loaded - Max Requests: {Config.MAX_REQUESTS_PER_SECOND}/sec", "INFO")
        
    def _create_status_bar(self, parent):
        """Create status bar"""
        status_bar = ttk.Frame(parent, relief=tk.SUNKEN)
        status_bar.pack(fill=tk.X, pady=(10, 0))
        
        self.status_text = ttk.Label(
            status_bar,
            text="Ready",
            font=('Segoe UI', 9)
        )
        self.status_text.pack(side=tk.LEFT, padx=5, pady=2)
        
    def _get_interfaces(self):
        """Get available network interfaces"""
        try:
            from scapy.all import get_if_list
            interfaces = get_if_list()
            return ["All Interfaces"] + interfaces
        except:
            return ["All Interfaces"]
            
    def _validate_ip(self, ip_address):
        """Validate IP address format"""
        try:
            parts = ip_address.split('.')
            if len(parts) != 4:
                return False
            for part in parts:
                num = int(part)
                if num < 0 or num > 255:
                    return False
            return True
        except ValueError:
            return False
            
    def _start_monitoring(self):
        """Start DoS detection"""
        interface = None if self.interface_var.get() == "All Interfaces" else self.interface_var.get()
        target_ip = self.target_ip_var.get().strip() if self.target_ip_var.get() else None
        
        # Validate target IP if provided
        if target_ip:
            if not self._validate_ip(target_ip):
                messagebox.showerror("Error", f"Invalid IP address format: {target_ip}")
                return
        
        if self.detector.start_detection(interface, target_ip):
            self.running = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.interface_combo.config(state=tk.DISABLED)
            self.target_ip_entry.config(state=tk.DISABLED)
            
            self.status_indicator.set_status('running')
            self.status_label.config(text="Running", foreground='#4CAF50')
            
            status_msg = f"Monitoring started on {self.interface_var.get()}"
            if target_ip:
                status_msg += f" | Target IP: {target_ip}"
            self.status_text.config(text=status_msg)
            
            self.log_viewer.add_log(status_msg, "SUCCESS")
        else:
            messagebox.showerror("Error", "Failed to start monitoring. Run as Administrator.")
            
    def _stop_monitoring(self):
        """Stop DoS detection"""
        if self.detector.stop_detection():
            self.running = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.interface_combo.config(state='readonly')
            self.target_ip_entry.config(state=tk.NORMAL)
            
            self.status_indicator.set_status('stopped')
            self.status_label.config(text="Stopped", foreground='#999')
            self.status_text.config(text="Monitoring stopped")
            
            self.log_viewer.add_log("Monitoring stopped", "INFO")
            
    def _apply_config(self):
        """Apply configuration changes"""
        max_requests = self.slider_requests.get()
        max_connections = self.slider_connections.get()
        syn_threshold = self.slider_syn.get()
        
        self.detector.update_config(max_requests, max_connections, syn_threshold)
        self.status_text.config(text="Configuration updated")
        
    def _clear_alerts(self):
        """Clear all alerts"""
        for widget in self.alerts_frame.winfo_children():
            widget.destroy()
        self.recent_alerts.clear()
        
    def _clear_logs(self):
        """Clear all logs"""
        self.log_viewer.clear()
        self.log_viewer.add_log("Logs cleared", "INFO")
        
    def _update_loop(self):
        """Update GUI with latest data"""
        if self.running:
            # Update statistics
            stats = self.detector.get_statistics()
            self.stat_active_ips.update_value(stats.get('active_ips', 0))
            self.stat_packets.update_value(stats.get('total_packets', 0))
            self.stat_connections.update_value(stats.get('total_connections', 0))
            self.stat_alerts.update_value(stats.get('total_alerts', 0))
            
            # Process new alerts
            new_alerts = self.detector.get_alerts()
            for alert in new_alerts:
                self._add_alert(alert)
                
            # Process new logs
            new_logs = self.detector.get_logs()
            for level, message in new_logs:
                self.log_viewer.add_log(message, level)
                
        # Schedule next update
        self.root.after(1000, self._update_loop)
        
    def _add_alert(self, alert):
        """Add alert to panel"""
        # Add to list
        self.recent_alerts.insert(0, alert)
        if len(self.recent_alerts) > self.max_alerts:
            self.recent_alerts.pop()
            
        # Rebuild alerts display
        for widget in self.alerts_frame.winfo_children():
            widget.destroy()
            
        for alert_data in self.recent_alerts:
            alert_widget = AlertItem(
                self.alerts_frame,
                alert_data['timestamp'],
                alert_data['severity'],
                alert_data['ip_address'],
                alert_data['attack_type']
            )
            alert_widget.pack(fill=tk.X, pady=2)


def main():
    """Main entry point"""
    root = tk.Tk()
    app = DoSDetectionGUI(root)
    
    # Handle window close
    def on_closing():
        if app.running:
            if messagebox.askokcancel("Quit", "Monitoring is active. Stop and quit?"):
                app._stop_monitoring()
                root.destroy()
        else:
            root.destroy()
            
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == '__main__':
    main()

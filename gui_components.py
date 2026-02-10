"""
GUI Components for DoS Detection System
Reusable widgets and custom components
"""

import tkinter as tk
from tkinter import ttk

class StatCard(ttk.Frame):
    """Statistical display card widget"""
    
    def __init__(self, parent, title, initial_value="0", color="#2196F3"):
        super().__init__(parent, relief=tk.RAISED, borderwidth=2)
        self.color = color
        
        # Title label
        self.title_label = ttk.Label(
            self,
            text=title,
            font=("Segoe UI", 10, "bold"),
            foreground="#666"
        )
        self.title_label.pack(pady=(10, 5))
        
        # Value label
        self.value_label = ttk.Label(
            self,
            text=initial_value,
            font=("Segoe UI", 24, "bold"),
            foreground=color
        )
        self.value_label.pack(pady=(0, 10))
        
    def update_value(self, value):
        """Update the displayed value"""
        self.value_label.config(text=str(value))


class AlertItem(ttk.Frame):
    """Single alert item widget"""
    
    def __init__(self, parent, timestamp, severity, ip_address, attack_type):
        super().__init__(parent, relief=tk.GROOVE, borderwidth=1)
        
        # Color mapping for severity
        colors = {
            'LOW': '#FFC107',
            'MEDIUM': '#FF9800',
            'HIGH': '#FF5722',
            'CRITICAL': '#F44336'
        }
        
        color = colors.get(severity, '#999')
        
        # Severity indicator
        severity_frame = tk.Frame(self, bg=color, width=5)
        severity_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        # Content frame
        content = ttk.Frame(self)
        content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Time and severity
        header = ttk.Label(
            content,
            text=f"{timestamp} - {severity}",
            font=("Segoe UI", 9, "bold")
        )
        header.pack(anchor=tk.W)
        
        # IP and attack type
        details = ttk.Label(
            content,
            text=f"{ip_address} - {attack_type}",
            font=("Segoe UI", 9)
        )
        details.pack(anchor=tk.W)


class LogViewer(ttk.Frame):
    """Scrollable log viewer widget"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Text widget
        self.text = tk.Text(
            self,
            wrap=tk.WORD,
            yscrollcommand=scrollbar.set,
            font=("Consolas", 9),
            bg="#1E1E1E",
            fg="#D4D4D4",
            insertbackground="#FFFFFF",
            state=tk.DISABLED
        )
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.text.yview)
        
        # Configure tags for colored output
        self.text.tag_config("INFO", foreground="#4EC9B0")
        self.text.tag_config("WARNING", foreground="#FFC107")
        self.text.tag_config("ERROR", foreground="#F44336")
        self.text.tag_config("SUCCESS", foreground="#4CAF50")
        
    def add_log(self, message, level="INFO"):
        """Add a log message"""
        self.text.config(state=tk.NORMAL)
        self.text.insert(tk.END, message + "\n", level)
        self.text.see(tk.END)
        self.text.config(state=tk.DISABLED)
        
    def clear(self):
        """Clear all logs"""
        self.text.config(state=tk.NORMAL)
        self.text.delete(1.0, tk.END)
        self.text.config(state=tk.DISABLED)


class StatusIndicator(tk.Canvas):
    """Status indicator with color states"""
    
    def __init__(self, parent, size=20):
        super().__init__(parent, width=size, height=size, bg="#F5F5F5", highlightthickness=0)
        self.size = size
        self.indicator = self.create_oval(2, 2, size-2, size-2, fill="#999", outline="")
        
    def set_status(self, status):
        """Set status: 'running', 'stopped', 'error'"""
        colors = {
            'running': '#4CAF50',
            'stopped': '#999',
            'error': '#F44336'
        }
        self.itemconfig(self.indicator, fill=colors.get(status, '#999'))


class ConfigSlider(ttk.Frame):
    """Configuration slider with label and value display"""
    
    def __init__(self, parent, label, from_=0, to=100, initial=50, command=None):
        super().__init__(parent)
        
        # Header frame
        header = ttk.Frame(self)
        header.pack(fill=tk.X, pady=(0, 5))
        
        # Label
        ttk.Label(
            header,
            text=label,
            font=("Segoe UI", 9, "bold")
        ).pack(side=tk.LEFT)
        
        # Value display
        self.value_label = ttk.Label(
            header,
            text=str(initial),
            font=("Segoe UI", 9),
            foreground="#2196F3"
        )
        self.value_label.pack(side=tk.RIGHT)
        
        # Slider
        self.slider = ttk.Scale(
            self,
            from_=from_,
            to=to,
            orient=tk.HORIZONTAL,
            command=self._on_change
        )
        self.slider.set(initial)
        self.slider.pack(fill=tk.X)
        
        self.custom_command = command
        
    def _on_change(self, value):
        """Handle slider change"""
        int_value = int(float(value))
        self.value_label.config(text=str(int_value))
        if hasattr(self, 'custom_command') and self.custom_command:
            self.custom_command(int_value)
            
    def get(self):
        """Get current value"""
        return int(self.slider.get())
    
    def set(self, value):
        """Set slider value"""
        self.slider.set(value)
        self.value_label.config(text=str(int(value)))

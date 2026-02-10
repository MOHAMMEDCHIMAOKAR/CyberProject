"""
GUI Detector - Bridge between GUI and detection system
"""

import threading
import queue
from datetime import datetime
from dos_detector import DoSDetector
from config import Config

class GUIDetector:
    """Wrapper for DoSDetector with GUI integration"""
    
    def __init__(self, gui_callback=None):
        self.detector = DoSDetector()
        self.gui_callback = gui_callback
        self.alert_queue = queue.Queue()
        self.log_queue = queue.Queue()
        self.running = False
        self.monitor_thread = None
        self.target_ip = None
        
        # Override alert system to capture alerts
        self._setup_alert_capture()
        
    def _setup_alert_capture(self):
        """Setup alert capture for GUI"""
        original_send_alert = self.detector.alert_system.send_alert
        
        def gui_send_alert(attack_type, ip_address, details, severity):
            # Call original
            original_send_alert(attack_type, ip_address, details, severity)
            
            # Send to GUI queue
            alert_data = {
                'timestamp': datetime.now().strftime('%H:%M:%S'),
                'severity': severity,
                'ip_address': ip_address,
                'attack_type': attack_type,
                'details': details
            }
            self.alert_queue.put(alert_data)
            
        self.detector.alert_system.send_alert = gui_send_alert
        
    def start_detection(self, interface=None, target_ip=None):
        """Start packet sniffing with optional target IP filtering"""
        self.target_ip = target_ip
        if self.running:
            return False
            
        self.running = True
        self.log_queue.put(("INFO", f"Starting DoS detection on interface: {interface or 'all'} with target IP: {target_ip}"))
        
        self.monitor_thread = threading.Thread(
            target=self._run_detection,
            args=(interface,),
            daemon=True
        )
        self.monitor_thread.start()
        return True
        
    def _run_detection(self, interface):
        """Run detection (called in thread)"""
        try:
            self.detector.start_detection(interface, self.target_ip)
        except Exception as e:
            self.log_queue.put(("ERROR", f"Detection error: {e}"))
            self.running = False
            
    def stop_detection(self):
        """Stop detection"""
        if not self.running:
            return False
            
        self.running = False
        self.detector.stop_detection()
        self.log_queue.put(("INFO", "DoS detection stopped"))
        return True
        
    def get_statistics(self):
        """Get current statistics"""
        if not self.running:
            return {
                'active_ips': 0,
                'total_packets': 0,
                'total_connections': 0,
                'total_alerts': 0
            }
        return self.detector.get_statistics()
        
    def get_alerts(self):
        """Get pending alerts from queue"""
        alerts = []
        while not self.alert_queue.empty():
            try:
                alerts.append(self.alert_queue.get_nowait())
            except queue.Empty:
                break
        return alerts
        
    def get_logs(self):
        """Get pending logs from queue"""
        logs = []
        while not self.log_queue.empty():
            try:
                logs.append(self.log_queue.get_nowait())
            except queue.Empty:
                break
        return logs
        
    def update_config(self, max_requests=None, max_connections=None, syn_threshold=None):
        """Update configuration"""
        if max_requests is not None:
            Config.MAX_REQUESTS_PER_SECOND = max_requests
            self.log_queue.put(("INFO", f"Updated max requests/sec: {max_requests}"))
            
        if max_connections is not None:
            Config.MAX_CONNECTIONS_PER_IP = max_connections
            self.log_queue.put(("INFO", f"Updated max connections: {max_connections}"))
            
        if syn_threshold is not None:
            Config.SYN_FLOOD_THRESHOLD = syn_threshold
            self.log_queue.put(("INFO", f"Updated SYN threshold: {syn_threshold}"))
            
    def _packet_callback(self, packet):
        """Packet processing callback with target IP filtering"""
        try:
            from scapy.layers.inet import IP, TCP, UDP
            
            # Skip non-IP packets
            if IP not in packet:
                return
                
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
            
            # Filter by target IP if specified
            if self.target_ip:
                if src_ip != self.target_ip and dst_ip != self.target_ip:
                    return
            
            # ...existing code for packet analysis...
        except Exception as e:
            self._add_log(f"Error processing packet: {e}", "ERROR")

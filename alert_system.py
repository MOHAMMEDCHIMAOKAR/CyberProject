"""
Alert System for DoS Detection
Handles console alerts, file logging, and alert management
"""

import logging
from datetime import datetime, timedelta
from colorama import init, Fore, Style
from config import Config

# Initialize colorama for Windows color support
init(autoreset=True)

class AlertSystem:
    """Manages alerts and logging for DoS detection"""
    
    def __init__(self):
        self.alert_history = []
        self.last_alert_time = {}  # Track last alert time per IP
        self.alert_count = 0
        
        # Setup file logging
        logging.basicConfig(
            filename=Config.LOG_FILE,
            level=getattr(logging, Config.LOG_LEVEL),
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
    def send_alert(self, attack_type, ip_address, details, severity="MEDIUM"):
        """Send alert to console and log file"""
        
        # Check cooldown period
        if not self._check_cooldown(ip_address):
            return
            
        # Update alert tracking
        self.last_alert_time[ip_address] = datetime.now()
        self.alert_count += 1
        
        # Create alert message
        alert_data = {
            'timestamp': datetime.now(),
            'attack_type': attack_type,
            'ip_address': ip_address,
            'details': details,
            'severity': severity
        }
        self.alert_history.append(alert_data)
        
        # Display console alert
        self._display_console_alert(alert_data)
        
        # Log to file
        self._log_alert(alert_data)
        
    def _check_cooldown(self, ip_address):
        """Check if enough time has passed since last alert for this IP"""
        if ip_address not in self.last_alert_time:
            return True
            
        time_since_last = datetime.now() - self.last_alert_time[ip_address]
        return time_since_last.total_seconds() >= Config.ALERT_COOLDOWN
        
    def _display_console_alert(self, alert_data):
        """Display color-coded alert in console"""
        severity = alert_data['severity']
        
        # Choose color based on severity
        color_map = {
            'LOW': Fore.YELLOW,
            'MEDIUM': Fore.LIGHTYELLOW_EX,
            'HIGH': Fore.LIGHTRED_EX,
            'CRITICAL': Fore.RED
        }
        color = color_map.get(severity, Fore.WHITE)
        
        # Format alert
        print(f"\n{color}{'='*60}")
        print(f"{Style.BRIGHT}[{severity}] DoS Attack Detected!")
        print(f"  Time: {alert_data['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  Type: {alert_data['attack_type']}")
        print(f"  Source IP: {alert_data['ip_address']}")
        
        # Display details
        for key, value in alert_data['details'].items():
            print(f"  {key}: {value}")
            
        print(f"{'='*60}{Style.RESET_ALL}\n")
        
    def _log_alert(self, alert_data):
        """Log alert to file"""
        log_message = (
            f"[{alert_data['severity']}] {alert_data['attack_type']} - "
            f"IP: {alert_data['ip_address']} - "
            f"Details: {alert_data['details']}"
        )
        
        if alert_data['severity'] == 'CRITICAL':
            self.logger.critical(log_message)
        elif alert_data['severity'] == 'HIGH':
            self.logger.error(log_message)
        elif alert_data['severity'] == 'MEDIUM':
            self.logger.warning(log_message)
        else:
            self.logger.info(log_message)
            
    def get_statistics(self):
        """Get alert statistics"""
        return {
            'total_alerts': self.alert_count,
            'unique_ips': len(self.last_alert_time),
            'recent_alerts': len([a for a in self.alert_history 
                                 if (datetime.now() - a['timestamp']).total_seconds() < 300])
        }
        
    def clear_old_alerts(self, max_age_hours=24):
        """Clear alerts older than specified hours"""
        cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
        self.alert_history = [a for a in self.alert_history 
                             if a['timestamp'] > cutoff_time]

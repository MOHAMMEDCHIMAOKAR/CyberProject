"""
DoS Detector - Main detection engine
Implements multiple detection algorithms
"""

from packet_monitor import PacketMonitor
from alert_system import AlertSystem
from config import Config

class DoSDetector:
    """Main DoS detection engine"""
    
    def __init__(self):
        self.monitor = PacketMonitor()
        self.alert_system = AlertSystem()
        self.running = False
        
    def start_detection(self, interface=None):
        """Start DoS detection"""
        self.running = True
        
        # Start packet monitoring with callback
        self.monitor.start_monitoring(
            interface=interface,
            packet_callback=self._analyze_packet
        )
        
    def _analyze_packet(self, src_ip, packet):
        """Analyze packet for DoS patterns"""
        
        # Skip whitelisted IPs
        if Config.is_whitelisted(src_ip):
            return
            
        # Run detection algorithms
        if Config.ENABLE_RATE_DETECTION:
            self._check_rate_limit(src_ip)
            
        if Config.ENABLE_CONNECTION_DETECTION:
            self._check_connection_flood(src_ip)
            
        if Config.ENABLE_SYN_FLOOD_DETECTION:
            self._check_syn_flood(src_ip)
            
        if Config.ENABLE_PACKET_SIZE_DETECTION:
            self._check_packet_size(packet)
            
    def _check_rate_limit(self, ip_address):
        """Check if IP exceeds request rate limit"""
        rate = self.monitor.get_ip_packet_rate(ip_address)
        
        if rate > Config.MAX_REQUESTS_PER_SECOND:
            severity = Config.get_severity(rate, Config.MAX_REQUESTS_PER_SECOND)
            
            details = {
                'Request Rate': f'{rate:.2f} req/sec',
                'Threshold': f'{Config.MAX_REQUESTS_PER_SECOND} req/sec',
                'Exceeded By': f'{rate - Config.MAX_REQUESTS_PER_SECOND:.2f} req/sec'
            }
            
            self.alert_system.send_alert(
                attack_type='High Request Rate',
                ip_address=ip_address,
                details=details,
                severity=severity
            )
            
    def _check_connection_flood(self, ip_address):
        """Check if IP has too many concurrent connections"""
        conn_count = self.monitor.get_ip_connection_count(ip_address)
        
        if conn_count > Config.MAX_CONNECTIONS_PER_IP:
            severity = Config.get_severity(conn_count, Config.MAX_CONNECTIONS_PER_IP)
            
            details = {
                'Active Connections': conn_count,
                'Threshold': Config.MAX_CONNECTIONS_PER_IP,
                'Exceeded By': conn_count - Config.MAX_CONNECTIONS_PER_IP
            }
            
            self.alert_system.send_alert(
                attack_type='Connection Flood',
                ip_address=ip_address,
                details=details,
                severity=severity
            )
            
    def _check_syn_flood(self, ip_address):
        """Check for SYN flood attack"""
        syn_rate = self.monitor.get_ip_syn_rate(ip_address)
        
        if syn_rate > Config.SYN_FLOOD_THRESHOLD:
            severity = Config.get_severity(syn_rate, Config.SYN_FLOOD_THRESHOLD)
            
            details = {
                'SYN Rate': f'{syn_rate:.2f} SYN/sec',
                'Threshold': f'{Config.SYN_FLOOD_THRESHOLD} SYN/sec',
                'Exceeded By': f'{syn_rate - Config.SYN_FLOOD_THRESHOLD:.2f} SYN/sec'
            }
            
            self.alert_system.send_alert(
                attack_type='SYN Flood Attack',
                ip_address=ip_address,
                details=details,
                severity=severity
            )
            
    def _check_packet_size(self, packet):
        """Check for abnormal packet sizes"""
        packet_size = len(packet)
        
        if packet_size < Config.MIN_PACKET_SIZE or packet_size > Config.MAX_PACKET_SIZE:
            # Get source IP
            if packet.haslayer('IP'):
                src_ip = packet['IP'].src
                
                details = {
                    'Packet Size': f'{packet_size} bytes',
                    'Normal Range': f'{Config.MIN_PACKET_SIZE}-{Config.MAX_PACKET_SIZE} bytes'
                }
                
                self.alert_system.send_alert(
                    attack_type='Abnormal Packet Size',
                    ip_address=src_ip,
                    details=details,
                    severity='LOW'
                )
                
    def get_statistics(self):
        """Get detection statistics"""
        monitor_stats = self.monitor.get_statistics()
        alert_stats = self.alert_system.get_statistics()
        
        return {
            **monitor_stats,
            'total_alerts': alert_stats['total_alerts'],
            'unique_alert_ips': alert_stats['unique_ips']
        }
        
    def stop_detection(self):
        """Stop DoS detection"""
        self.running = False
        self.monitor.stop_monitoring()

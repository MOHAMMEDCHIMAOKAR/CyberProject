"""
Packet Monitor - Network traffic capture and analysis
"""

import threading
from collections import defaultdict, deque
from datetime import datetime, timedelta
from scapy.all import sniff, IP, TCP, UDP, ICMP
from config import Config

class PacketMonitor:
    """Monitors network packets and tracks statistics"""
    
    def __init__(self):
        self.running = False
        self.packet_count = 0
        
        # Thread-safe data structures
        self.lock = threading.Lock()
        
        # IP tracking with timestamps
        self.ip_packets = defaultdict(lambda: deque())  # IP -> [(timestamp, packet), ...]
        self.ip_connections = defaultdict(int)  # IP -> connection count
        self.ip_syn_packets = defaultdict(lambda: deque())  # IP -> [(timestamp), ...]
        
        # Protocol statistics
        self.protocol_stats = defaultdict(int)
        
        # Packet size tracking
        self.packet_sizes = deque(maxlen=1000)
        
    def start_monitoring(self, interface=None, packet_callback=None):
        """Start packet capture"""
        self.running = True
        self.packet_callback = packet_callback
        
        # Start sniffing in background thread
        sniff_thread = threading.Thread(
            target=self._sniff_packets,
            args=(interface,),
            daemon=True
        )
        sniff_thread.start()
        
    def _sniff_packets(self, interface):
        """Sniff packets (runs in thread)"""
        try:
            sniff(
                iface=interface,
                prn=self._process_packet,
                store=False,
                stop_filter=lambda x: not self.running
            )
        except Exception as e:
            print(f"Error in packet capture: {e}")
            self.running = False
            
    def _process_packet(self, packet):
        """Process captured packet"""
        if not packet.haslayer(IP):
            return
            
        with self.lock:
            self.packet_count += 1
            
            # Extract IP info
            ip_layer = packet[IP]
            src_ip = ip_layer.src
            packet_size = len(packet)
            timestamp = datetime.now()
            
            # Track packet with timestamp
            self.ip_packets[src_ip].append((timestamp, packet))
            
            # Track packet size
            self.packet_sizes.append(packet_size)
            
            # Protocol tracking
            if packet.haslayer(TCP):
                self.protocol_stats['TCP'] += 1
                
                # Track connections
                tcp_layer = packet[TCP]
                if tcp_layer.flags & 0x02:  # SYN flag
                    self.ip_syn_packets[src_ip].append(timestamp)
                    
                # Track active connections
                if tcp_layer.flags & 0x02 and not tcp_layer.flags & 0x10:  # SYN without ACK
                    self.ip_connections[src_ip] += 1
                elif tcp_layer.flags & 0x01:  # FIN flag
                    if self.ip_connections[src_ip] > 0:
                        self.ip_connections[src_ip] -= 1
                        
            elif packet.haslayer(UDP):
                self.protocol_stats['UDP'] += 1
            elif packet.haslayer(ICMP):
                self.protocol_stats['ICMP'] += 1
            else:
                self.protocol_stats['OTHER'] += 1
                
            # Callback for detection
            if self.packet_callback:
                self.packet_callback(src_ip, packet)
                
            # Cleanup old data
            self._cleanup_old_data()
            
    def _cleanup_old_data(self):
        """Remove data outside time window"""
        cutoff_time = datetime.now() - timedelta(seconds=Config.TIME_WINDOW)
        
        # Clean IP packets
        for ip in list(self.ip_packets.keys()):
            self.ip_packets[ip] = deque([
                (ts, pkt) for ts, pkt in self.ip_packets[ip]
                if ts > cutoff_time
            ])
            if not self.ip_packets[ip]:
                del self.ip_packets[ip]
                
        # Clean SYN packets
        for ip in list(self.ip_syn_packets.keys()):
            self.ip_syn_packets[ip] = deque([
                ts for ts in self.ip_syn_packets[ip]
                if ts > cutoff_time
            ])
            if not self.ip_syn_packets[ip]:
                del self.ip_syn_packets[ip]
                
    def get_ip_packet_rate(self, ip_address):
        """Get packets per second for IP"""
        with self.lock:
            if ip_address not in self.ip_packets:
                return 0
                
            packets = self.ip_packets[ip_address]
            if not packets:
                return 0
                
            time_span = (datetime.now() - packets[0][0]).total_seconds()
            if time_span == 0:
                return len(packets)
                
            return len(packets) / time_span
            
    def get_ip_connection_count(self, ip_address):
        """Get active connection count for IP"""
        with self.lock:
            return self.ip_connections.get(ip_address, 0)
            
    def get_ip_syn_rate(self, ip_address):
        """Get SYN packets per second for IP"""
        with self.lock:
            if ip_address not in self.ip_syn_packets:
                return 0
                
            syn_packets = self.ip_syn_packets[ip_address]
            if not syn_packets:
                return 0
                
            time_span = (datetime.now() - syn_packets[0]).total_seconds()
            if time_span == 0:
                return len(syn_packets)
                
            return len(syn_packets) / time_span
            
    def get_statistics(self):
        """Get overall statistics"""
        with self.lock:
            return {
                'total_packets': self.packet_count,
                'active_ips': len(self.ip_packets),
                'total_connections': sum(self.ip_connections.values()),
                'protocol_distribution': dict(self.protocol_stats),
                'avg_packet_size': sum(self.packet_sizes) / len(self.packet_sizes) if self.packet_sizes else 0
            }
            
    def get_active_ips(self):
        """Get list of currently active IPs"""
        with self.lock:
            return list(self.ip_packets.keys())
            
    def stop_monitoring(self):
        """Stop packet capture"""
        self.running = False

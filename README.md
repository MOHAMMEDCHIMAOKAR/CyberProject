# DoS Detection System - Professional Edition

A comprehensive Denial-of-Service (DoS) detection system with real-time monitoring, multi-algorithm threat detection, and an intuitive professional GUI dashboard.

## 🛡️ Features

- **Real-Time Network Monitoring**: Captures and analyzes live network traffic
- **Multi-Algorithm Detection**:
  - High Request Rate Detection
  - Connection Flood Detection
  - SYN Flood Detection
  - Abnormal Packet Size Detection
- **Professional GUI Dashboard**:
  - Real-time statistics display
  - Live alert monitoring
  - System logs viewer
  - Dynamic configuration controls
- **Configurable Thresholds**: Adjust detection sensitivity on-the-fly
- **Alert System**: Severity-based alerts (LOW, MEDIUM, HIGH, CRITICAL)
- **IP Whitelisting**: Trust and ignore packets from known safe IPs
- **Comprehensive Logging**: Detailed system and alert logs

## 📋 Requirements

- Python 3.7+
- Windows, Linux, or macOS
- Administrator/Root privileges (required for packet capture)

### Dependencies

```
scapy>=2.5.0          # Packet capture and analysis
colorama>=0.4.6       # Colored console output
psutil>=5.9.0         # System and process utilities
```

## 🚀 Installation

1. **Clone or download the project**:
   ```bash
   cd CyberProject-1
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation**:
   ```bash
   python -c "import scapy, colorama, psutil; print('All dependencies installed!')"
   ```

## 📖 Usage

### GUI Application (Recommended)

Start the professional dashboard:

```bash
python gui_main.py
```

**Run as Administrator/Root** (required for network packet capture):

- **Windows**: Right-click PowerShell/CMD and select "Run as Administrator"
- **Linux/macOS**: Use `sudo python gui_main.py`

**GUI Controls**:
- **Network Interface**: Select network interface to monitor (or "All Interfaces")
- **Start/Stop Buttons**: Control monitoring session
- **Configuration Sliders**:
  - Max Requests/sec (50-500)
  - Max Connections per IP (10-200)
  - SYN Flood Threshold (20-200)
- **Apply Configuration**: Update thresholds in real-time
- **Real-Time Statistics**: Active IPs, Total Packets, Connections, Alerts
- **Alerts Panel**: View recent detected attacks with severity levels
- **System Logs**: Track application events and detections

### Command-Line Detection (Standalone Engine)

```bash
python dos_detector.py
```

## ⚙️ Configuration

Edit [config.py](config.py) to adjust detection parameters:

```python
# Detection Thresholds
MAX_REQUESTS_PER_SECOND = 100      # Requests per second from single IP
MAX_CONNECTIONS_PER_IP = 50        # Concurrent connections per IP
SYN_FLOOD_THRESHOLD = 50           # SYN packets per second

# Time Windows
TIME_WINDOW = 60                   # Analysis window in seconds
ALERT_COOLDOWN = 60                # Cooldown between alerts

# Feature Toggles
ENABLE_RATE_DETECTION = True
ENABLE_CONNECTION_DETECTION = True
ENABLE_SYN_FLOOD_DETECTION = True
ENABLE_PACKET_SIZE_DETECTION = True

# Logging
LOG_FILE = "dos_alerts.log"
LOG_LEVEL = "INFO"
```

### Adding IPs to Whitelist

In your code or via the alert system:

```python
from config import Config
Config.add_whitelist_ip("192.168.1.100")
Config.remove_whitelist_ip("192.168.1.100")
```

## 📁 Project Structure

```
CyberProject-1/
├── gui_main.py           # Main GUI application entry point
├── gui_detector.py       # GUI-integrated detection engine
├── gui_components.py     # Reusable GUI components (StatCard, AlertItem, etc.)
├── dos_detector.py       # Core DoS detection engine
├── packet_monitor.py     # Network packet capture and analysis
├── alert_system.py       # Alert generation and management
├── config.py             # Central configuration
├── requirements.txt      # Python dependencies
├── dos_alerts.log        # Alert log file (generated)
└── README.md             # This file
```

## 🔍 Alert Severity Levels

Severity is calculated based on how much the detected metric exceeds the threshold:

| Severity | Ratio | Meaning |
|----------|-------|---------|
| **LOW** | 1.0x - 1.2x | Slightly elevated, monitor |
| **MEDIUM** | 1.2x - 1.5x | Concerning, take action |
| **HIGH** | 1.5x - 2.0x | Likely attack, investigate |
| **CRITICAL** | > 2.0x | Confirmed attack, respond |

## 🖥️ System Requirements

- **Minimum**:
  - 512 MB RAM
  - Dual-core processor
  - Standard network interface
  
- **Recommended**:
  - 2+ GB RAM
  - Quad-core processor
  - High-speed network interface
  - Dedicated security network segment

## 🔐 Security Considerations

- **Always run with elevated privileges**: Packet capture requires admin/root access
- **Network permission**: Monitor only networks you own or have authorization for
- **Whitelist trusted IPs**: Add known safe IPs to prevent false positives
- **Regular log review**: Check `dos_alerts.log` for patterns
- **Backup logs**: Archive alert logs for incident analysis

## 🛠️ Troubleshooting

### "Permission Denied" or "No interfaces found"

**Solution**: Run with administrator/root privileges:
- Windows: Right-click terminal → Run as Administrator
- Linux/macOS: `sudo python gui_main.py`

### No packets being captured

1. Verify network interface is active: `ipconfig` (Windows) or `ifconfig` (Linux)
2. Try "All Interfaces" option in GUI
3. Check firewall settings (may block packet capture)
4. Verify Scapy installation: `python -c "from scapy.all import sniff; print('OK')"`

### GUI not starting

1. Ensure tkinter is installed (included with Python on most systems)
2. On Linux, may need: `sudo apt-get install python3-tk`
3. Check Python version: `python --version` (requires 3.7+)

### High CPU usage

- Reduce thresholds to generate fewer alerts
- Monitor fewer interfaces (select specific interface instead of "All")
- Increase TIME_WINDOW in config to analyze broader time periods

### False positives (legitimate traffic flagged)

- Increase thresholds in Configuration panel
- Add known good IPs to whitelist
- Review packet patterns in logs to refine detection

## 📊 Performance Tips

- **High-traffic networks**: Use interface-specific monitoring instead of "All Interfaces"
- **Reduce false positives**: Adjust sliders higher for more selective detection
- **Memory management**: Periodically clear old alerts from the GUI
- **Log rotation**: Archive `dos_alerts.log` regularly for large deployments

## 📝 Logging

All events are logged to `dos_alerts.log`:

```
[2026-02-10 14:23:45] INFO: DoS Detection System initialized
[2026-02-10 14:24:12] SUCCESS: Monitoring started on eth0
[2026-02-10 14:25:33] ALERT: Connection Flood detected from 192.168.1.50
[2026-02-10 14:26:01] CRITICAL: SYN Flood attack from 10.0.0.15
```

## 🎯 Use Cases

- **Enterprise Networks**: Detect and respond to DoS attacks in real-time
- **Security Operations Centers (SOC)**: Monitor multiple network segments
- **Development/Testing**: Validate DoS protection mechanisms
- **Network Administration**: Identify problematic clients consuming bandwidth
- **Security Research**: Analyze attack patterns and behaviors

## 📄 License

This project is provided as-is for educational and authorized security monitoring purposes.

## 👨‍💻 Author Notes

- Built with Python, Tkinter, and Scapy
- Cross-platform compatible (Windows, Linux, macOS)
- Professional-grade GUI with real-time updates
- Modular architecture for easy customization

## 🤝 Contributing

To extend functionality:

1. Modify detection algorithms in [dos_detector.py](dos_detector.py)
2. Add new GUI components to [gui_components.py](gui_components.py)
3. Update configuration thresholds in [config.py](config.py)
4. Test with administrative privileges

## ❓ FAQ

**Q: Can I monitor remote networks?**  
A: Only networks accessible from your machine. Packet capture requires local network access.

**Q: Is this production-ready?**  
A: Yes, with proper tuning for your network environment.

**Q: How accurate is the detection?**  
A: Accuracy depends on threshold configuration. Tune based on your normal traffic patterns.

**Q: Can I export alerts?**  
A: Yes, all alerts are logged to `dos_alerts.log` in plain text format.

**Q: What's the overhead?**  
A: Minimal impact on network performance; CPU usage depends on traffic volume.

---

**Last Updated**: February 2026  
**Version**: 1.0 - Professional Edition

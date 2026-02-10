"""
DoS Detection & Testing Environment - Setup & Usage Guide
========================================================

This unified testing environment allows you to run both the detection system
and the simulator together for comprehensive DoS attack testing and validation.

COMPONENTS:
-----------
1. Detection System (gui_main.py)
   - Monitors network traffic for DoS attacks
   - Multiple attack type detection
   - Real-time statistics and alerts
   - System logging

2. Simulator (dos_simulator.py)
   - Generates synthetic DoS traffic
   - 4 attack types: High Request Rate, Connection Flood, SYN Flood, Packet Size
   - Configurable intensity and duration
   - Target IP configuration

3. Integrated Environment (integrated_environment.py)
   - Unified launcher for both components
   - Easy on/off controls
   - Status monitoring

INSTALLATION:
-------------
1. Install all dependencies:
   pip install -r requirements.txt

2. Ensure you have the following files in your project directory:
   - requirements.txt
   - config.py (configuration settings)
   - gui_main.py (detection system GUI)
   - gui_detector.py (detection logic)
   - gui_components.py (GUI components)
   - dos_simulator.py (simulator GUI and logic)
   - integrated_environment.py (this file's launcher)

RUNNING THE INTEGRATED ENVIRONMENT:
-----------------------------------

Option 1: Run the integrated launcher (recommended)
   python integrated_environment.py

   This opens a unified control panel where you can:
   - Start/Stop the Detection System
   - Start/Stop the Simulator
   - Monitor both systems' status

Option 2: Run components separately
   Terminal 1: python gui_main.py      # Start detection system
   Terminal 2: python dos_simulator.py # Start simulator

TESTING WORKFLOW:
----------------

1. Start the Integrated Environment:
   python integrated_environment.py

2. Click "▶ Start Detector"
   - Detection system window opens
   - Click "Start Monitoring" in the detector window
   - Select network interface or "All Interfaces"
   
3. Click "▶ Start Simulator"
   - Simulator window opens
   - Configure attack parameters:
     * Target IP: 127.0.0.1 (localhost) or your test server
     * Duration: 10-60 seconds
     * Intensity: 1.5x - 3.0x (higher = more traffic)
     * Attack Type: Select desired attack pattern
   
4. Start Attack Simulation
   - Click "▶ Start Simulation" in the simulator
   - Monitor alerts and statistics in the detector window
   
5. Analyze Results
   - View detected attacks in the alerts panel
   - Check statistics for traffic patterns
   - Review system logs
   
6. Stop Everything
   - Close simulator window or click "⏹ Stop Simulation"
   - Stop detector in its window or use integrated environment controls
   - Close integrated environment

CONFIGURATION OPTIONS:
----------------------

In integrated_environment.py, you can customize:
- Window size and layout
- Default target IP addresses
- Process timeout values
- Status update intervals

In dos_simulator.py, you can customize:
- Packet rate calculations
- Source IP ranges for spoofing
- Payload sizes
- Port selections

In gui_main.py / gui_detector.py, you can customize:
- Detection thresholds
- Alert severity levels
- Logging verbosity
- Interface selection

IMPORTANT WARNINGS:
------------------

⚠️ LEGAL & ETHICAL CONSIDERATIONS:
- ONLY use this on networks you own or have explicit written authorization to test
- Unauthorized network testing is illegal in most jurisdictions
- Always get written permission from network administrators before testing
- Use only in isolated lab environments or personal test networks

🔒 SECURITY NOTES:
- Packet spoofing requires elevated privileges (Administrator/root)
- The detection system requires capture privileges
- Both components will prompt for elevated access on Windows
- Network packets sent are synthetic test packets only

REQUIREMENTS:
-------------
- Python 3.7+
- scapy >= 2.5.0 (for packet handling)
- colorama >= 0.4.6 (for terminal colors)
- psutil >= 5.9.0 (for system monitoring)
- tkinter (usually included with Python)
- Administrator/root privileges (for packet operations)

TROUBLESHOOTING:
----------------

Problem: "Permission denied" or "WinError 5"
Solution: Run as Administrator
  - On Windows: Right-click python.exe or terminal → "Run as Administrator"
  - On Linux: Use sudo python integrated_environment.py

Problem: Scapy not found
Solution: Install scapy
  pip install scapy

Problem: No packets detected
Solution:
  - Ensure you're using localhost (127.0.0.1) as target
  - Check firewall settings
  - Verify network interface selection
  - Run detector with "All Interfaces"

Problem: "Port already in use"
Solution:
  - Close other instances of the applications
  - Wait a few seconds before restarting
  - Check for zombie processes

EXAMPLE TEST SCENARIO:
---------------------

1. Open integrated_environment.py in two terminal windows

Terminal 1 (Detection System):
   python gui_main.py
   - Select "All Interfaces"
   - Click "Start Monitoring"
   
Terminal 2 (Simulator):
   python dos_simulator.py
   - Target IP: 127.0.0.1
   - Duration: 30 seconds
   - Attack Type: SYN Flood
   - Intensity: 2.0x
   - Click "Start Simulation"

Expected Result:
   - Detection system shows increased packet/connection counts
   - Alerts appear showing SYN flood detection
   - Statistics update in real-time
   - Logs record all events

PERFORMANCE NOTES:
------------------
- High intensity attacks may consume significant CPU/network resources
- Use 1.5x - 2.0x intensity for stable testing
- Avoid running other network-heavy applications during testing
- Monitor system resources to prevent crashes

NEXT STEPS:
-----------
1. Start with low intensity (1.0x) attacks
2. Gradually increase intensity to find detection thresholds
3. Test each attack type individually first
4. Combine multiple attacks for advanced testing
5. Review logs to fine-tune detection parameters
6. Validate detection accuracy and false positive rates

For more information, see config.py for all configurable parameters.
"""

# This is a documentation file. To use it:
# 1. Read through the instructions above
# 2. Run: python integrated_environment.py
# 3. Follow the testing workflow

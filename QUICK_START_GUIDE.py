"""
DoS Detection & Testing Environment - Quick Start Guide
========================================================

SAMPLE IP ADDRESS FOR TESTING:
172.16.17.163

SETUP INSTRUCTIONS:
===================

1. RUN THE INTEGRATED ENVIRONMENT
   python integrated_environment.py

2. CONFIGURE THE DETECTOR
   - Click "▶ Start Detector"
   - UAC prompt will appear - click "Yes"
   - In detector window:
     * Network Interface: All Interfaces
     * Target IP: 172.16.17.163
     * Click "Start Monitoring"

3. CONFIGURE THE SIMULATOR
   - Click "▶ Start Simulator"
   - In simulator window:
     * Target IP: 172.16.17.163
     * Duration: 30 seconds
     * Intensity: 2.0x
     * Attack Type: Select one:
       - High Request Rate Attack
       - Connection Flood Attack
       - SYN Flood Attack
       - Abnormal Packet Size Attack

4. RUN THE TEST
   - Click "▶ Start Simulation"
   - Watch detector for alerts
   - Monitor statistics in real-time
   - Review logs for events

EXPECTED RESULTS:
=================
✓ Active IPs count increases
✓ Total Packets increases
✓ Connections counter updates
✓ Alerts appear in alerts panel
✓ System logs show detection events
✓ Detector identifies attack type

TESTING WORKFLOW:
=================

Test 1: High Request Rate
   Target: 172.16.17.163
   Attack Type: High Request Rate Attack
   Intensity: 1.5x
   Duration: 20 seconds
   Expected: Detector shows spike in packet rate

Test 2: Connection Flood
   Target: 172.16.17.163
   Attack Type: Connection Flood Attack
   Intensity: 2.0x
   Duration: 30 seconds
   Expected: Connection counter increases significantly

Test 3: SYN Flood
   Target: 172.16.17.163
   Attack Type: SYN Flood Attack
   Intensity: 2.5x
   Duration: 20 seconds
   Expected: SYN flood alert triggered

Test 4: Abnormal Packet Size
   Target: 172.16.17.163
   Attack Type: Abnormal Packet Size Attack
   Intensity: 2.0x
   Duration: 15 seconds
   Expected: Packet size anomaly detected

TROUBLESHOOTING:
================

Issue: No packets detected
Solution:
  1. Check network interface selection (use "All Interfaces")
  2. Verify target IP is correct: 172.16.17.163
  3. Ensure detector is running before simulator
  4. Check Windows Firewall isn't blocking packets

Issue: Detector window won't open
Solution:
  1. Run integrated_environment.py as Administrator
  2. Click "Yes" to UAC prompt
  3. Wait a few seconds for window to appear

Issue: Simulator shows errors
Solution:
  1. Verify scapy is installed: pip install scapy
  2. Run as Administrator
  3. Check target IP format is correct

Issue: Stats not updating
Solution:
  1. Ensure "Start Monitoring" is clicked in detector
  2. Verify target IP matches in both windows
  3. Check logs for error messages

COMMAND LINE ALTERNATIVE:
==========================

If you prefer separate terminals:

Terminal 1 (Detector):
  python gui_main.py
  - Enter Target IP: 172.16.17.163
  - Click "Start Monitoring"

Terminal 2 (Simulator):
  python dos_simulator.py
  - Enter Target IP: 172.16.17.163
  - Select attack type
  - Click "Start Simulation"

SAMPLE IP ADDRESSES FOR DIFFERENT TESTS:
=========================================

Local Machine:     127.0.0.1
Sample Network IP: 172.16.17.163
Alternative IPs:   192.168.1.100
                   10.0.0.50

IMPORTANT NOTES:
================
⚠️ Only use this on authorized networks/systems
⚠️ Test IP 172.16.17.163 should be a test machine
⚠️ Do NOT use on production networks
⚠️ Requires administrator privileges
⚠️ Network packets are synthetic test packets only

PERFORMANCE TIPS:
==================
• Start with intensity 1.5x for baseline testing
• Increase intensity gradually (2.0x, 2.5x, 3.0x)
• Run tests for 20-30 seconds duration
• Monitor system resources during tests
• Allow 5-10 seconds between tests

SUCCESS INDICATORS:
===================
✓ Detector window opens with admin privileges
✓ Both windows can run simultaneously
✓ Packets increase when simulator runs
✓ Alerts appear in alert panel
✓ Logs show detection events
✓ Statistics update in real-time
✓ No errors in console output
✓ Can stop/restart both components

For more detailed information, see:
- INTEGRATED_ENVIRONMENT_GUIDE.py
- TARGET_IP_SCANNING_GUIDE.py
"""

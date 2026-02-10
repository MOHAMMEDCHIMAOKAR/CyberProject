"""
TARGET IP SCANNING FEATURE - DETECTOR UPDATE
=============================================

NEW FEATURE DESCRIPTION:
-----------------------
The DoS Detection System now supports scanning a specific target IP address,
allowing you to focus on monitoring traffic to/from a particular host.

USAGE:
------

1. Launch the detector:
   python gui_main.py

2. In the "Controls" section, you'll see a new field:
   
   Target IP (optional): [_________________]
   (Leave empty to monitor all IPs)

3. Enter the IP address you want to monitor:
   Examples:
   - 192.168.1.100
   - 10.0.0.50
   - 127.0.0.1 (localhost)

4. Leave it empty to monitor all IPs (default behavior)

5. Click "Start Monitoring" to begin

FEATURES:
---------
✓ Optional target IP filtering
✓ Automatic IP validation
✓ Focuses detection on specific host
✓ Monitors traffic to/from target IP
✓ Shows target IP in status bar when scanning
✓ Disabled during active monitoring (re-enabled on stop)

EXAMPLES:

Example 1: Monitor localhost for attacks
   Target IP: 127.0.0.1
   - Perfect for testing with dos_simulator.py
   - Run simulator targeting localhost
   - Detector shows only localhost traffic

Example 2: Monitor specific server
   Target IP: 192.168.1.100
   - Focus on one server
   - Ignore other network traffic
   - Reduce false positives

Example 3: Monitor all traffic (default)
   Target IP: (leave empty)
   - Monitors all network traffic
   - Detects attacks on any IP
   - Full network visibility

TECHNICAL IMPLEMENTATION:
------------------------

Changes made:
1. gui_main.py:
   - Added Target IP input field in control panel
   - Added IP validation function (_validate_ip)
   - Updated _start_monitoring to pass target_ip
   - Updated _stop_monitoring to re-enable input

2. gui_detector.py:
   - Added target_ip parameter to start_detection()
   - Added IP filtering in _packet_callback()
   - Only processes packets matching target IP (if specified)
   - Logs target IP in status messages

WORKFLOW:

┌─────────────────────────┐
│  User launches detector  │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ Optionally enters IP    │
│ (e.g., 127.0.0.1)      │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ Clicks Start Monitoring │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ Detector validates IP   │
│ If invalid: show error  │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ Monitoring starts       │
│ Filters packets if IP   │
│ specified              │
└──────────────────────────┘

VALIDATION:
-----------
The detector validates IP addresses before starting:
- Must have 4 octets separated by dots (e.g., 192.168.1.1)
- Each octet must be 0-255
- Shows error dialog if invalid format

BENEFITS:
---------
✓ Reduced noise from other network traffic
✓ Focus detection on specific test targets
✓ Better for isolated testing scenarios
✓ Improved detection accuracy
✓ Easier to analyze specific IP behavior

COMPATIBILITY:
--------------
✓ Works with integrated_environment.py
✓ Works with dos_simulator.py
✓ Backward compatible (optional feature)
✓ No configuration changes needed

TESTING SCENARIO:
-----------------
1. Run integrated_environment.py
2. Click "Start Detector"
3. In detector window:
   - Target IP: 127.0.0.1
   - Click "Start Monitoring"
4. Click "Start Simulator" in integrated environment
5. In simulator:
   - Target IP: 127.0.0.1
   - Attack Type: SYN Flood
   - Click "Start Simulation"
6. Detector monitors only localhost traffic
7. Sees only simulator's test packets
8. Clean, focused detection results

For more information, see gui_main.py and gui_detector.py
"""

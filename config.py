"""
Configuration Management for DoS Detection System
"""

class Config:
    """Central configuration for DoS detection system"""
    
    # Detection Thresholds
    MAX_REQUESTS_PER_SECOND = 100  # Maximum requests per second from single IP
    MAX_CONNECTIONS_PER_IP = 50    # Maximum concurrent connections per IP
    SYN_FLOOD_THRESHOLD = 50       # SYN packets per second threshold
    MIN_PACKET_SIZE = 20           # Minimum normal packet size
    MAX_PACKET_SIZE = 65535        # Maximum packet size
    
    # Time Windows (in seconds)
    TIME_WINDOW = 60               # Time window for rate analysis
    ALERT_COOLDOWN = 60            # Cooldown period between alerts for same IP
    STATS_UPDATE_INTERVAL = 30     # Statistics display interval
    
    # IP Whitelist
    WHITELISTED_IPS = set()        # IPs to ignore (trusted sources)
    
    # Alert Severity Thresholds
    SEVERITY_LOW = 1.2             # 1.0x - 1.2x threshold
    SEVERITY_MEDIUM = 1.5          # 1.2x - 1.5x threshold
    SEVERITY_HIGH = 2.0            # 1.5x - 2.0x threshold
    # CRITICAL is anything above 2.0x
    
    # Feature Toggles
    ENABLE_RATE_DETECTION = True
    ENABLE_CONNECTION_DETECTION = True
    ENABLE_SYN_FLOOD_DETECTION = True
    ENABLE_PACKET_SIZE_DETECTION = True
    
    # Logging
    LOG_FILE = "dos_alerts.log"
    LOG_LEVEL = "INFO"
    
    @classmethod
    def add_whitelist_ip(cls, ip_address):
        """Add IP to whitelist"""
        cls.WHITELISTED_IPS.add(ip_address)
        
    @classmethod
    def remove_whitelist_ip(cls, ip_address):
        """Remove IP from whitelist"""
        cls.WHITELISTED_IPS.discard(ip_address)
        
    @classmethod
    def is_whitelisted(cls, ip_address):
        """Check if IP is whitelisted"""
        return ip_address in cls.WHITELISTED_IPS
        
    @classmethod
    def get_severity(cls, actual, threshold):
        """Calculate severity based on threshold exceedance"""
        if threshold == 0:
            return "CRITICAL"
            
        ratio = actual / threshold
        
        if ratio < cls.SEVERITY_LOW:
            return "LOW"
        elif ratio < cls.SEVERITY_MEDIUM:
            return "MEDIUM"
        elif ratio < cls.SEVERITY_HIGH:
            return "HIGH"
        else:
            return "CRITICAL"

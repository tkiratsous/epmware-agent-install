# Appendix D - Error Codes Reference

Comprehensive reference for EPMware Agent error codes, their meanings, and resolution steps.

## Error Code Format

EPMware Agent errors follow this format:
```
[TIMESTAMP] [LEVEL] [MODULE] Error Code: [CODE] - [Description]
Example: 2023-11-15 10:30:45 ERROR CONNECTION Error Code: CONN-001 - Connection refused
```

## Error Categories

| Code Range | Category | Description |
|------------|----------|-------------|
| **CONN-xxx** | Connection | Network and connectivity errors |
| **AUTH-xxx** | Authentication | Authentication and authorization |
| **CONF-xxx** | Configuration | Configuration file errors |
| **DEPLOY-xxx** | Deployment | Deployment operation errors |
| **APP-xxx** | Application | Target application errors |
| **SYS-xxx** | System | System and resource errors |
| **IO-xxx** | Input/Output | File and I/O operations |
| **SEC-xxx** | Security | Security-related errors |

## Connection Errors (CONN-xxx)

### CONN-001: Connection Refused

**Error Message:**
```
Error Code: CONN-001 - Connection refused: connect
java.net.ConnectException: Connection refused
```

**Cause:** Server is not reachable or not listening on the specified port.

**Resolution:**
```bash
# Check server is running
ping epmware-server.com

# Test port connectivity
telnet epmware-server.com 443

# Verify URL in configuration
grep ew.portal.url agent.properties
```

---

### CONN-002: Connection Timeout

**Error Message:**
```
Error Code: CONN-002 - Connection timed out after 30000ms
java.net.SocketTimeoutException: Read timed out
```

**Cause:** Network latency or firewall blocking connection.

**Resolution:**
```bash
# Increase timeout
echo "agent.connection.timeout=60000" >> agent.properties

# Check firewall
sudo iptables -L -n | grep 443

# Test with curl
curl --connect-timeout 60 https://epmware-server.com
```

---

### CONN-003: Unknown Host

**Error Message:**
```
Error Code: CONN-003 - Unknown host: epmware-server.com
java.net.UnknownHostException: epmware-server.com
```

**Cause:** DNS resolution failure.

**Resolution:**
```bash
# Check DNS
nslookup epmware-server.com

# Add to hosts file temporarily
echo "192.168.1.100 epmware-server.com" >> /etc/hosts

# Use IP instead of hostname
sed -i 's/epmware-server.com/192.168.1.100/' agent.properties
```

---

### CONN-004: SSL Handshake Failed

**Error Message:**
```
Error Code: CONN-004 - SSL handshake failed
javax.net.ssl.SSLHandshakeException: sun.security.validator.ValidatorException
```

**Cause:** Certificate validation failure.

**Resolution:**
```bash
# Import certificate
keytool -import -trustcacerts -keystore $JAVA_HOME/lib/security/cacerts \
        -alias epmware -file epmware.crt -storepass changeit

# Or disable validation (testing only)
java -Dcom.sun.net.ssl.checkRevocation=false -jar epmware-agent.jar
```

---

### CONN-005: Proxy Authentication Required

**Error Message:**
```
Error Code: CONN-005 - Proxy authentication required
HTTP/1.1 407 Proxy Authentication Required
```

**Cause:** Proxy requires authentication.

**Resolution:**
```properties
# Add to agent.properties
http.proxyHost=proxy.company.com
http.proxyPort=8080
http.proxyUser=username
http.proxyPassword=password
```

## Authentication Errors (AUTH-xxx)

### AUTH-001: Invalid Token

**Error Message:**
```
Error Code: AUTH-001 - Invalid authentication token
HTTP 401 Unauthorized
```

**Cause:** Token is invalid, expired, or malformed.

**Resolution:**
1. Generate new token in EPMware
2. Update agent.properties:
```bash
sed -i 's/ew.portal.token=.*/ew.portal.token=NEW-TOKEN/' agent.properties
```
3. Restart agent

---

### AUTH-002: Token Expired

**Error Message:**
```
Error Code: AUTH-002 - Authentication token has expired
```

**Cause:** Token has exceeded its validity period.

**Resolution:**
1. Log into EPMware
2. Navigate to Users → Generate Token
3. Update configuration with new token
4. Implement token rotation schedule

---

### AUTH-003: Insufficient Permissions

**Error Message:**
```
Error Code: AUTH-003 - User does not have required permissions
HTTP 403 Forbidden
```

**Cause:** User lacks necessary permissions for operation.

**Resolution:**
```bash
# Verify user permissions in EPMware
# Grant required roles:
# - Deployment Execute
# - API Access
# - Application Access
```

---

### AUTH-004: Account Locked

**Error Message:**
```
Error Code: AUTH-004 - User account is locked
```

**Cause:** Account locked due to failed attempts or security policy.

**Resolution:**
1. Unlock account in EPMware admin
2. Reset password if required
3. Generate new token

## Configuration Errors (CONF-xxx)

### CONF-001: Missing Configuration File

**Error Message:**
```
Error Code: CONF-001 - Configuration file not found: agent.properties
java.io.FileNotFoundException: agent.properties
```

**Cause:** agent.properties file is missing.

**Resolution:**
```bash
# Create from template
cp agent.properties.template agent.properties

# Or create new
cat > agent.properties << EOF
ew.portal.server=servername
ew.portal.url=https://url
ew.portal.token=token
agent.interval.millisecond=30000
agent.root.dir=/home/user
EOF
```

---

### CONF-002: Invalid Property Format

**Error Message:**
```
Error Code: CONF-002 - Invalid property format in configuration
```

**Cause:** Syntax error in properties file.

**Resolution:**
```bash
# Check syntax
grep -E "^[^#].*=" agent.properties

# Look for common issues:
# - Missing equals sign
# - Spaces in property names
# - Unclosed quotes
```

---

### CONF-003: Missing Required Property

**Error Message:**
```
Error Code: CONF-003 - Required property missing: ew.portal.url
```

**Cause:** Essential configuration property not set.

**Resolution:**
```bash
# Check all required properties
for prop in ew.portal.server ew.portal.url ew.portal.token; do
    grep "^$prop=" agent.properties || echo "Add: $prop=value"
done
```

---

### CONF-004: Invalid Path Format

**Error Message:**
```
Error Code: CONF-004 - Invalid path format: C:cygwin64homeuser
```

**Cause:** Incorrect path separator or format.

**Resolution:**
```properties
# Windows - use double backslashes
agent.root.dir=C:\\\\cygwin64\\\\home\\\\user

# Or forward slashes
agent.root.dir=C:/cygwin64/home/user

# Linux
agent.root.dir=/home/user
```

## Deployment Errors (DEPLOY-xxx)

### DEPLOY-001: Deployment Failed

**Error Message:**
```
Error Code: DEPLOY-001 - Deployment failed for application HFM_PROD
```

**Cause:** General deployment failure.

**Resolution:**
```bash
# Check application status
# Verify credentials
# Review deployment logs
tail -100 logs/agent.log | grep -i deploy

# Test connection to application
java -jar epmware-agent.jar --test-app HFM_PROD
```

---

### DEPLOY-002: Target Application Unavailable

**Error Message:**
```
Error Code: DEPLOY-002 - Target application HFM_PROD is not available
```

**Cause:** Application is down or not accessible.

**Resolution:**
```bash
# Check application status
systemctl status hfm  # Linux service

# Test application connection
telnet hfm-server 19000

# Verify application URL/credentials
```

---

### DEPLOY-003: Invalid Metadata Format

**Error Message:**
```
Error Code: DEPLOY-003 - Invalid metadata format in deployment package
```

**Cause:** Metadata file is corrupted or wrong format.

**Resolution:**
1. Validate metadata file format
2. Check for XML/CSV errors
3. Verify character encoding (UTF-8)
4. Regenerate metadata package

---

### DEPLOY-004: Deployment Timeout

**Error Message:**
```
Error Code: DEPLOY-004 - Deployment operation timed out after 3600 seconds
```

**Cause:** Deployment taking longer than timeout limit.

**Resolution:**
```properties
# Increase timeout in agent.properties
deployment.timeout=7200000  # 2 hours

# Or for specific application
hfm.deployment.timeout=7200000
```

## Application Errors (APP-xxx)

### APP-001: HFM Registry Not Found

**Error Message:**
```
Error Code: APP-001 - HFM registry properties file not found
```

**Cause:** reg.properties not in correct location.

**Resolution:**
```bash
# Copy registry file
cp $MIDDLEWARE/user_projects/config/foundation/11.1.2.0/reg.properties \
   $MIDDLEWARE/user_projects/epmsystem1/config/foundation/11.1.2.0/
```

---

### APP-002: Planning Password File Error

**Error Message:**
```
Error Code: APP-002 - Cannot read Planning password file
```

**Cause:** Password file missing or corrupted.

**Resolution:**
```bash
# Generate new password file
cd $PLANNING_HOME
./PasswordEncryption.sh password_file.txt

# Update EPMware configuration with file path
```

---

### APP-003: EPM Automate Not Found

**Error Message:**
```
Error Code: APP-003 - EPM Automate utility not found
```

**Cause:** EPM Automate not installed for cloud operations.

**Resolution:**
```bash
# Install EPM Automate
tar xf EPMAutomate.tar
export PATH=$PATH:~/epmautomate/bin

# Test
epmautomate --version
```

---

### APP-004: Application Login Failed

**Error Message:**
```
Error Code: APP-004 - Login failed for application user
```

**Cause:** Invalid application credentials.

**Resolution:**
1. Verify username and password
2. Check account isn't locked
3. Verify user has required application roles
4. Test login manually

## System Errors (SYS-xxx)

### SYS-001: Out of Memory

**Error Message:**
```
Error Code: SYS-001 - Out of memory error
java.lang.OutOfMemoryError: Java heap space
```

**Cause:** Insufficient heap memory allocated.

**Resolution:**
```bash
# Increase heap size in ew_target_service.sh
JAVA_OPTS="-Xms1024m -Xmx2048m"

# Or set in environment
export _JAVA_OPTIONS="-Xmx2g"
```

---

### SYS-002: Disk Space Exhausted

**Error Message:**
```
Error Code: SYS-002 - No space left on device
java.io.IOException: No space left on device
```

**Cause:** Disk is full.

**Resolution:**
```bash
# Check disk usage
df -h

# Clean up logs
find logs/ -name "*.log" -mtime +30 -delete
find temp/ -type f -delete

# Archive and compress old files
gzip logs/*.log.old
```

---

### SYS-003: Too Many Open Files

**Error Message:**
```
Error Code: SYS-003 - Too many open files
java.io.IOException: Too many open files
```

**Cause:** File descriptor limit reached.

**Resolution:**
```bash
# Increase limit (Linux)
ulimit -n 65536

# Permanent change
echo "* soft nofile 65536" >> /etc/security/limits.conf
echo "* hard nofile 65536" >> /etc/security/limits.conf
```

---

### SYS-004: Process Already Running

**Error Message:**
```
Error Code: SYS-004 - Agent process already running with PID: 12345
```

**Cause:** Another agent instance is running.

**Resolution:**
```bash
# Check running processes
ps aux | grep epmware-agent

# Kill existing process
kill -15 <PID>

# Remove PID file
rm agent.pid
```

## I/O Errors (IO-xxx)

### IO-001: File Not Found

**Error Message:**
```
Error Code: IO-001 - File not found: /path/to/file
java.io.FileNotFoundException
```

**Cause:** Required file is missing.

**Resolution:**
```bash
# Check file exists
ls -la /path/to/file

# Check permissions
# Create if missing
touch /path/to/file
```

---

### IO-002: Permission Denied

**Error Message:**
```
Error Code: IO-002 - Permission denied: /path/to/file
java.io.IOException: Permission denied
```

**Cause:** Insufficient file permissions.

**Resolution:**
```bash
# Fix permissions
chmod 644 /path/to/file
chown epmware_agent:epmware_agent /path/to/file

# Check directory permissions
chmod 755 /path/to/
```

---

### IO-003: File Lock Error

**Error Message:**
```
Error Code: IO-003 - File is locked by another process
```

**Cause:** File is being used by another process.

**Resolution:**
```bash
# Find process using file
lsof /path/to/file

# Remove lock file if stale
rm /path/to/file.lock
```

## Security Errors (SEC-xxx)

### SEC-001: Certificate Expired

**Error Message:**
```
Error Code: SEC-001 - SSL certificate has expired
```

**Cause:** Server certificate is expired.

**Resolution:**
1. Request certificate renewal
2. Import new certificate:
```bash
keytool -import -alias epmware -file new-cert.crt \
        -keystore $JAVA_HOME/lib/security/cacerts
```

---

### SEC-002: Cipher Suite Mismatch

**Error Message:**
```
Error Code: SEC-002 - No cipher suites in common
```

**Cause:** TLS cipher suite incompatibility.

**Resolution:**
```properties
# Enable additional ciphers
https.cipherSuites=TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384,TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256
```

---

### SEC-003: TLS Version Mismatch

**Error Message:**
```
Error Code: SEC-003 - TLS version not supported
```

**Cause:** TLS version incompatibility.

**Resolution:**
```bash
# Enable TLS 1.2 and 1.3
JAVA_OPTS="-Dhttps.protocols=TLSv1.2,TLSv1.3"
```

## Error Resolution Scripts

### Comprehensive Error Checker

```bash
#!/bin/bash
# error_checker.sh - Diagnose common errors

echo "=== EPMware Agent Error Diagnosis ==="

# Check configuration
if [ ! -f agent.properties ]; then
    echo "ERROR: CONF-001 - agent.properties not found"
fi

# Check Java
if ! command -v java &> /dev/null; then
    echo "ERROR: SYS-005 - Java not found"
fi

# Check connectivity
if ! ping -c 1 epmware-server.com &> /dev/null; then
    echo "ERROR: CONN-001 - Cannot reach server"
fi

# Check disk space
DISK_USAGE=$(df . | tail -1 | awk '{print $5}' | sed 's/%//')
if [ $DISK_USAGE -gt 90 ]; then
    echo "WARNING: SYS-002 - Disk usage at ${DISK_USAGE}%"
fi

# Check for errors in logs
if [ -f logs/agent.log ]; then
    echo "=== Recent Errors ==="
    grep "Error Code:" logs/agent.log | tail -10
fi
```

### Error Recovery Script

```bash
#!/bin/bash
# recover_from_error.sh - Automated error recovery

ERROR_CODE=$1

case $ERROR_CODE in
    CONN-001)
        echo "Attempting to recover from connection error..."
        # Restart network
        sudo systemctl restart network
        ;;
    
    AUTH-001)
        echo "Token error - please regenerate token"
        echo "Update agent.properties with new token"
        ;;
    
    SYS-001)
        echo "Memory error - restarting with more heap"
        pkill -f epmware-agent
        java -Xmx4096m -jar epmware-agent.jar &
        ;;
    
    SYS-002)
        echo "Disk space error - cleaning up..."
        find logs/ -name "*.log" -mtime +7 -delete
        find temp/ -type f -delete
        ;;
    
    *)
        echo "Unknown error code: $ERROR_CODE"
        echo "Check documentation for resolution"
        ;;
esac
```

## Error Monitoring

### Error Alert Configuration

```bash
#!/bin/bash
# error_monitor.sh - Monitor and alert on errors

LOG_FILE="logs/agent.log"
ERROR_THRESHOLD=5
ALERT_EMAIL="admin@company.com"

# Count recent errors (last hour)
ERROR_COUNT=$(find $LOG_FILE -mmin -60 -exec grep -c "Error Code:" {} \;)

if [ $ERROR_COUNT -gt $ERROR_THRESHOLD ]; then
    # Send alert
    echo "High error rate detected: $ERROR_COUNT errors in last hour" | \
        mail -s "EPMware Agent Error Alert" $ALERT_EMAIL
    
    # Extract error details
    grep "Error Code:" $LOG_FILE | tail -20 | \
        mail -s "EPMware Agent Error Details" $ALERT_EMAIL
fi
```

## Error Prevention Best Practices

### Proactive Error Prevention

1. **Regular Health Checks**
   - Monitor logs continuously
   - Check resource usage
   - Verify connectivity regularly

2. **Configuration Validation**
   - Test changes before production
   - Validate properties syntax
   - Backup configurations

3. **Resource Management**
   - Monitor disk space
   - Set appropriate heap size
   - Implement log rotation

4. **Security Maintenance**
   - Keep certificates updated
   - Rotate tokens regularly
   - Apply security patches

### Error Documentation Template

```markdown
## Error Report

**Error Code:** CONN-001
**Date/Time:** 2023-11-15 10:30:45
**Severity:** HIGH
**Environment:** Production

**Error Message:**
Connection refused: connect

**Root Cause:**
Firewall rule changed blocking port 443

**Resolution:**
1. Identified firewall change
2. Updated firewall rule
3. Tested connectivity
4. Restarted agent

**Prevention:**
- Add firewall rules to change control
- Implement connection monitoring
- Document network requirements

**Time to Resolution:** 45 minutes
```

!!! tip "Error Pattern Recognition"
    Keep a log of recurring errors and their solutions. This helps identify systemic issues and speeds up resolution time.

!!! warning "Critical Errors"
    Errors marked as FATAL or CRITICAL should trigger immediate alerts and may require emergency response procedures.

## Next Steps

- [Port Requirements](ports.md) - Network configuration
- [Security Checklist](security.md) - Security setup
- [Agent Commands](commands.md) - Command reference
- [Return to Appendices](index.md) - Main appendices page
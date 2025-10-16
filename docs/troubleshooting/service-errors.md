# Service Errors

This guide covers common service errors encountered with EPMware Agent, including diagnostic procedures and resolution steps.

## Common Service Errors

### Connection Errors

#### Error: Connection Refused

**Symptoms:**
```
ERROR: Connection refused to epmware-server.com:443
java.net.ConnectException: Connection refused
```

**Causes:**
- EPMware server is down
- Firewall blocking connection
- Incorrect server URL or port
- Network connectivity issues

**Resolution:**

1. **Verify server is accessible:**
   ```bash
   # Test connectivity
   ping epmware-server.com
   
   # Test port
   telnet epmware-server.com 443
   
   # Test with curl
   curl -I https://epmware-server.com
   ```

2. **Check firewall rules:**
   ```bash
   # Linux
   sudo iptables -L | grep 443
   
   # Windows
   netsh advfirewall firewall show rule name=all | findstr 443
   ```

3. **Verify agent configuration:**
   ```bash
   grep "ew.portal.url" agent.properties
   ```

4. **Test from different network location:**
   ```bash
   # Use traceroute to identify network issues
   traceroute epmware-server.com
   ```

#### Error: Connection Timeout

**Symptoms:**
```
ERROR: Connection timeout after 30000ms
java.net.SocketTimeoutException: Read timed out
```

**Resolution:**

1. **Increase timeout in agent.properties:**
   ```properties
   agent.connection.timeout=60000
   agent.read.timeout=60000
   ```

2. **Check for proxy requirements:**
   ```bash
   # Set proxy if needed
   export HTTP_PROXY=http://proxy.company.com:8080
   export HTTPS_PROXY=http://proxy.company.com:8080
   ```

3. **Optimize network route:**
   ```bash
   # Check network latency
   ping -c 100 epmware-server.com | grep avg
   ```

### Authentication Errors

#### Error: 401 Unauthorized

**Symptoms:**
```
ERROR: HTTP 401 Unauthorized
Authentication failed: Invalid token
```

**Resolution:**

1. **Verify token is correct:**
   ```bash
   # Check token in config
   grep "ew.portal.token" agent.properties
   
   # Ensure no extra spaces or characters
   cat agent.properties | od -c | grep token
   ```

2. **Regenerate token:**
   - Log into EPMware
   - Navigate to Security → Users
   - Generate new token for agent user
   - Update agent.properties

3. **Check user permissions:**
   - Verify agent user is active
   - Confirm user has required roles
   - Check no IP restrictions

#### Error: 403 Forbidden

**Symptoms:**
```
ERROR: HTTP 403 Forbidden
Access denied to resource
```

**Resolution:**

1. **Verify user permissions in EPMware:**
   - Agent user needs appropriate security class
   - Check application access rights
   - Verify server configuration access

2. **Check SSL certificate issues:**
   ```bash
   # Test SSL connection
   openssl s_client -connect epmware-server.com:443
   ```

### Java/JVM Errors

#### Error: OutOfMemoryError

**Symptoms:**
```
Exception in thread "main" java.lang.OutOfMemoryError: Java heap space
```

**Resolution:**

1. **Increase heap size in ew_target_service.sh:**
   ```bash
   # Original
   java -jar epmware-agent.jar --spring.config.name=agent
   
   # Modified with increased memory
   java -Xms512m -Xmx2g -jar epmware-agent.jar --spring.config.name=agent
   ```

2. **Monitor memory usage:**
   ```bash
   # Check current usage
   jstat -gc $(pgrep -f epmware-agent)
   
   # Generate heap dump for analysis
   jmap -dump:format=b,file=heap.bin $(pgrep -f epmware-agent)
   ```

#### Error: ClassNotFoundException

**Symptoms:**
```
java.lang.ClassNotFoundException: com.epmware.agent.Main
```

**Resolution:**

1. **Verify JAR file integrity:**
   ```bash
   # Check JAR is not corrupted
   jar tf epmware-agent.jar | grep Main
   
   # Verify checksum if provided
   sha256sum epmware-agent.jar
   ```

2. **Check Java classpath:**
   ```bash
   # Ensure all required JARs are present
   ls -la *.jar
   
   # Verify Java version compatibility
   java -version
   ```

### File System Errors

#### Error: Permission Denied

**Symptoms:**
```
ERROR: Permission denied: /home/user/logs/agent.log
java.io.FileNotFoundException: Permission denied
```

**Resolution:**

1. **Fix file permissions:**
   ```bash
   # Check current permissions
   ls -la logs/
   
   # Fix permissions
   chmod 755 logs
   chmod 644 logs/*.log
   
   # Fix ownership
   chown -R agent_user:agent_group ~/
   ```

2. **Check SELinux (Linux):**
   ```bash
   # Check if SELinux is blocking
   getenforce
   
   # Temporarily disable to test
   sudo setenforce 0
   
   # Add permanent exception if needed
   sudo semanage fcontext -a -t user_home_t "/home/agent(/.*)?"
   sudo restorecon -Rv /home/agent
   ```

#### Error: No Space Left on Device

**Symptoms:**
```
ERROR: No space left on device
java.io.IOException: No space left on device
```

**Resolution:**

1. **Check disk space:**
   ```bash
   # Check overall disk usage
   df -h
   
   # Find large files
   du -sh /* | sort -hr | head -20
   
   # Check agent logs size
   du -sh logs/
   ```

2. **Clean up logs:**
   ```bash
   # Archive old logs
   tar -czf logs-$(date +%Y%m%d).tar.gz logs/*.log
   
   # Remove old logs
   find logs/ -name "*.log" -mtime +30 -delete
   ```

3. **Implement log rotation:**
   ```bash
   # Add to crontab
   0 0 * * * find /home/agent/logs -name "*.log" -mtime +7 -delete
   ```

### Service Management Errors

#### Error: Service Fails to Start

**Symptoms:**
- Scheduled task shows "Failed"
- systemd service won't start
- No process created

**Resolution:**

1. **Check for existing process:**
   ```bash
   # Linux
   ps -ef | grep epmware-agent
   
   # Windows
   Get-Process java | Where {$_.CommandLine -like "*epmware*"}
   ```

2. **Review system logs:**
   ```bash
   # Linux systemd
   journalctl -xe | grep epmware
   
   # Windows Event Log
   Get-EventLog -LogName Application -Source "EPMware*"
   ```

3. **Verify prerequisites:**
   ```bash
   # Check Java
   java -version
   
   # Check required files
   ls -la ew_target_service.sh epmware-agent.jar agent.properties
   ```

#### Error: Service Keeps Restarting

**Symptoms:**
- Service restarts every few minutes
- Multiple PIDs in short time
- Logs show repeated startup attempts

**Resolution:**

1. **Check restart configuration:**
   ```ini
   # systemd - Increase restart delay
   RestartSec=60
   StartLimitBurst=3
   StartLimitIntervalSec=300
   ```

2. **Investigate crash cause:**
   ```bash
   # Check for core dumps
   find / -name "core.*" 2>/dev/null
   
   # Review error logs
   grep -E "ERROR|FATAL|Exception" logs/agent.log
   ```

### Application-Specific Errors

#### Error: EPMLCM-13000 (Planning)

**Symptoms:**
```
EPMLCM-13000: Service currently not available
```

**Resolution:**

1. **Verify Planning application provisioning:**
   - Check user is provisioned to Planning application
   - Verify application is running
   - Test with EPM Automate or Workspace

2. **Check Planning services:**
   ```bash
   # On Planning server
   ./startPlanning.sh status
   ```

#### Error: HFM Registry Not Found

**Symptoms:**
```
ERROR: Cannot find reg.properties file
HFM import/deployment fails
```

**Resolution:**

1. **Copy reg.properties to correct location:**
   ```cmd
   copy D:\Oracle\Middleware\user_projects\config\foundation\11.1.2.0\reg.properties ^
        D:\Oracle\Middleware\user_projects\epmsystem1\config\foundation\11.1.2.0\
   ```

2. **Verify file permissions:**
   ```cmd
   icacls D:\Oracle\Middleware\user_projects\epmsystem1\config\foundation\11.1.2.0\reg.properties
   ```

## Error Diagnosis Tools

### Log Analysis Script

Create a script to analyze agent logs for errors:

**analyze-errors.sh:**
```bash
#!/bin/bash

LOG_DIR="logs"
REPORT_FILE="error-report-$(date +%Y%m%d).txt"

echo "EPMware Agent Error Analysis Report" > $REPORT_FILE
echo "Generated: $(date)" >> $REPORT_FILE
echo "==========================================" >> $REPORT_FILE
echo >> $REPORT_FILE

# Count errors by type
echo "Error Summary:" >> $REPORT_FILE
echo "--------------" >> $REPORT_FILE
grep -h ERROR $LOG_DIR/*.log | cut -d' ' -f5- | sort | uniq -c | sort -rn | head -20 >> $REPORT_FILE

echo >> $REPORT_FILE
echo "Recent Errors (Last 24 hours):" >> $REPORT_FILE
echo "-------------------------------" >> $REPORT_FILE
find $LOG_DIR -name "*.log" -mtime -1 -exec grep ERROR {} \; | tail -20 >> $REPORT_FILE

echo >> $REPORT_FILE
echo "Connection Issues:" >> $REPORT_FILE
echo "------------------" >> $REPORT_FILE
grep -h "Connection\|Timeout\|refused" $LOG_DIR/*.log | tail -10 >> $REPORT_FILE

echo >> $REPORT_FILE
echo "Memory Issues:" >> $REPORT_FILE
echo "--------------" >> $REPORT_FILE
grep -h "OutOfMemory\|heap" $LOG_DIR/*.log | tail -10 >> $REPORT_FILE

echo "Report saved to: $REPORT_FILE"
cat $REPORT_FILE
```

### Health Check Script

**health-check.sh:**
```bash
#!/bin/bash

echo "=== EPMware Agent Health Check ==="
echo

# Check 1: Process Running
echo -n "Agent Process: "
if pgrep -f epmware-agent > /dev/null; then
    echo "✓ Running (PID: $(pgrep -f epmware-agent))"
else
    echo "✗ Not Running"
fi

# Check 2: Recent Polls
echo -n "Recent Polls: "
LAST_POLL=$(tail -1 logs/agent-poll.log 2>/dev/null | awk '{print $1, $2}')
if [ -n "$LAST_POLL" ]; then
    echo "✓ Last poll: $LAST_POLL"
else
    echo "✗ No recent polls"
fi

# Check 3: Error Count
echo -n "Recent Errors: "
ERROR_COUNT=$(find logs -name "*.log" -mmin -60 -exec grep ERROR {} \; 2>/dev/null | wc -l)
if [ $ERROR_COUNT -eq 0 ]; then
    echo "✓ No errors in last hour"
else
    echo "⚠ $ERROR_COUNT errors in last hour"
fi

# Check 4: Disk Space
echo -n "Disk Space: "
DISK_USE=$(df -h . | tail -1 | awk '{print $5}' | sed 's/%//')
if [ $DISK_USE -lt 80 ]; then
    echo "✓ ${DISK_USE}% used"
else
    echo "⚠ ${DISK_USE}% used (cleanup recommended)"
fi

# Check 5: Memory Usage
echo -n "Memory Usage: "
if pgrep -f epmware-agent > /dev/null; then
    MEM=$(ps aux | grep epmware-agent | grep -v grep | awk '{print $4}')
    echo "✓ ${MEM}% of system memory"
fi

echo
echo "=== Health Check Complete ==="
```

## Recovery Procedures

### Emergency Restart Procedure

1. **Kill all agent processes:**
   ```bash
   pkill -9 -f epmware-agent
   ```

2. **Clean up temporary files:**
   ```bash
   rm -f /tmp/epmware-*
   rm -f ~/agent.pid
   ```

3. **Archive problematic logs:**
   ```bash
   mkdir -p logs/archive
   mv logs/*.log logs/archive/
   ```

4. **Start with debug mode:**
   ```bash
   export AGENT_DEBUG=true
   ./ew_target_service.sh
   ```

### Rollback Procedure

If new agent version causes issues:

1. **Stop current agent**
2. **Backup current configuration:**
   ```bash
   cp agent.properties agent.properties.backup
   ```
3. **Restore previous version:**
   ```bash
   cp epmware-agent-old.jar epmware-agent.jar
   ```
4. **Restart agent**
5. **Monitor for stability**

## Monitoring for Errors

### Automated Error Detection

Set up automated monitoring for critical errors:

```bash
#!/bin/bash
# monitor-errors.sh - Run via cron every 5 minutes

CRITICAL_PATTERNS="OutOfMemory|Connection refused|Authentication failed|FATAL"
ALERT_EMAIL="admin@company.com"

# Check for critical errors
ERRORS=$(grep -E "$CRITICAL_PATTERNS" logs/agent.log | tail -5)

if [ -n "$ERRORS" ]; then
    echo "$ERRORS" | mail -s "EPMware Agent Critical Error on $(hostname)" $ALERT_EMAIL
fi
```

## Best Practices

1. **Implement comprehensive logging** at appropriate levels
2. **Set up proactive monitoring** for common errors
3. **Document error patterns** specific to your environment
4. **Create runbooks** for common error scenarios
5. **Test recovery procedures** regularly
6. **Maintain error knowledge base** for your team
7. **Review logs regularly** even when no issues are reported

## Related Topics

- [Debug Mode](debug.md)
- [Password Issues](passwords.md)
- [Agent Logs](../management/logs.md)
- [Monitoring](../management/monitoring.md)
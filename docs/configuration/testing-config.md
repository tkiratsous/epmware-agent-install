# Testing Agent Connection

## Overview

After configuring the EPMware Agent, it's crucial to test the connection to ensure proper communication between the agent and EPMware application. This guide covers various testing methods and troubleshooting steps.

## Prerequisites

Before testing, ensure:

- [ ] Agent files are properly extracted
- [ ] `agent.properties` is configured with correct values
- [ ] REST API token is generated and added to configuration
- [ ] Java is installed and accessible
- [ ] Network connectivity to EPMware server exists

## Basic Connection Test

### Method 1: Command Line Test

The simplest way to test the agent connection:

```bash
# Navigate to agent directory
cd /home/[username]

# Run the agent in test mode
java -jar epmware-agent.jar --test
```

Expected output:
```
Testing connection to EPMware...
Server: epmware1.epmware.com
URL: https://client.epmwarecloud.com
Token: [VALID]
Connection: SUCCESS
Agent version: 1.7.0
Server version: 2023.4
```

### Method 2: Service Script Test

Test using the service script:

```bash
# Make script executable
chmod +x ew_target_service.sh

# Run the service script
./ew_target_service.sh
```

Expected output:
```
Starting EPMware Agent...
Loading configuration from agent.properties
Connecting to https://client.epmwarecloud.com
Authentication successful
Starting polling cycle (interval: 30000ms)
Polling for tasks...
No pending tasks
```

![Agent Polling Output](../assets/images/configuration/agent-polling-output.png)<br/>
*Successful agent polling output*

### Method 3: EPMware UI Test

Test from the EPMware application:

1. Log into EPMware
2. Navigate to **Infrastructure** → **Servers**
3. Right-click on the configured server
4. Select **Test Connection**

![Test Connection UI](../assets/images/configuration/test-connection-ui.png)<br/>
*Testing connection from EPMware UI*

Expected result:
- Green checkmark indicating successful connection
- Response time displayed
- "Connection successful" message

## Advanced Testing

### Verbose Mode Testing

Enable detailed output for troubleshooting:

```bash
# Run with debug logging
java -Dagent.log.level=DEBUG -jar epmware-agent.jar --test

# Or modify agent.properties temporarily
echo "agent.log.level=DEBUG" >> agent.properties
./ew_target_service.sh
```

### Network Connectivity Test

Test basic network connectivity:

```bash
# Test DNS resolution
nslookup epmware1.epmware.com
ping epmware1.epmware.com

# Test HTTPS connectivity
curl -I https://client.epmwarecloud.com

# Test with token
curl -H "Authorization: Bearer YOUR-TOKEN-HERE" \
     https://client.epmwarecloud.com/api/v1/agent/health
```

### Port Connectivity Test

Verify required ports are open:

```bash
# Test HTTPS port (443)
telnet client.epmwarecloud.com 443

# Or using nc (netcat)
nc -zv client.epmwarecloud.com 443

# Or using PowerShell (Windows)
Test-NetConnection -ComputerName client.epmwarecloud.com -Port 443
```

## Testing Deployment Functionality

### Create Test Deployment

1. In EPMware, create a simple test request
2. Approve the request through workflow
3. Monitor agent logs for deployment activity

```bash
# Watch agent logs
tail -f logs/agent.log

# In another terminal, check polling
tail -f logs/agent-poll.log
```

### Deployment Test Output

Expected log entries:
```
2023-11-15 14:30:00 INFO  Polling for tasks...
2023-11-15 14:30:01 INFO  Retrieved 1 deployment task(s)
2023-11-15 14:30:02 INFO  Starting deployment: DEP-001
2023-11-15 14:30:03 INFO  Target: HFM_PROD
2023-11-15 14:30:04 INFO  Loading metadata file...
2023-11-15 14:30:10 INFO  Deployment completed successfully
2023-11-15 14:30:11 INFO  Reporting status to EPMware
```

## Common Test Failures

### Authentication Failures

**Symptom:**
```
ERROR: Authentication failed - Invalid token
```

**Solutions:**
1. Verify token in agent.properties:
```bash
grep ew.portal.token agent.properties
```

2. Regenerate token in EPMware:
   - Navigate to Users
   - Right-click → Generate Token
   - Update agent.properties

3. Check token format:
```bash
# Token should be 36 characters with hyphens
echo "2e6d4103-5145-4c30-9837-ac6d14797523" | wc -c
# Should output 37 (36 + newline)
```

### Connection Timeouts

**Symptom:**
```
ERROR: Connection timeout after 30000ms
```

**Solutions:**
1. Check network connectivity:
```bash
ping -c 4 epmware-server.com
traceroute epmware-server.com
```

2. Verify firewall rules:
```bash
# Linux
sudo iptables -L -n | grep 443

# Windows
netsh advfirewall firewall show rule name=all | find "443"
```

3. Test with increased timeout:
```properties
# In agent.properties
agent.connection.timeout=60000
```

### Certificate Issues

**Symptom:**
```
ERROR: SSL/TLS certificate validation failed
```

**Solutions:**
1. Import certificate to Java truststore:
```bash
# Export certificate
openssl s_client -connect epmware-server.com:443 </dev/null | \
  openssl x509 -outform PEM > epmware.crt

# Import to Java
keytool -import -alias epmware -keystore $JAVA_HOME/lib/security/cacerts \
  -file epmware.crt -storepass changeit
```

2. Temporarily disable validation (not for production):
```bash
java -Dcom.sun.net.ssl.checkRevocation=false \
     -Dtrust.all.certificates=true \
     -jar epmware-agent.jar --test
```

## Performance Testing

### Response Time Measurement

Test agent response times:

```bash
# Simple response time test
time curl -H "Authorization: Bearer TOKEN" \
     https://epmware-server.com/api/v1/agent/health

# Multiple iterations
for i in {1..10}; do
  time curl -s -H "Authorization: Bearer TOKEN" \
    https://epmware-server.com/api/v1/agent/health > /dev/null
done
```

### Load Testing

Simulate multiple deployments:

```bash
# Create test script
cat > test_load.sh << 'EOF'
#!/bin/bash
for i in {1..5}; do
  echo "Test deployment $i"
  # Trigger test deployment
  sleep 2
done
EOF

chmod +x test_load.sh
./test_load.sh
```

## Test Validation Checklist

### Initial Connection

- [ ] Agent starts without errors
- [ ] Authentication successful
- [ ] Polling begins at configured interval
- [ ] No errors in agent.log
- [ ] Server shows as "Connected" in EPMware

### Deployment Capability

- [ ] Agent receives deployment tasks
- [ ] Can access target application
- [ ] Successfully deploys metadata
- [ ] Reports status back to EPMware
- [ ] Logs show successful completion

### Error Handling

- [ ] Agent recovers from network interruptions
- [ ] Handles invalid tasks gracefully
- [ ] Logs errors appropriately
- [ ] Continues polling after errors

## Testing Different Configurations

### Test with Proxy

If using a proxy server:

```bash
# Set proxy environment variables
export HTTP_PROXY=http://proxy.company.com:8080
export HTTPS_PROXY=http://proxy.company.com:8080
export NO_PROXY=localhost,127.0.0.1

# Test connection
java -Dhttp.proxyHost=proxy.company.com \
     -Dhttp.proxyPort=8080 \
     -Dhttps.proxyHost=proxy.company.com \
     -Dhttps.proxyPort=8080 \
     -jar epmware-agent.jar --test
```

### Test with Different Polling Intervals

```bash
# Quick test with 10-second interval
sed -i.bak 's/agent.interval.millisecond=30000/agent.interval.millisecond=10000/' agent.properties
./ew_target_service.sh

# Monitor rapid polling
tail -f logs/agent-poll.log
```

!!! warning "Production Settings"
    Remember to restore production polling interval after testing.

## Monitoring Tools

### Log Analysis

Monitor logs in real-time:

```bash
# Combined log monitoring
tail -f logs/*.log | grep -E "ERROR|WARN|SUCCESS"

# Specific pattern monitoring
tail -f logs/agent.log | grep "deployment"

# Count errors
grep -c ERROR logs/agent.log
```

### Health Check Script

Create a monitoring script:

```bash
#!/bin/bash
# health_check.sh

echo "=== EPMware Agent Health Check ==="
echo "Date: $(date)"

# Check if agent is running
if pgrep -f "epmware-agent.jar" > /dev/null; then
    echo "✓ Agent process is running"
else
    echo "✗ Agent process is NOT running"
fi

# Check last poll time
LAST_POLL=$(tail -1 logs/agent-poll.log | cut -d' ' -f1-2)
echo "Last poll: $LAST_POLL"

# Check for recent errors
ERROR_COUNT=$(tail -100 logs/agent.log | grep -c ERROR)
echo "Recent errors: $ERROR_COUNT"

# Test connection
if java -jar epmware-agent.jar --test > /dev/null 2>&1; then
    echo "✓ Connection test passed"
else
    echo "✗ Connection test failed"
fi
```

## Test Documentation

### Recording Test Results

Document your test results:

```markdown
# Agent Testing Report

## Environment
- Server: servername
- Date: 2023-11-15
- Agent Version: 1.7.0
- Java Version: 1.8.0_291

## Test Results
| Test | Result | Notes |
|------|--------|-------|
| Basic Connection | ✓ Pass | Connected in 200ms |
| Authentication | ✓ Pass | Token validated |
| Polling | ✓ Pass | 30-second interval working |
| Deployment | ✓ Pass | Test deployment successful |
| Error Recovery | ✓ Pass | Recovered from network interruption |

## Issues Found
- None

## Recommendations
- Continue to production deployment
```

## Troubleshooting Resources

### Log Locations

Check these logs for issues:

| Log File | Contents |
|----------|----------|
| `logs/agent.log` | Main agent activity and errors |
| `logs/agent-poll.log` | Polling activity |
| `/var/log/messages` (Linux) | System-level issues |
| Windows Event Viewer | Windows service issues |

### Debug Commands

Useful commands for troubleshooting:

```bash
# Check Java version
java -version

# Verify environment variables
env | grep -E "JAVA|PATH"

# Check process
ps -ef | grep epmware

# Network diagnostics
netstat -an | grep ESTABLISHED

# Disk space
df -h /home/[username]
```

## Next Steps

After successful testing:

1. [Schedule the Agent](../management/windows/scheduled-tasks.md) - Set up automatic startup
2. [Configure Applications](../integration/index.md) - Set up target applications
3. [Monitor Operations](../management/monitoring.md) - Implement monitoring
4. [Review Troubleshooting](../troubleshooting/index.md) - Prepare for issues
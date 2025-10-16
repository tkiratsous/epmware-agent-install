# Debug Mode

Debug mode provides detailed logging and diagnostic information for troubleshooting complex issues with the EPMware Agent. This guide covers enabling debug mode, interpreting debug output, and using debug information effectively.

## Enabling Debug Mode

### Method 1: Configuration File

Add debug settings to `agent.properties`:

```properties
# Enable debug logging
agent.log.level=DEBUG
agent.debug.enabled=true

# Optional: Enable specific debug categories
agent.debug.connection=true
agent.debug.commands=true
agent.debug.deployment=true
agent.debug.authentication=true
```

### Method 2: Environment Variable

Set environment variable before starting agent:

**Linux:**
```bash
export AGENT_DEBUG=true
export AGENT_LOG_LEVEL=DEBUG
./ew_target_service.sh
```

**Windows (PowerShell):**
```powershell
$env:AGENT_DEBUG = "true"
$env:AGENT_LOG_LEVEL = "DEBUG"
.\ew_target_service.bat
```

### Method 3: JVM Arguments

Modify the startup script to include debug flags:

```bash
# In ew_target_service.sh
java -Dagent.debug=true \
     -Dlog.level=DEBUG \
     -Xdebug \
     -Xrunjdwp:transport=dt_socket,server=y,suspend=n,address=5005 \
     -jar epmware-agent.jar --spring.config.name=agent
```

## Debug Output Levels

### Log Levels Explained

| Level | Description | Use Case |
|-------|-------------|----------|
| **ERROR** | Critical failures only | Production normal operation |
| **WARN** | Warnings and errors | Production monitoring |
| **INFO** | Standard operational logs | Default level |
| **DEBUG** | Detailed diagnostic info | Troubleshooting |
| **TRACE** | Maximum verbosity | Deep debugging |

### Sample Debug Output

```log
2023-11-15 10:30:45.123 DEBUG [main] c.e.agent.AgentMain - Starting EPMware Agent v2.5.0
2023-11-15 10:30:45.234 DEBUG [main] c.e.agent.config.Config - Loading configuration from: agent.properties
2023-11-15 10:30:45.345 DEBUG [main] c.e.agent.config.Config - Configuration loaded:
  - Portal URL: https://epmware.company.com
  - Server Name: HFM-PROD-01
  - Poll Interval: 30000ms
  - Debug Mode: ENABLED
2023-11-15 10:30:45.456 DEBUG [pool-1] c.e.agent.connection.Client - Initializing HTTP client
2023-11-15 10:30:45.567 DEBUG [pool-1] c.e.agent.connection.Client - Setting connection timeout: 30000ms
2023-11-15 10:30:45.678 DEBUG [pool-1] c.e.agent.auth.TokenAuth - Using token authentication
2023-11-15 10:30:45.789 TRACE [pool-1] c.e.agent.auth.TokenAuth - Token: 2e6d4103-5145-4c30-9837-ac6d14797523
2023-11-15 10:30:46.890 DEBUG [pool-1] c.e.agent.connection.Client - Connecting to: https://epmware.company.com/api/agent/poll
2023-11-15 10:30:47.123 DEBUG [pool-1] c.e.agent.connection.Client - Response: 200 OK
2023-11-15 10:30:47.234 DEBUG [pool-2] c.e.agent.commands.CommandProcessor - Received command: DEPLOY
2023-11-15 10:30:47.345 DEBUG [pool-2] c.e.agent.commands.Deploy - Deployment parameters:
  - Application: HFM_PROD
  - Request ID: 12345
  - Action: METADATA_DEPLOY
```

## Debug Categories

### Connection Debugging

Enable to troubleshoot network and connectivity issues:

```properties
agent.debug.connection=true
agent.debug.connection.verbose=true
```

**Debug output includes:**
- Connection attempts and retries
- URL construction
- Request/response headers
- SSL handshake details
- Proxy configuration
- Timeout occurrences

**Sample connection debug:**
```log
DEBUG [connection] Attempting connection to: epmware.company.com:443
DEBUG [connection] Proxy configured: proxy.company.com:8080
DEBUG [connection] SSL Protocol: TLSv1.2
DEBUG [connection] Cipher Suite: TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384
DEBUG [connection] Certificate chain validated successfully
DEBUG [connection] Connection established in 245ms
```

### Command Debugging

Enable to see detailed command processing:

```properties
agent.debug.commands=true
agent.debug.commands.show.output=true
```

**Debug output includes:**
- Command construction
- Parameter substitution
- Shell execution details
- Output capture
- Exit codes

**Sample command debug:**
```log
DEBUG [command] Executing command: importmetadata.bat
DEBUG [command] Working directory: D:\Oracle\EPM\bin
DEBUG [command] Environment variables:
  - ORACLE_HOME=D:\Oracle\Middleware
  - EPM_ORACLE_INSTANCE=D:\Oracle\Middleware\user_projects\epmsystem1
DEBUG [command] Command arguments:
  - -application "HFM_PROD"
  - -metadatafile "D:\temp\metadata_20231115.xml"
DEBUG [command] Process started: PID=5678
DEBUG [command] Command output:
  Loading metadata...
  Processing dimensions...
  Validation complete
  Import successful
DEBUG [command] Exit code: 0
DEBUG [command] Execution time: 45.2 seconds
```

### Deployment Debugging

Enable for detailed deployment troubleshooting:

```properties
agent.debug.deployment=true
agent.debug.deployment.show.files=true
```

**Debug output includes:**
- File transfers
- Deployment staging
- Validation steps
- Rollback procedures

### Authentication Debugging

Enable to troubleshoot authentication issues:

```properties
agent.debug.authentication=true
# WARNING: This may log sensitive information
agent.debug.authentication.show.tokens=false
```

## Interactive Debug Mode

### Starting Interactive Debug

Start agent with interactive console:

```bash
# Linux
./ew_target_service.sh --interactive --debug

# Windows
ew_target_service.bat /interactive /debug
```

### Interactive Commands

Once in interactive mode, use these commands:

| Command | Description |
|---------|-------------|
| `status` | Show current agent status |
| `config` | Display configuration |
| `test-connection` | Test EPMware server connection |
| `test-deploy [app]` | Simulate deployment to application |
| `show-logs [n]` | Display last n log entries |
| `set-level [level]` | Change log level dynamically |
| `threads` | Show active threads |
| `memory` | Display memory usage |
| `help` | Show all available commands |
| `quit` | Exit interactive mode |

## Remote Debugging

### Enable JVM Remote Debugging

Configure agent for remote debugging with IDE:

```bash
# In ew_target_service.sh
java -agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:5005 \
     -jar epmware-agent.jar --spring.config.name=agent
```

### Connect with IDE

**IntelliJ IDEA:**
1. Run → Edit Configurations
2. Add → Remote JVM Debug
3. Host: agent-server.company.com
4. Port: 5005
5. Click Debug

**Eclipse:**
1. Run → Debug Configurations
2. Remote Java Application → New
3. Host: agent-server.company.com
4. Port: 5005
5. Click Debug

**Visual Studio Code:**
```json
// .vscode/launch.json
{
  "type": "java",
  "name": "Debug EPMware Agent",
  "request": "attach",
  "hostName": "agent-server.company.com",
  "port": 5005
}
```

## Debug Output Analysis

### Using grep for Debug Analysis

Common debug analysis commands:

```bash
# Find all DEBUG entries
grep DEBUG agent.log

# Find connection issues
grep -E "DEBUG.*connection|timeout|refused" agent.log

# Find command executions
grep "DEBUG.*command.*Executing" agent.log

# Find errors with context
grep -B5 -A5 ERROR agent.log

# Track specific request
grep "Request ID: 12345" agent.log
```

### Debug Log Rotation

Debug mode generates large log files. Configure rotation:

```properties
# In agent.properties
agent.log.max.size=100MB
agent.log.max.files=10
agent.log.compress=true
```

### Performance Impact

Debug mode impacts performance. Monitor:

```bash
# Check CPU usage
top -p $(pgrep -f epmware-agent)

# Check memory
ps aux | grep epmware-agent | awk '{print $4}'

# Check disk I/O
iotop -p $(pgrep -f epmware-agent)
```

## Debug Scripts and Tools

### Debug Information Collector

Create a script to collect debug information:

**collect-debug.sh:**
```bash
#!/bin/bash

DEBUG_DIR="debug-$(date +%Y%m%d-%H%M%S)"
mkdir -p $DEBUG_DIR

echo "Collecting debug information..."

# Agent configuration
cp agent.properties $DEBUG_DIR/

# Recent logs
cp logs/agent*.log $DEBUG_DIR/

# System information
echo "=== System Information ===" > $DEBUG_DIR/system-info.txt
uname -a >> $DEBUG_DIR/system-info.txt
echo "" >> $DEBUG_DIR/system-info.txt
echo "=== Java Version ===" >> $DEBUG_DIR/system-info.txt
java -version 2>> $DEBUG_DIR/system-info.txt
echo "" >> $DEBUG_DIR/system-info.txt
echo "=== Memory ===" >> $DEBUG_DIR/system-info.txt
free -h >> $DEBUG_DIR/system-info.txt
echo "" >> $DEBUG_DIR/system-info.txt
echo "=== Disk Space ===" >> $DEBUG_DIR/system-info.txt
df -h >> $DEBUG_DIR/system-info.txt
echo "" >> $DEBUG_DIR/system-info.txt
echo "=== Network ===" >> $DEBUG_DIR/system-info.txt
netstat -an | grep ESTABLISHED >> $DEBUG_DIR/system-info.txt

# Process information
if pgrep -f epmware-agent > /dev/null; then
    echo "=== Agent Process ===" > $DEBUG_DIR/process-info.txt
    ps aux | grep epmware-agent | grep -v grep >> $DEBUG_DIR/process-info.txt
    echo "" >> $DEBUG_DIR/process-info.txt
    echo "=== Thread Dump ===" >> $DEBUG_DIR/process-info.txt
    jstack $(pgrep -f epmware-agent) >> $DEBUG_DIR/process-info.txt 2>&1
    echo "" >> $DEBUG_DIR/process-info.txt
    echo "=== Heap Info ===" >> $DEBUG_DIR/process-info.txt
    jmap -heap $(pgrep -f epmware-agent) >> $DEBUG_DIR/process-info.txt 2>&1
fi

# Recent errors
echo "=== Recent Errors ===" > $DEBUG_DIR/recent-errors.txt
grep ERROR logs/agent.log | tail -100 >> $DEBUG_DIR/recent-errors.txt

# Create archive
tar -czf $DEBUG_DIR.tar.gz $DEBUG_DIR/
rm -rf $DEBUG_DIR/

echo "Debug information collected: $DEBUG_DIR.tar.gz"
echo "Send this file to EPMware support for analysis"
```

### Real-time Debug Monitor

Create a script for real-time debug monitoring:

**monitor-debug.sh:**
```bash
#!/bin/bash

# Colors for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

clear
echo "EPMware Agent Debug Monitor"
echo "==========================="
echo "Press Ctrl+C to exit"
echo

tail -f logs/agent.log | while read line; do
    if echo "$line" | grep -q ERROR; then
        echo -e "${RED}$line${NC}"
    elif echo "$line" | grep -q WARN; then
        echo -e "${YELLOW}$line${NC}"
    elif echo "$line" | grep -q DEBUG; then
        echo -e "${GREEN}$line${NC}"
    else
        echo "$line"
    fi
done
```

## Debug Best Practices

### When to Use Debug Mode

✅ **Use debug mode for:**
- Initial agent setup and configuration
- Troubleshooting connection issues
- Investigating deployment failures
- Performance analysis
- Integration testing
- Reproducing reported issues

❌ **Avoid debug mode in:**
- Production environments (unless necessary)
- High-load scenarios
- Limited disk space situations
- Security-sensitive environments

### Debug Mode Checklist

Before enabling debug mode:

- [ ] Ensure sufficient disk space (at least 5GB free)
- [ ] Notify team about debug activation
- [ ] Document the issue being investigated
- [ ] Set up log rotation/cleanup
- [ ] Plan debug duration (don't leave on indefinitely)
- [ ] Have rollback plan ready

After debug session:

- [ ] Disable debug mode
- [ ] Archive debug logs
- [ ] Document findings
- [ ] Clean up large log files
- [ ] Restore normal configuration
- [ ] Verify normal operation

### Security Considerations

⚠️ **Debug mode may log sensitive information:**

- Authentication tokens
- Passwords in command lines
- User data
- System paths
- Network topology

**Secure debug practices:**

1. **Limit access to debug logs:**
   ```bash
   chmod 600 logs/agent-debug.log
   ```

2. **Sanitize logs before sharing:**
   ```bash
   sed -i 's/token=.*/token=REDACTED/g' debug.log
   sed -i 's/password=.*/password=REDACTED/g' debug.log
   ```

3. **Use secure transfer for debug files:**
   ```bash
   # Encrypt before sending
   gpg -c debug-info.tar.gz
   ```

## Troubleshooting Debug Mode

### Debug Mode Not Working

If debug output isn't appearing:

1. **Verify configuration:**
   ```bash
   grep -i debug agent.properties
   ```

2. **Check log file permissions:**
   ```bash
   ls -la logs/
   ```

3. **Confirm Java system properties:**
   ```bash
   jinfo $(pgrep -f epmware-agent) | grep debug
   ```

4. **Test with explicit debug:**
   ```bash
   java -Dagent.debug=true -Dlog.level=DEBUG -jar epmware-agent.jar --spring.config.name=agent
   ```

### Excessive Debug Output

If debug logs are too verbose:

1. **Adjust specific categories:**
   ```properties
   agent.debug.connection=false
   agent.debug.polling=false
   ```

2. **Use grep to filter:**
   ```bash
   tail -f agent.log | grep -v "poll"
   ```

3. **Increase log level:**
   ```properties
   agent.log.level=INFO
   ```

## Related Topics

- [Service Errors](service-errors.md)
- [Agent Logs](../management/logs.md)
- [Password Issues](passwords.md)
- [Monitoring](../management/monitoring.md)
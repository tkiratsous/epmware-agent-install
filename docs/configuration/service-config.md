# Service Configuration

## Overview

The `ew_target_service.sh` script is the primary mechanism for starting and managing the EPMware Agent. This guide covers configuration options, customization, and platform-specific setup.

## Understanding the Service Script

### Default Script Content

The default `ew_target_service.sh` contains:

```bash
#!/bin/bash
#mvn spring-boot:run
HOME=/home/Administrator
cd $HOME
#java -jar epmware-agent.jar --spring.config.name=agent > /dev/null 2>&1
java -jar epmware-agent.jar --spring.config.name=agent
```

### Script Components

| Component | Purpose | Customizable |
|-----------|---------|--------------|
| `#!/bin/bash` | Shell interpreter | No |
| `HOME=/home/Administrator` | Working directory | Yes - Must match installation |
| `cd $HOME` | Change to agent directory | No |
| `java -jar` command | Start the agent | Yes - Add JVM options |

## Basic Configuration

### Setting the HOME Directory

The HOME variable must match your installation directory:

**Windows (Cygwin):**
```bash
HOME=/home/Administrator  # Default
# Or for custom user
HOME=/home/hfmsvcaccount
```

**Linux:**
```bash
HOME=/home/epmadmin
# Or
HOME=/opt/epmware/agent
```

### Verification

```bash
# Verify path exists
ls -la /home/Administrator

# Test script modification
./ew_target_service.sh
```

## Advanced Configuration

### JVM Memory Settings

Configure memory allocation for the agent:

```bash
#!/bin/bash
HOME=/home/Administrator
cd $HOME

# Memory configuration
JAVA_OPTS="-Xms512m -Xmx2048m"
JAVA_OPTS="$JAVA_OPTS -XX:MaxMetaspaceSize=256m"

java $JAVA_OPTS -jar epmware-agent.jar --spring.config.name=agent
```

### Memory Recommendations

| Environment | Heap Min (-Xms) | Heap Max (-Xmx) | Metaspace |
|-------------|-----------------|-----------------|-----------|
| Development | 256m | 512m | 128m |
| Test | 512m | 1024m | 256m |
| Production | 1024m | 2048m | 512m |
| Large Scale | 2048m | 4096m | 1024m |

### Logging Configuration

Control logging output and location:

```bash
#!/bin/bash
HOME=/home/Administrator
cd $HOME

# Logging configuration
LOG_DIR="$HOME/logs"
LOG_FILE="$LOG_DIR/agent.log"

# Ensure log directory exists
mkdir -p $LOG_DIR

# Start with logging options
java -Dlogging.file.name=$LOG_FILE \
     -Dlogging.level.root=INFO \
     -Dlogging.level.com.epmware=DEBUG \
     -jar epmware-agent.jar --spring.config.name=agent
```

### Environment Variables

Set environment-specific variables:

```bash
#!/bin/bash
HOME=/home/Administrator
cd $HOME

# Environment variables
export EPMWARE_ENV=production
export AGENT_ID=agent01
export TZ=America/New_York

# Java settings
export JAVA_HOME=/usr/java/jdk1.8.0_291
export PATH=$JAVA_HOME/bin:$PATH

# Agent settings
AGENT_OPTS="--spring.profiles.active=$EPMWARE_ENV"
AGENT_OPTS="$AGENT_OPTS --agent.id=$AGENT_ID"

java -jar epmware-agent.jar --spring.config.name=agent $AGENT_OPTS
```

## Platform-Specific Configuration

### Windows Service Script

Enhanced script for Windows (Cygwin):

```bash
#!/bin/bash
# ew_target_service.sh - Windows version

# Configuration
HOME=/home/Administrator
JAVA_CMD="/cygdrive/c/Program Files/Java/jdk1.8.0_291/bin/java"
AGENT_JAR="epmware-agent.jar"
PID_FILE="$HOME/agent.pid"

# Change to home directory
cd $HOME

# Check if already running
if [ -f "$PID_FILE" ]; then
    PID=$(cat $PID_FILE)
    if ps -p $PID > /dev/null 2>&1; then
        echo "Agent already running with PID: $PID"
        exit 1
    fi
fi

# Start agent and save PID
"$JAVA_CMD" -jar $AGENT_JAR --spring.config.name=agent &
echo $! > $PID_FILE
echo "Agent started with PID: $(cat $PID_FILE)"
```

### Linux Service Script

Enhanced script for Linux with systemd integration:

```bash
#!/bin/bash
# ew_target_service.sh - Linux version

# Configuration
HOME=/home/epmadmin
JAVA_CMD=$(which java)
AGENT_JAR="epmware-agent.jar"
PID_FILE="/var/run/epmware-agent.pid"
LOG_FILE="/var/log/epmware/agent.log"

# Ensure directories exist
mkdir -p $(dirname $LOG_FILE)
mkdir -p $(dirname $PID_FILE)

# Change to home directory
cd $HOME

# Function to start agent
start_agent() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat $PID_FILE)
        if ps -p $PID > /dev/null 2>&1; then
            echo "Agent already running with PID: $PID"
            return 1
        fi
    fi
    
    nohup $JAVA_CMD -jar $AGENT_JAR --spring.config.name=agent \
          > $LOG_FILE 2>&1 &
    echo $! > $PID_FILE
    echo "Agent started with PID: $(cat $PID_FILE)"
}

# Function to stop agent
stop_agent() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat $PID_FILE)
        kill $PID
        rm -f $PID_FILE
        echo "Agent stopped"
    else
        echo "Agent not running"
    fi
}

# Main logic
case "$1" in
    start)
        start_agent
        ;;
    stop)
        stop_agent
        ;;
    restart)
        stop_agent
        sleep 2
        start_agent
        ;;
    *)
        echo "Usage: $0 {start|stop|restart}"
        exit 1
        ;;
esac
```

## Output Management

### Redirecting Output

Control where agent output goes:

```bash
# Discard all output (silent mode)
java -jar epmware-agent.jar --spring.config.name=agent > /dev/null 2>&1

# Log to file
java -jar epmware-agent.jar --spring.config.name=agent > agent.out 2>&1

# Separate stdout and stderr
java -jar epmware-agent.jar --spring.config.name=agent \
     > stdout.log 2> stderr.log

# Append to existing log
java -jar epmware-agent.jar --spring.config.name=agent >> agent.log 2>&1
```

### Log Rotation

Implement log rotation:

```bash
#!/bin/bash
HOME=/home/Administrator
cd $HOME

# Log rotation settings
LOG_FILE="logs/agent-console.log"
MAX_SIZE=104857600  # 100MB
BACKUP_COUNT=5

# Check log size and rotate if needed
if [ -f "$LOG_FILE" ]; then
    SIZE=$(stat -c%s "$LOG_FILE")
    if [ $SIZE -gt $MAX_SIZE ]; then
        for i in $(seq $((BACKUP_COUNT-1)) -1 1); do
            [ -f "$LOG_FILE.$i" ] && mv "$LOG_FILE.$i" "$LOG_FILE.$((i+1))"
        done
        mv "$LOG_FILE" "$LOG_FILE.1"
    fi
fi

# Start agent with logging
java -jar epmware-agent.jar --spring.config.name=agent >> $LOG_FILE 2>&1
```

## Error Handling

### Basic Error Handling

Add error checking to the script:

```bash
#!/bin/bash
set -e  # Exit on error

HOME=/home/Administrator
cd $HOME || exit 1

# Check Java availability
if ! command -v java &> /dev/null; then
    echo "ERROR: Java not found in PATH"
    exit 1
fi

# Check JAR file exists
if [ ! -f "epmware-agent.jar" ]; then
    echo "ERROR: epmware-agent.jar not found"
    exit 1
fi

# Check properties file exists
if [ ! -f "agent.properties" ]; then
    echo "ERROR: agent.properties not found"
    exit 1
fi

# Start agent
java -jar epmware-agent.jar --spring.config.name=agent || {
    echo "ERROR: Failed to start agent"
    exit 1
}
```

### Retry Logic

Implement automatic retry on failure:

```bash
#!/bin/bash
HOME=/home/Administrator
cd $HOME

MAX_RETRIES=3
RETRY_DELAY=10
RETRY_COUNT=0

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    echo "Starting agent (attempt $((RETRY_COUNT + 1))/$MAX_RETRIES)..."
    
    java -jar epmware-agent.jar --spring.config.name=agent
    EXIT_CODE=$?
    
    if [ $EXIT_CODE -eq 0 ]; then
        echo "Agent terminated normally"
        break
    else
        echo "Agent failed with exit code $EXIT_CODE"
        RETRY_COUNT=$((RETRY_COUNT + 1))
        
        if [ $RETRY_COUNT -lt $MAX_RETRIES ]; then
            echo "Retrying in $RETRY_DELAY seconds..."
            sleep $RETRY_DELAY
        else
            echo "Maximum retries reached. Giving up."
            exit 1
        fi
    fi
done
```

## Performance Tuning

### JVM Options

Optimize JVM performance:

```bash
#!/bin/bash
HOME=/home/Administrator
cd $HOME

# Performance tuning options
JVM_OPTS="-server"                           # Server mode
JVM_OPTS="$JVM_OPTS -Xms1024m"              # Initial heap
JVM_OPTS="$JVM_OPTS -Xmx2048m"              # Maximum heap
JVM_OPTS="$JVM_OPTS -XX:+UseG1GC"           # G1 garbage collector
JVM_OPTS="$JVM_OPTS -XX:MaxGCPauseMillis=200"  # GC pause target
JVM_OPTS="$JVM_OPTS -XX:+HeapDumpOnOutOfMemoryError"  # Heap dump on OOM
JVM_OPTS="$JVM_OPTS -XX:HeapDumpPath=$HOME/logs"      # Heap dump location

java $JVM_OPTS -jar epmware-agent.jar --spring.config.name=agent
```

### Network Optimization

Configure network settings:

```bash
# Network tuning
NET_OPTS="-Djava.net.preferIPv4Stack=true"
NET_OPTS="$NET_OPTS -Dsun.net.client.defaultConnectTimeout=30000"
NET_OPTS="$NET_OPTS -Dsun.net.client.defaultReadTimeout=30000"

java $NET_OPTS -jar epmware-agent.jar --spring.config.name=agent
```

## Security Configuration

### Running with Limited Privileges

Use sudo for specific operations:

```bash
#!/bin/bash
HOME=/home/epmadmin
cd $HOME

# Drop privileges after binding to ports
RUNAS_USER=epmware
RUNAS_GROUP=epmware

# Start as root, then switch user
sudo -u $RUNAS_USER -g $RUNAS_GROUP \
    java -jar epmware-agent.jar --spring.config.name=agent
```

### Secure Environment Variables

Protect sensitive information:

```bash
#!/bin/bash
HOME=/home/Administrator
cd $HOME

# Load secure environment
if [ -f "$HOME/.env.secure" ]; then
    # Ensure file has restricted permissions
    chmod 600 $HOME/.env.secure
    source $HOME/.env.secure
fi

# Use environment variables for sensitive data
java -Dew.portal.token="$EPMWARE_TOKEN" \
     -jar epmware-agent.jar --spring.config.name=agent
```

## Multi-Instance Configuration

### Running Multiple Agents

Configure script for multiple instances:

```bash
#!/bin/bash
# Multi-instance service script

INSTANCE=$1
if [ -z "$INSTANCE" ]; then
    echo "Usage: $0 <instance_name>"
    exit 1
fi

# Instance-specific configuration
BASE_DIR=/opt/epmware
INSTANCE_DIR=$BASE_DIR/$INSTANCE
CONFIG_FILE=$INSTANCE_DIR/agent.properties
PID_FILE=$INSTANCE_DIR/agent.pid

cd $INSTANCE_DIR

java -Dspring.config.location=$CONFIG_FILE \
     -Dagent.instance=$INSTANCE \
     -jar $BASE_DIR/epmware-agent.jar
```

## Monitoring Integration

### Health Check Endpoint

Add health monitoring:

```bash
#!/bin/bash
HOME=/home/Administrator
cd $HOME

# Enable health endpoint
HEALTH_OPTS="-Dmanagement.endpoint.health.enabled=true"
HEALTH_OPTS="$HEALTH_OPTS -Dmanagement.server.port=8081"

java $HEALTH_OPTS -jar epmware-agent.jar --spring.config.name=agent &

# Save PID for monitoring
echo $! > agent.pid

# Wait and check health
sleep 10
curl -s http://localhost:8081/actuator/health
```

## Troubleshooting Service Issues

### Common Problems

| Issue | Cause | Solution |
|-------|-------|----------|
| Script not executable | Missing execute permission | `chmod +x ew_target_service.sh` |
| Wrong HOME directory | Path doesn't match installation | Update HOME variable |
| Java not found | PATH not set correctly | Add Java to PATH or use full path |
| Permission denied | Insufficient privileges | Check file ownership and permissions |

### Debug Mode

Enable detailed debugging:

```bash
#!/bin/bash
set -x  # Enable debug output

HOME=/home/Administrator
cd $HOME

# Debug environment
echo "Current user: $(whoami)"
echo "Current directory: $(pwd)"
echo "Java version: $(java -version 2>&1)"
echo "Files in directory: $(ls -la)"

# Start with debug logging
java -Dagent.debug=true \
     -Dlogging.level.root=DEBUG \
     -jar epmware-agent.jar --spring.config.name=agent
```

## Best Practices

### Script Maintenance

1. **Version Control** - Keep script in version control
2. **Documentation** - Comment all customizations
3. **Backup** - Keep original script backup
4. **Testing** - Test changes in non-production first

### Security Recommendations

1. **Restrict Permissions** - `chmod 750 ew_target_service.sh`
2. **Validate Input** - Check all variables
3. **Limit Privileges** - Run with minimum required permissions
4. **Audit Changes** - Log all script modifications

## Next Steps

After configuring the service script:

1. [Test the Connection](testing.md) - Verify agent connectivity
2. [Schedule the Service](../management/windows/scheduled-tasks.md) - Set up automatic startup
3. [Monitor Agent Logs](../management/logs.md) - Review logging output
4. [Configure Applications](../integration/index.md) - Set up target integrations
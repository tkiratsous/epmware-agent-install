# Start and Stop Procedures

This guide provides comprehensive procedures for starting and stopping the EPMware Agent on both Linux and Windows servers.

## Linux Server Procedures

### Starting the Agent on Linux

#### Method 1: Direct Execution

Log in as the user under which the agent is installed:

```bash
cd /home/[username]
./ew_target_service.sh &
```

The `&` symbol runs the process in the background.

#### Method 2: Using nohup

For persistent execution after logout:

```bash
cd /home/[username]
nohup ./ew_target_service.sh > agent-startup.log 2>&1 &
echo $! > agent.pid
```

#### Method 3: Using systemd (Recommended)

If configured as a systemd service:

```bash
sudo systemctl start epmware-agent

# Verify startup
sudo systemctl status epmware-agent
```

#### Method 4: Using init.d

For systems with init.d configuration:

```bash
sudo service epmware-agent start

# Or directly
sudo /etc/init.d/epmware-agent start
```

### Stopping the Agent on Linux

#### Method 1: Using Process ID

Find and terminate the agent process:

```bash
# Find the process
ps -ef | grep -i epmware-agent | grep $(whoami) | grep -v grep

# Note the process ID (second column), then kill it
kill -9 [process_id]

# Or in one command
kill -9 $(ps -ef | grep -i epmware-agent | grep $(whoami) | grep -v grep | awk '{print $2}')
```

#### Method 2: Using Saved PID File

If you saved the PID during startup:

```bash
# Kill using saved PID
kill -9 $(cat agent.pid)

# Remove PID file
rm agent.pid
```

#### Method 3: Using systemd

```bash
sudo systemctl stop epmware-agent

# Verify shutdown
sudo systemctl status epmware-agent
```

#### Method 4: Using init.d

```bash
sudo service epmware-agent stop

# Or directly
sudo /etc/init.d/epmware-agent stop
```

### Restarting the Agent on Linux

#### Quick Restart

```bash
# Find and kill existing process
kill -9 $(pgrep -f epmware-agent)

# Wait for process to terminate
sleep 5

# Start new instance
cd /home/[username]
nohup ./ew_target_service.sh > agent.log 2>&1 &
```

#### Using Service Manager

```bash
# systemd
sudo systemctl restart epmware-agent

# init.d
sudo service epmware-agent restart
```

## Windows Server Procedures

### Starting the Agent on Windows

#### Method 1: Using Task Scheduler (Recommended)

1. Open Windows Task Scheduler
2. Locate the task "EPMWARE TARGET AGENT SERVICE"
3. Check the Status column:
   - If "Ready", right-click and select **Run**
   - If "Running", the agent is already active

![Start Agent via Task Scheduler](../../assets/images/management/task-scheduler-start.png)

#### Method 2: Using Command Line

Open Command Prompt as Administrator:

```cmd
# Start the scheduled task
schtasks /Run /TN "EPMWARE TARGET AGENT SERVICE"
```

#### Method 3: Using Cygwin Terminal

```bash
# Navigate to agent directory
cd /home/Administrator

# Start the service
./ew_target_service.sh
```

### Stopping the Agent on Windows

#### Method 1: Using Task Manager

1. Open Windows Task Manager (Ctrl+Shift+Esc)
2. Go to the **Details** tab
3. Find **java.exe** process
4. Check the Command Line column for "epmware-agent.jar"
5. Right-click the process and select **End Task**

![Stop Agent via Task Manager](../../assets/images/management/task-manager-stop.png)

#### Method 2: Using PowerShell

Run PowerShell as Administrator:

```powershell
# Find and stop the agent process
Get-Process java | Where-Object {$_.CommandLine -like "*epmware-agent.jar*"} | Stop-Process -Force
```

#### Method 3: Using Command Prompt

```cmd
# Find the process
wmic process where "commandline like '%epmware-agent.jar%'" get processid

# Kill the process (replace PID with actual process ID)
taskkill /F /PID [PID]
```

#### Method 4: Stop Scheduled Task

```cmd
# Stop the scheduled task (doesn't kill the Java process)
schtasks /End /TN "EPMWARE TARGET AGENT SERVICE"
```

!!! warning "Important"
    Stopping the scheduled task does NOT automatically terminate the Java process. You must manually kill the Java process before restarting the agent.

### Restarting the Agent on Windows

Complete restart procedure:

```powershell
# 1. Kill existing Java process
Get-Process java | Where-Object {$_.CommandLine -like "*epmware-agent.jar*"} | Stop-Process -Force

# 2. Wait for process to terminate
Start-Sleep -Seconds 5

# 3. Optional: Clean up old log files
Remove-Item "C:\cygwin64\home\Administrator\logs\agent*.log" -Force

# 4. Start the scheduled task
schtasks /Run /TN "EPMWARE TARGET AGENT SERVICE"
```

## Verification Procedures

### Verify Agent is Running

#### Linux

```bash
# Check process
ps -ef | grep -i epmware-agent | grep -v grep

# Check latest log entries
tail -f ~/logs/agent-poll.log

# Check service status (if using systemd)
systemctl status epmware-agent
```

#### Windows

```powershell
# Check process
Get-Process java | Where-Object {$_.CommandLine -like "*epmware-agent.jar*"}

# Check scheduled task status
schtasks /Query /TN "EPMWARE TARGET AGENT SERVICE" /V

# Check latest log entries
Get-Content "C:\cygwin64\home\Administrator\logs\agent-poll.log" -Tail 10 -Wait
```

### Verify Agent Connectivity

After starting the agent, verify it's communicating with EPMware:

1. **Check poll log for recent entries:**
   ```bash
   tail -10 logs/agent-poll.log
   ```
   Should show entries every 30 seconds (or configured interval)

2. **Check main log for errors:**
   ```bash
   grep ERROR logs/agent.log | tail -10
   ```

3. **Test from EPMware UI:**
   - Navigate to Infrastructure → Servers
   - Right-click the server
   - Select "Test Connection"

## Automated Start/Stop Scripts

### Linux Automation Script

Create `agent-control.sh`:

```bash
#!/bin/bash

AGENT_HOME="/home/[username]"
PIDFILE="$AGENT_HOME/agent.pid"
LOGFILE="$AGENT_HOME/logs/agent.log"

start() {
    if [ -f $PIDFILE ] && ps -p $(cat $PIDFILE) > /dev/null 2>&1; then
        echo "Agent already running (PID: $(cat $PIDFILE))"
        return 1
    fi
    
    echo "Starting EPMware Agent..."
    cd $AGENT_HOME
    nohup ./ew_target_service.sh > $LOGFILE 2>&1 &
    echo $! > $PIDFILE
    echo "Agent started (PID: $(cat $PIDFILE))"
}

stop() {
    if [ ! -f $PIDFILE ]; then
        echo "Agent is not running (no PID file)"
        return 1
    fi
    
    PID=$(cat $PIDFILE)
    echo "Stopping EPMware Agent (PID: $PID)..."
    kill -9 $PID
    rm -f $PIDFILE
    echo "Agent stopped"
}

restart() {
    stop
    sleep 5
    start
}

status() {
    if [ -f $PIDFILE ] && ps -p $(cat $PIDFILE) > /dev/null 2>&1; then
        echo "Agent is running (PID: $(cat $PIDFILE))"
    else
        echo "Agent is not running"
    fi
}

case "$1" in
    start|stop|restart|status)
        $1
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status}"
        exit 1
        ;;
esac
```

### Windows Automation Script

Create `Agent-Control.ps1`:

```powershell
param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("Start","Stop","Restart","Status")]
    [string]$Action
)

$AgentPath = "C:\cygwin64\home\Administrator"
$TaskName = "EPMWARE TARGET AGENT SERVICE"

function Start-Agent {
    $process = Get-Process java -ErrorAction SilentlyContinue | 
        Where-Object {$_.CommandLine -like "*epmware-agent.jar*"}
    
    if ($process) {
        Write-Host "Agent already running (PID: $($process.Id))" -ForegroundColor Yellow
        return
    }
    
    Write-Host "Starting EPMware Agent..." -ForegroundColor Green
    Start-ScheduledTask -TaskName $TaskName
    Start-Sleep -Seconds 3
    
    $process = Get-Process java -ErrorAction SilentlyContinue | 
        Where-Object {$_.CommandLine -like "*epmware-agent.jar*"}
    
    if ($process) {
        Write-Host "Agent started successfully (PID: $($process.Id))" -ForegroundColor Green
    } else {
        Write-Host "Failed to start agent" -ForegroundColor Red
    }
}

function Stop-Agent {
    $process = Get-Process java -ErrorAction SilentlyContinue | 
        Where-Object {$_.CommandLine -like "*epmware-agent.jar*"}
    
    if (-not $process) {
        Write-Host "Agent is not running" -ForegroundColor Yellow
        return
    }
    
    Write-Host "Stopping EPMware Agent (PID: $($process.Id))..." -ForegroundColor Yellow
    $process | Stop-Process -Force
    Write-Host "Agent stopped" -ForegroundColor Green
}

function Restart-Agent {
    Stop-Agent
    Start-Sleep -Seconds 5
    Start-Agent
}

function Get-AgentStatus {
    $process = Get-Process java -ErrorAction SilentlyContinue | 
        Where-Object {$_.CommandLine -like "*epmware-agent.jar*"}
    
    if ($process) {
        Write-Host "Agent is running" -ForegroundColor Green
        Write-Host "  PID: $($process.Id)"
        Write-Host "  CPU: $($process.CPU)"
        Write-Host "  Memory: $([math]::Round($process.WS/1MB, 2)) MB"
    } else {
        Write-Host "Agent is not running" -ForegroundColor Red
    }
    
    $task = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
    if ($task) {
        Write-Host "Scheduled Task Status: $($task.State)"
    }
}

# Execute requested action
switch ($Action) {
    "Start"   { Start-Agent }
    "Stop"    { Stop-Agent }
    "Restart" { Restart-Agent }
    "Status"  { Get-AgentStatus }
}
```

## Troubleshooting Start/Stop Issues

### Agent Won't Start

1. **Check Java installation:**
   ```bash
   java -version
   ```

2. **Verify file permissions:**
   ```bash
   ls -la ew_target_service.sh
   chmod +x ew_target_service.sh
   ```

3. **Check configuration:**
   ```bash
   cat agent.properties
   ```

4. **Review error logs:**
   ```bash
   tail -100 logs/agent.log
   ```

### Agent Won't Stop

1. **Force kill if necessary:**
   ```bash
   kill -9 $(pgrep -f epmware-agent)
   ```

2. **Check for zombie processes:**
   ```bash
   ps aux | grep defunct
   ```

3. **Clear stale PID files:**
   ```bash
   rm -f agent.pid
   ```

### Agent Starts but Immediately Stops

1. Check for port conflicts
2. Verify memory availability
3. Review startup logs for errors
4. Confirm network connectivity to EPMware server

## Best Practices

1. **Always verify** the agent has stopped before starting a new instance
2. **Clean up log files** periodically to prevent disk space issues
3. **Use service managers** (systemd, Task Scheduler) for production environments
4. **Document procedures** specific to your environment
5. **Test procedures** regularly, especially after system updates
6. **Monitor agent status** after any start/stop operation

## Related Topics

- [Background Process Management](background-process.md)
- [Agent Monitoring](../monitoring.md)
- [Troubleshooting](../../troubleshooting/index.md)
- [Agent Installation](../../installation/index.md)
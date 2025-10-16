# Start and Stop Procedures - Windows

This guide provides detailed procedures for starting and stopping the EPMware Agent on Windows servers, including scheduled tasks, manual processes, and troubleshooting.

## Starting the Agent

### Method 1: Using Task Scheduler GUI

1. **Open Task Scheduler**
   - Press `Win + R`, type `taskschd.msc`
   - Or search "Task Scheduler" in Start menu

2. **Locate the Agent Task**
   - Navigate to Task Scheduler Library
   - Find "EPMWARE TARGET AGENT SERVICE"

3. **Start the Task**
   - Right-click the task
   - Select **Run**
   - Status should change to "Running"

![Start Task GUI](../../assets/images/management/start-task-gui.png)<br/>
*Starting agent from Task Scheduler*

### Method 2: Using PowerShell

```powershell
# Start the scheduled task
Start-ScheduledTask -TaskName "EPMWARE TARGET AGENT SERVICE"

# Verify it started
Get-ScheduledTask -TaskName "EPMWARE TARGET AGENT SERVICE" | 
    Select-Object TaskName, State
```

### Method 3: Using Command Prompt

```cmd
REM Start the scheduled task
schtasks /run /tn "EPMWARE TARGET AGENT SERVICE"

REM Check status
schtasks /query /tn "EPMWARE TARGET AGENT SERVICE"
```

### Method 4: Manual Cygwin Start

```bash
# Open Cygwin Terminal
# Navigate to agent directory
cd /home/Administrator

# Start agent in foreground (for testing)
./ew_target_service.sh

# Start agent in background
./ew_target_service.sh &

# Or with nohup to persist after terminal closes
nohup ./ew_target_service.sh > agent.out 2>&1 &
```

### Verifying Agent Started

After starting, verify the agent is running:

```powershell
# Check process is running
Get-Process | Where-Object {$_.ProcessName -eq "java"} | 
    Where-Object {$_.CommandLine -like "*epmware-agent*"}

# Check logs for startup
Get-Content C:\cygwin64\home\Administrator\logs\agent.log -Tail 20

# Check polling activity
Get-Content C:\cygwin64\home\Administrator\logs\agent-poll.log -Tail 5
```

Expected log output:
```
2023-11-15 10:00:00 INFO  Starting EPMware Agent v1.7.0
2023-11-15 10:00:01 INFO  Loading configuration from agent.properties
2023-11-15 10:00:02 INFO  Connecting to https://epmware.com
2023-11-15 10:00:03 INFO  Authentication successful
2023-11-15 10:00:04 INFO  Starting polling cycle
```

## Stopping the Agent

### Method 1: Stop via Task Scheduler

1. **Open Task Scheduler**
2. **Locate "EPMWARE TARGET AGENT SERVICE"**
3. **Right-click and select "End"**

!!! warning "Process Cleanup"
    Stopping the scheduled task doesn't always kill the Java process. Always verify and manually terminate if needed.

### Method 2: Using PowerShell

```powershell
# Stop the scheduled task
Stop-ScheduledTask -TaskName "EPMWARE TARGET AGENT SERVICE"

# Find and stop Java process
$process = Get-Process | Where-Object {
    $_.ProcessName -eq "java" -and 
    $_.CommandLine -like "*epmware-agent*"
}

if ($process) {
    Stop-Process -Id $process.Id -Force
    Write-Host "Agent process stopped (PID: $($process.Id))"
} else {
    Write-Host "Agent process not found"
}
```

### Method 3: Using Command Prompt

```cmd
REM Stop scheduled task
schtasks /end /tn "EPMWARE TARGET AGENT SERVICE"

REM Find Java process
wmic process where "CommandLine like '%epmware-agent%'" get ProcessId

REM Kill process (replace PID with actual process ID)
taskkill /PID [PID] /F
```

### Method 4: Using Task Manager

1. **Open Task Manager** (`Ctrl + Shift + Esc`)
2. **Go to Details tab**
3. **Find java.exe process**
4. **Check Command Line column for "epmware-agent"**
5. **Right-click and select "End Task"**

![Task Manager Stop](../../assets/images/management/task-manager-stop.png)<br/>
*Stopping agent via Task Manager*

### Clean Stop Script

PowerShell script for clean shutdown:

```powershell
# clean_stop.ps1
param(
    [int]$Timeout = 30
)

Write-Host "Stopping EPMware Agent..."

# Stop scheduled task
Stop-ScheduledTask -TaskName "EPMWARE TARGET AGENT SERVICE" -ErrorAction SilentlyContinue

# Find agent process
$process = Get-Process | Where-Object {
    $_.ProcessName -eq "java" -and 
    $_.CommandLine -like "*epmware-agent*"
}

if ($process) {
    # Try graceful shutdown first
    $process.CloseMainWindow()
    
    # Wait for process to exit
    $waited = 0
    while (!$process.HasExited -and $waited -lt $Timeout) {
        Start-Sleep -Seconds 1
        $waited++
    }
    
    # Force kill if still running
    if (!$process.HasExited) {
        Write-Warning "Graceful shutdown failed, forcing termination..."
        Stop-Process -Id $process.Id -Force
    }
    
    Write-Host "Agent stopped successfully"
} else {
    Write-Host "Agent process not found"
}

# Clean up PID file if exists
$pidFile = "C:\cygwin64\home\Administrator\agent.pid"
if (Test-Path $pidFile) {
    Remove-Item $pidFile
}
```

## Restarting the Agent

### Automated Restart

PowerShell script for restart:

```powershell
# restart_agent.ps1
Write-Host "Restarting EPMware Agent..."

# Stop agent
& .\clean_stop.ps1

# Wait for complete shutdown
Start-Sleep -Seconds 5

# Start agent
Start-ScheduledTask -TaskName "EPMWARE TARGET AGENT SERVICE"

# Verify startup
Start-Sleep -Seconds 10
$running = Get-Process | Where-Object {
    $_.ProcessName -eq "java" -and 
    $_.CommandLine -like "*epmware-agent*"
}

if ($running) {
    Write-Host "Agent restarted successfully (PID: $($running.Id))"
} else {
    Write-Error "Agent failed to start"
}
```

### Restart with Configuration Reload

When configuration changes require restart:

```powershell
# Stop agent
& .\clean_stop.ps1

# Backup current logs
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
Copy-Item "C:\cygwin64\home\Administrator\logs\agent.log" `
    "C:\cygwin64\home\Administrator\logs\agent_$timestamp.log"

# Clear cache if needed
Remove-Item "C:\cygwin64\home\Administrator\temp\*" -Recurse -Force

# Start with new configuration
Start-ScheduledTask -TaskName "EPMWARE TARGET AGENT SERVICE"
```

## Emergency Procedures

### Force Stop All Java Processes

!!! danger "Use with Caution"
    This will stop ALL Java processes, not just the agent.

```powershell
# Emergency stop all Java
Get-Process java | Stop-Process -Force

# Or more targeted
Get-Process | Where {$_.ProcessName -eq "java"} | 
    Where {$_.CommandLine -like "*epmware*"} | 
    Stop-Process -Force
```

### Recovery from Hung Process

```powershell
# Check for hung process
$process = Get-Process java -ErrorAction SilentlyContinue | 
    Where {$_.CommandLine -like "*epmware*"}

if ($process) {
    # Check if responding
    if ($process.Responding) {
        Write-Host "Process is responding"
    } else {
        Write-Warning "Process not responding, forcing termination"
        Stop-Process -Id $process.Id -Force
        
        # Clean up locks
        Remove-Item "C:\cygwin64\home\Administrator\*.lock" -Force
        Remove-Item "C:\cygwin64\home\Administrator\agent.pid" -Force
        
        # Restart
        Start-Sleep -Seconds 5
        Start-ScheduledTask -TaskName "EPMWARE TARGET AGENT SERVICE"
    }
}
```

## Startup Issues

### Agent Won't Start

Troubleshooting checklist:

1. **Check Java**
   ```powershell
   java -version
   $env:JAVA_HOME
   ```

2. **Check Cygwin**
   ```powershell
   Test-Path "C:\cygwin64\bin\bash.exe"
   ```

3. **Check Permissions**
   ```powershell
   Get-Acl "C:\cygwin64\home\Administrator"
   ```

4. **Check Configuration**
   ```powershell
   Test-Path "C:\cygwin64\home\Administrator\agent.properties"
   Get-Content "C:\cygwin64\home\Administrator\agent.properties"
   ```

### Agent Starts Then Stops

Common causes and solutions:

| Issue | Check | Fix |
|-------|-------|-----|
| Bad configuration | agent.properties syntax | Fix syntax errors |
| Network issues | Test connectivity | Check firewall/proxy |
| Invalid token | REST token validity | Generate new token |
| Memory issues | Available RAM | Increase heap size |

### Multiple Instance Prevention

Prevent multiple agent instances:

```powershell
# Check for existing process before starting
$existing = Get-Process | Where {$_.CommandLine -like "*epmware-agent*"}
if ($existing) {
    Write-Warning "Agent already running (PID: $($existing.Id))"
    exit 1
} else {
    Start-ScheduledTask -TaskName "EPMWARE TARGET AGENT SERVICE"
}
```

## Monitoring Start/Stop Events

### Windows Event Log Integration

Log agent events to Windows Event Log:

```powershell
# Create event source (run once as admin)
New-EventLog -LogName Application -Source "EPMware Agent"

# Log start event
Write-EventLog -LogName Application -Source "EPMware Agent" `
    -EntryType Information -EventId 1000 `
    -Message "EPMware Agent started successfully"

# Log stop event
Write-EventLog -LogName Application -Source "EPMware Agent" `
    -EntryType Information -EventId 1001 `
    -Message "EPMware Agent stopped"
```

### Email Notifications

Send notifications on start/stop:

```powershell
# Email notification function
function Send-AgentNotification {
    param(
        [string]$Event,
        [string]$Status
    )
    
    $smtp = "smtp.company.com"
    $from = "epmware-agent@company.com"
    $to = "admin@company.com"
    $subject = "EPMware Agent $Event"
    $body = @"
EPMware Agent $Event
Server: $env:COMPUTERNAME
Time: $(Get-Date)
Status: $Status
"@
    
    Send-MailMessage -SmtpServer $smtp -From $from -To $to `
        -Subject $subject -Body $body
}

# Use in scripts
Send-AgentNotification -Event "Started" -Status "Success"
```

## Scheduled Maintenance

### Scheduled Restart

Configure automatic restart in Task Scheduler:

```xml
<!-- Additional trigger for weekly restart -->
<Trigger>
    <Weekly>
        <StartTime>2023-11-15T02:00:00</StartTime>
        <DaysOfWeek>Sunday</DaysOfWeek>
    </Weekly>
</Trigger>
```

### Maintenance Mode

Script to enable maintenance mode:

```powershell
# maintenance_mode.ps1
param(
    [switch]$Enable,
    [switch]$Disable
)

if ($Enable) {
    # Stop agent
    Stop-ScheduledTask -TaskName "EPMWARE TARGET AGENT SERVICE"
    
    # Disable scheduled task
    Disable-ScheduledTask -TaskName "EPMWARE TARGET AGENT SERVICE"
    
    # Create maintenance flag
    New-Item -Path "C:\cygwin64\home\Administrator\MAINTENANCE" -ItemType File
    
    Write-Host "Maintenance mode enabled"
}

if ($Disable) {
    # Remove maintenance flag
    Remove-Item -Path "C:\cygwin64\home\Administrator\MAINTENANCE" -Force
    
    # Enable scheduled task
    Enable-ScheduledTask -TaskName "EPMWARE TARGET AGENT SERVICE"
    
    # Start agent
    Start-ScheduledTask -TaskName "EPMWARE TARGET AGENT SERVICE"
    
    Write-Host "Maintenance mode disabled"
}
```

## Best Practices

### Start/Stop Guidelines

1. **Always Verify** - Check process actually started/stopped
2. **Clean Shutdown** - Allow graceful shutdown when possible
3. **Log Activities** - Record all start/stop events
4. **Monitor Health** - Check logs after restart
5. **Document Issues** - Record any problems encountered

### Automation Tips

1. **Use Scripts** - Automate common procedures
2. **Add Logging** - Include detailed logging in scripts
3. **Error Handling** - Include try-catch blocks
4. **Notifications** - Alert on failures
5. **Testing** - Test procedures in non-production

## Next Steps

- [Scheduled Tasks Configuration](scheduled-tasks.md) - Detailed task setup
- [Windows Management Overview](index.md) - Windows management guide
- [Agent Logs](../logs.md) - Understanding log files
- [Troubleshooting](../../troubleshooting/service-errors.md) - Service issues
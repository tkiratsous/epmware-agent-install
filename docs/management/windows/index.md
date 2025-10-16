# Windows Services Management

This section covers managing the EPMware Agent on Windows servers, including scheduled tasks, service management, and Windows-specific considerations.

## Windows Management Options

The EPMware Agent can run on Windows as:

<div class="grid cards" markdown>

- :material-calendar-clock: **[Scheduled Task](scheduled-tasks.md)**  
  Recommended approach using Task Scheduler
  
- :material-cog: **Windows Service**  
  Alternative using third-party tools
  
- :material-play-pause: **[Manual Process](start-stop.md)**  
  Direct execution for testing

</div>

## Management Overview

### Scheduled Task (Recommended)

Windows Task Scheduler provides:
- Automatic startup on boot
- Restart on failure
- Run without login
- Built-in Windows feature

### Windows Service (Alternative)

Using tools like NSSM or srvany:
- True Windows service
- Service dependencies
- Recovery options
- Requires additional software

### Manual Execution

For testing and troubleshooting:
- Direct control
- Console output visible
- Easy debugging
- Not for production

## Quick Management Commands

### Check Agent Status

```powershell
# Check if running
Get-Process | Where-Object {$_.ProcessName -like "*java*" -and $_.CommandLine -like "*epmware-agent*"}

# Check scheduled task
Get-ScheduledTask -TaskName "EPMWARE TARGET AGENT SERVICE"

# Check recent logs
Get-Content C:\cygwin64\home\Administrator\logs\agent.log -Tail 20
```

### Start Agent

```powershell
# Via Task Scheduler
Start-ScheduledTask -TaskName "EPMWARE TARGET AGENT SERVICE"

# Via Cygwin
C:\cygwin64\bin\bash.exe -l -c "cd ~ && ./ew_target_service.sh &"
```

### Stop Agent

```powershell
# Stop scheduled task
Stop-ScheduledTask -TaskName "EPMWARE TARGET AGENT SERVICE"

# Kill Java process
Get-Process | Where-Object {$_.CommandLine -like "*epmware-agent*"} | Stop-Process -Force
```

## Windows-Specific Configuration

### Cygwin Integration

The agent requires Cygwin for shell script execution:

```bash
# Cygwin paths
Home Directory: C:\cygwin64\home\[username]
Bash Location: C:\cygwin64\bin\bash.exe
Agent Location: /home/[username] (Cygwin path)
```

### Path Considerations

Windows path formats in configuration:

```properties
# agent.properties - Windows paths need escaping
agent.root.dir=C:\\\\cygwin64\\\\home\\\\Administrator

# Or use forward slashes
agent.root.dir=C:/cygwin64/home/Administrator
```

### User Account Setup

Configure the service account:

```powershell
# Create local user
New-LocalUser -Name "svc_epmware" -Password (ConvertTo-SecureString "Password123!" -AsPlainText -Force)

# Add to appropriate groups
Add-LocalGroupMember -Group "Administrators" -Member "svc_epmware"

# Grant logon as batch job
$policy = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
secedit /export /cfg c:\temp\export.cfg
# Edit file to add user to SeBatchLogonRight
secedit /import /cfg c:\temp\export.cfg /db secedit.sdb
```

## Task Scheduler Configuration

### Creating the Scheduled Task

PowerShell script to create task:

```powershell
# Create scheduled task via PowerShell
$taskName = "EPMWARE TARGET AGENT SERVICE"
$description = "EPMware Agent for metadata deployment"
$username = "DOMAIN\svc_epmware"

# Create action
$action = New-ScheduledTaskAction `
    -Execute "C:\cygwin64\bin\bash.exe" `
    -Argument '-l -c "./ew_target_service.sh"' `
    -WorkingDirectory "C:\cygwin64\bin"

# Create trigger (at startup)
$trigger = New-ScheduledTaskTrigger -AtStartup

# Create settings
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -RestartCount 3 `
    -RestartInterval (New-TimeSpan -Minutes 1)

# Register task
Register-ScheduledTask `
    -TaskName $taskName `
    -Description $description `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -User $username `
    -Password "Password123!" `
    -RunLevel Highest
```

### Task Configuration Details

Key settings for the scheduled task:

| Setting | Recommended Value | Purpose |
|---------|------------------|---------|
| **Run whether logged on** | Yes | Ensures continuous operation |
| **Run with highest privileges** | Yes | Required for some operations |
| **Start at startup** | Yes | Automatic start on reboot |
| **Restart on failure** | 3 times | Automatic recovery |
| **Restart interval** | 1 minute | Quick recovery |

## Service Monitoring

### Windows Event Log Integration

Monitor agent through Event Viewer:

```powershell
# Create custom event log source
New-EventLog -LogName Application -Source "EPMware Agent"

# Write events from agent
Write-EventLog -LogName Application -Source "EPMware Agent" `
    -EntryType Information -EventId 1000 -Message "Agent started"
```

### Performance Monitoring

Use Windows Performance Monitor:

```powershell
# Get Java process metrics
Get-Counter "\Process(java*)\% Processor Time"
Get-Counter "\Process(java*)\Working Set"
Get-Counter "\Process(java*)\Handle Count"
```

### Resource Usage Tracking

Monitor agent resource consumption:

```powershell
# Resource usage script
$process = Get-Process | Where {$_.ProcessName -eq "java" -and $_.CommandLine -like "*epmware*"}
if ($process) {
    Write-Host "CPU: $($process.CPU) seconds"
    Write-Host "Memory: $([math]::Round($process.WS/1MB, 2)) MB"
    Write-Host "Handles: $($process.Handles)"
    Write-Host "Threads: $($process.Threads.Count)"
}
```

## Windows Firewall Configuration

### Outbound Rules

Configure Windows Firewall for agent:

```powershell
# Allow outbound HTTPS
New-NetFirewallRule `
    -DisplayName "EPMware Agent HTTPS" `
    -Direction Outbound `
    -Protocol TCP `
    -RemotePort 443 `
    -Action Allow `
    -Program "C:\Program Files\Java\jdk1.8.0_291\bin\java.exe"

# Allow outbound to specific server
New-NetFirewallRule `
    -DisplayName "EPMware Agent Server" `
    -Direction Outbound `
    -Protocol TCP `
    -RemoteAddress "192.168.1.100" `
    -RemotePort 8080 `
    -Action Allow
```

## Troubleshooting Windows Issues

### Common Windows Problems

| Issue | Symptoms | Solution |
|-------|----------|----------|
| Cygwin not found | Scripts fail | Verify Cygwin installation path |
| Permission denied | Cannot start service | Check user rights and file permissions |
| Path issues | Java not found | Fix environment variables |
| Task not running | Agent doesn't start | Check task scheduler history |

### Windows Diagnostic Commands

```powershell
# Check Cygwin installation
Test-Path "C:\cygwin64\bin\bash.exe"

# Verify Java
java -version

# Check scheduled task details
Get-ScheduledTaskInfo -TaskName "EPMWARE TARGET AGENT SERVICE"

# Review task history
Get-WinEvent -FilterHashtable @{LogName='Microsoft-Windows-TaskScheduler/Operational'; ID=100,102,103}
```

### Event Viewer Analysis

Check these Windows logs:
- Application Log - Java errors
- System Log - Service failures
- Task Scheduler Log - Task execution

## Security Considerations

### User Rights Assignment

Required permissions for service account:

```powershell
# Required user rights
- Log on as a batch job
- Log on as a service (if running as service)
- Access this computer from network
- Allow log on locally

# Check current rights
secedit /export /cfg c:\temp\rights.cfg
type c:\temp\rights.cfg | findstr "svc_epmware"
```

### File System Permissions

Set appropriate NTFS permissions:

```powershell
# Set permissions on agent directory
$acl = Get-Acl "C:\cygwin64\home\Administrator"
$permission = "DOMAIN\svc_epmware","FullControl","ContainerInherit,ObjectInherit","None","Allow"
$accessRule = New-Object System.Security.AccessControl.FileSystemAccessRule $permission
$acl.SetAccessRule($accessRule)
Set-Acl "C:\cygwin64\home\Administrator" $acl
```

## Maintenance Scripts

### Daily Maintenance

PowerShell maintenance script:

```powershell
# daily_maintenance.ps1
param(
    [string]$AgentPath = "C:\cygwin64\home\Administrator"
)

# Check agent status
$running = Get-Process | Where {$_.ProcessName -eq "java" -and $_.CommandLine -like "*epmware*"}
if (!$running) {
    Write-Warning "Agent not running!"
    Start-ScheduledTask -TaskName "EPMWARE TARGET AGENT SERVICE"
}

# Clean old logs
Get-ChildItem "$AgentPath\logs" -Filter "*.log" | 
    Where {$_.LastWriteTime -lt (Get-Date).AddDays(-30)} | 
    Remove-Item

# Check disk space
$disk = Get-PSDrive C
if ($disk.Free -lt 1GB) {
    Write-Warning "Low disk space: $([math]::Round($disk.Free/1GB, 2)) GB free"
}
```

### Health Check Script

```powershell
# health_check.ps1
$status = @{
    Running = $false
    LastPoll = $null
    Errors = 0
    DiskSpace = 0
}

# Check process
$process = Get-Process | Where {$_.CommandLine -like "*epmware-agent*"} -ErrorAction SilentlyContinue
$status.Running = $null -ne $process

# Check last poll
$lastLog = Get-Content "C:\cygwin64\home\Administrator\logs\agent-poll.log" -Tail 1
if ($lastLog -match '(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})') {
    $status.LastPoll = [DateTime]::Parse($matches[1])
}

# Count recent errors
$errors = Get-Content "C:\cygwin64\home\Administrator\logs\agent.log" -Tail 100 | 
    Select-String "ERROR" | Measure-Object
$status.Errors = $errors.Count

# Check disk space
$disk = Get-PSDrive C
$status.DiskSpace = [math]::Round($disk.Free/1GB, 2)

# Output status
$status | ConvertTo-Json
```

## Integration with Windows Tools

### SCOM Integration

System Center Operations Manager monitoring:

```xml
<!-- SCOM Management Pack snippet -->
<Rule ID="EPMware.Agent.ProcessMonitor">
  <Target>Windows!Microsoft.Windows.Computer</Target>
  <DataSource>
    <ProcessMonitor>
      <ProcessName>java.exe</ProcessName>
      <CommandLine>epmware-agent</CommandLine>
    </ProcessMonitor>
  </DataSource>
</Rule>
```

### PowerShell DSC

Desired State Configuration for agent:

```powershell
Configuration EPMwareAgent {
    Import-DscResource -ModuleName PSDesiredStateConfiguration
    
    Node "localhost" {
        File AgentFiles {
            DestinationPath = "C:\cygwin64\home\Administrator"
            SourcePath = "\\fileserver\epmware\agent"
            Type = "Directory"
            Recurse = $true
        }
        
        ScheduledTask AgentTask {
            TaskName = "EPMWARE TARGET AGENT SERVICE"
            ActionExecutable = "C:\cygwin64\bin\bash.exe"
            ActionArguments = '-l -c "./ew_target_service.sh"'
            ScheduleType = "AtStartup"
            Enable = $true
        }
    }
}
```

## Best Practices

### Windows-Specific Recommendations

1. **Use Scheduled Tasks** - More reliable than services
2. **Monitor Event Logs** - Integrate with existing monitoring
3. **Regular Updates** - Keep Windows and Java updated
4. **Backup Configurations** - Use VSS for consistent backups
5. **Test Restarts** - Verify automatic recovery works

### Performance Optimization

1. **Antivirus Exclusions** - Exclude agent directories
2. **Windows Updates** - Schedule around agent operations
3. **Resource Allocation** - Ensure adequate CPU and memory
4. **Network Optimization** - Configure QoS if needed

## Next Steps

- [Configure Scheduled Tasks](scheduled-tasks.md) - Detailed task setup
- [Start and Stop Procedures](start-stop.md) - Operation procedures
- [Monitor Agent Logs](../logs.md) - Log management
- [Linux Management](../linux/index.md) - For Linux servers
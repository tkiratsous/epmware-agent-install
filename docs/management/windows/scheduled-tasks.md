# Configuring Agent as a Scheduled Task

## Overview

The EPMware Agent needs to run continuously on Windows servers to poll for deployment tasks. Windows Task Scheduler provides a reliable way to ensure the agent starts automatically and remains running.

## Prerequisites

Before configuring the scheduled task:

- [ ] Agent files are installed in the correct directory
- [ ] `agent.properties` is configured
- [ ] Java is installed and in the system PATH
- [ ] You have administrator privileges

## Creating the Scheduled Task

### Step 1: Open Task Scheduler

1. Log on to the Windows server with Administrator privileges
2. Open Task Scheduler using one of these methods:
   - Search for "Task Scheduler" in the Start menu
   - Run `taskschd.msc` from the command prompt
   - Navigate through Control Panel → Administrative Tools

![Task Scheduler](../../assets/images/management/task-scheduler-open.png)<br/>
*Opening Windows Task Scheduler*

### Step 2: Create New Task

1. In Task Scheduler, click **Create Task** in the Actions panel (right side)

![Create Task](../../assets/images/management/create-task-button.png)<br/>
*Create Task option in the Actions menu*

### Step 3: Configure General Settings

In the **General** tab, configure the following:

| Setting | Value |
|---------|-------|
| **Name** | `EPMWARE TARGET AGENT SERVICE` |
| **Description** | EPMware Agent for metadata deployment to target applications |
| **Security Options** | Run whether user is logged on or not |
| **Run with highest privileges** | ✓ Checked |
| **Configure for** | Windows Server 2016/2019/2022 (as appropriate) |

![General Settings](../../assets/images/management/task-general-settings.png)<br/>
*General settings for the scheduled task*

### Step 4: Configure Triggers

1. Click on the **Triggers** tab
2. Click **New** to create a trigger
3. Configure the trigger settings:

| Setting | Value |
|---------|-------|
| **Begin the task** | At startup |
| **Delay task for** | 30 seconds (optional, allows services to start) |
| **Enabled** | ✓ Checked |

![Trigger Configuration](../../assets/images/management/trigger-configuration.png)<br/>
*Configuring the startup trigger*

!!! tip "Additional Triggers"
    You can add multiple triggers, such as:
    - Daily at specific time for regular restarts
    - On workstation unlock for development environments
    - On an event for integration with monitoring systems

### Step 5: Configure Actions

1. Click on the **Actions** tab
2. Click **New** to create an action
3. Configure the action settings:

| Field | Value | Notes |
|-------|-------|-------|
| **Action** | Start a program | |
| **Program/script** | `C:\cygwin64\bin\bash.exe` | Adjust path if Cygwin is installed elsewhere |
| **Add arguments** | `-l -c "./ew_target_service.sh"` | |
| **Start in** | `C:\cygwin64\bin` | Must be the Cygwin bin directory |

![Action Configuration](../../assets/images/management/action-configuration.png)<br/>
*Configuring the action to start the agent*

!!! warning "Path Accuracy"
    Ensure the Cygwin path matches your installation. The default is `C:\cygwin64`, but it may be different in your environment.

### Step 6: Configure Conditions

1. Click on the **Conditions** tab
2. Configure the following settings:

| Setting | Value |
|---------|-------|
| **Start only if on AC power** | ☐ Unchecked (for servers) |
| **Stop if switches to battery** | ☐ Unchecked |
| **Start only if network available** | ✓ Checked |
| **Wake computer to run** | ☐ Unchecked |

### Step 7: Configure Settings

1. Click on the **Settings** tab
2. Configure the following:

| Setting | Value |
|---------|-------|
| **Allow task to be run on demand** | ✓ Checked |
| **Run task as soon as possible after missed start** | ✓ Checked |
| **If task fails, restart every** | 1 minute |
| **Attempt restart up to** | 3 times |
| **Stop task if runs longer than** | ☐ Unchecked |
| **If running task does not end when requested** | ✓ Force stop |

![Settings Configuration](../../assets/images/management/settings-configuration.png)<br/>
*Task settings for reliability*

### Step 8: Save with Credentials

1. Click **OK** to save the task
2. Enter credentials when prompted:
   - Username: Use the same user under which Cygwin is installed
   - Password: Enter the user's password
   - These credentials will be used to run the task

![Enter Credentials](../../assets/images/management/enter-credentials.png)<br/>
*Entering credentials for the scheduled task*

## Starting the Scheduled Task

### Manual Start

1. In Task Scheduler, locate `EPMWARE TARGET AGENT SERVICE`
2. Right-click the task
3. Select **Run**

![Run Task](../../assets/images/management/run-task.png)<br/>
*Manually starting the scheduled task*

### Verify Task is Running

Check the task status:
1. The Status column should show "Running"
2. Last Run Result should show "The operation completed successfully. (0x0)"

![Task Running](../../assets/images/management/task-running-status.png)<br/>
*Scheduled task running successfully*

## Monitoring the Scheduled Task

### Task History

Enable task history to track execution:
1. In Task Scheduler, click **Enable All Tasks History** in the Actions panel
2. Select your task and click the **History** tab

### Check Agent Logs

Verify the agent is working by checking log files:

```bash
# Navigate to agent directory
cd C:\cygwin64\home\Administrator\logs

# Check polling log
type agent-poll.log

# Check main agent log
type agent.log
```

The logs should show:
- **agent-poll.log**: Regular polling entries every 30 seconds
- **agent.log**: Deployment activities and any errors

![Agent Logs](../../assets/images/management/agent-logs-content.png)<br/>
*Sample agent log entries showing normal operation*

## Troubleshooting Scheduled Tasks

### Common Issues

| Issue | Solution |
|-------|----------|
| Task won't start | Verify Cygwin path and user permissions |
| Task starts but stops immediately | Check agent.properties configuration |
| "Access Denied" error | Ensure user has "Log on as batch job" permission |
| Task runs but agent doesn't poll | Verify Java is in PATH for the task user |

### Permission Requirements

The task user account needs:
- **Log on as a batch job** right
- **Read/write** access to agent directory
- **Execute** permission for Java and Cygwin

To grant "Log on as batch job":
1. Run `secpol.msc`
2. Navigate to Local Policies → User Rights Assignment
3. Add user to "Log on as a batch job"

### Debugging Steps

1. **Check Task History**
   ```
   Event ID 100 - Task Started
   Event ID 102 - Task Completed
   Event ID 103 - Task Failed
   ```

2. **Run Manually in Cygwin**
   ```bash
   # Open Cygwin terminal as the service user
   cd /home/Administrator
   ./ew_target_service.sh
   ```

3. **Enable Detailed Logging**
   Add to agent.properties:
   ```properties
   agent.log.level=DEBUG
   ```

## Best Practices

### Security Recommendations

- Use a dedicated service account for the agent
- Implement least privilege principle
- Store credentials securely
- Regular password rotation for service account

### Monitoring Setup

1. Configure email notifications for task failures
2. Set up monitoring alerts for log file errors
3. Implement health check scripts
4. Monitor disk space for log files

### Maintenance Tasks

- **Weekly**: Review agent logs for errors
- **Monthly**: Clean up old log files
- **Quarterly**: Update agent software if needed
- **Annually**: Review and update service account permissions

!!! tip "High Availability"
    For production environments, consider setting up a secondary server with an identical scheduled task configuration for failover capabilities.

!!! warning "Java Process Cleanup"
    When stopping the scheduled task, the Java process may not terminate automatically. Always verify and manually terminate if necessary before restarting.

## Advanced Configuration

### Multiple Agent Instances

To run multiple agents for different applications:

1. Create separate directories for each agent
2. Configure unique `agent.properties` for each
3. Create separate scheduled tasks with distinct names
4. Use different polling intervals to prevent conflicts

### PowerShell Alternative

For environments preferring PowerShell:

```powershell
# Create scheduled task via PowerShell
$action = New-ScheduledTaskAction -Execute "C:\cygwin64\bin\bash.exe" `
    -Argument '-l -c "./ew_target_service.sh"' `
    -WorkingDirectory "C:\cygwin64\bin"

$trigger = New-ScheduledTaskTrigger -AtStartup

$settings = New-ScheduledTaskSettingsSet -RestartCount 3 `
    -RestartInterval (New-TimeSpan -Minutes 1)

Register-ScheduledTask -TaskName "EPMWARE TARGET AGENT SERVICE" `
    -Action $action -Trigger $trigger -Settings $settings `
    -User "DOMAIN\ServiceAccount" -Password "SecurePassword"
```

## Next Steps

After configuring the scheduled task:

1. [Monitor Agent Logs](../logs.md)
2. [Configure Application Integration](../../integration/index.md)
3. [Set up Monitoring Alerts](../monitoring.md)
4. [Test Deployment Process](../../configuration/testing.md)
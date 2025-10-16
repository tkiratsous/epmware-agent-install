# Agent Properties Configuration

## Overview

The `agent.properties` file contains all configuration settings for the EPMware Agent. This file must be properly configured before starting the agent service.

## Location

The `agent.properties` file is located in the agent installation directory:

- **Windows**: `C:\cygwin64\home\[username]\agent.properties`
- **Linux**: `/home/[username]/agent.properties`

![Agent Properties File](../assets/images/configuration/agent-properties-file.png)<br/>
*Location of agent.properties file in the installation directory*

## Configuration Parameters

### Core Settings

| Property | Description | Example |
|----------|-------------|---------|
| `ew.portal.server` | Server name configured in EPMware | `epmware1.epmware.com` |
| `ew.portal.url` | EPMware application URL | `https://client.epmwarecloud.com` |
| `ew.portal.token` | REST API authentication token | `2e6d4103-5145-4c30-9837-ac6d14797523` |
| `agent.interval.millisecond` | Polling interval in milliseconds | `30000` |
| `agent.root.dir` | Agent installation directory | `C:\\\\cygwin64\\\\home\\\\Administrator` |

### Optional Parameters

| Property | Description | Example |
|----------|-------------|---------|
| `agent.params.quote` | Quote character for parameters | `"` (for Linux) |
| `agent.log.level` | Logging verbosity | `INFO`, `DEBUG`, `ERROR` |
| `agent.timeout.seconds` | Command execution timeout | `3600` |
| `agent.retry.count` | Number of retry attempts | `3` |

## Configuration Examples

### Cloud EPMware Configuration

```properties
# EPMware Cloud Configuration
ew.portal.server=epmware1.epmware.com
ew.portal.url=https://client.epmwarecloud.com
ew.portal.token=2e6d4103-5145-4c30-9837-ac6d14797523
agent.interval.millisecond=30000
agent.root.dir=C:\\\\cygwin64\\\\home\\\\Administrator
```

### On-Premise EPMware Configuration

```properties
# EPMware On-Premise Configuration
ew.portal.server=epmware1.epmware.com
ew.portal.url=http://epmware-server.com:8080/epmware
ew.portal.token=2e6d4103-5145-4c30-9837-ac6d14797523
agent.interval.millisecond=30000
agent.root.dir=C:\\\\cygwin64\\\\home\\\\Administrator
```

### Linux Server Configuration

```properties
# Linux Server Configuration
ew.portal.server=epmware1.epmware.com
ew.portal.url=https://client.epmwarecloud.com
ew.portal.token=2e6d4103-5145-4c30-9837-ac6d14797523
agent.interval.millisecond=30000
agent.root.dir=/home/epmadmin
agent.params.quote="
```

## Obtaining Configuration Values

### Server Name

The server name must match the name configured in EPMware:

1. Log into EPMware application
2. Navigate to **Infrastructure** → **Servers**
3. Note the exact server name

![Server Configuration](../assets/images/configuration/server-name.png)<br/>
*Server name configuration in EPMware*

### Portal URL

- **Cloud**: Use the provided EPMware cloud URL (e.g., `https://client.epmwarecloud.com`)
- **On-Premise**: Use your internal EPMware server URL with port

### REST API Token

See [REST API Token Configuration](rest-token.md) for detailed instructions on generating tokens.

## Parameter Details

### Polling Interval

The `agent.interval.millisecond` parameter controls how frequently the agent checks for tasks:

| Setting | Milliseconds | Use Case |
|---------|-------------|----------|
| Frequent | 10000 (10 sec) | High-priority production environments |
| **Standard** | **30000 (30 sec)** | **Recommended for most environments** |
| Infrequent | 60000 (60 sec) | Low-volume or development environments |
| Minimal | 300000 (5 min) | Testing or maintenance windows |

!!! tip "Performance Optimization"
    Lower polling intervals increase server load but reduce deployment latency. Adjust based on your deployment frequency and performance requirements.

### Directory Paths

#### Windows Path Format

Windows paths require double backslashes:

```properties
agent.root.dir=C:\\\\cygwin64\\\\home\\\\Administrator
```

#### Linux Path Format

Linux paths use forward slashes:

```properties
agent.root.dir=/home/epmadmin
```

### Quote Character Configuration

The `agent.params.quote` parameter is used for enclosing parameter values:

- **Windows**: Not required (default handling)
- **Linux**: Set to `"` (double quote)

This ensures proper handling of parameters with spaces or special characters.

## Validation

### Check Configuration

After editing `agent.properties`, validate your configuration:

1. Verify all required parameters are set
2. Ensure URLs are accessible
3. Confirm token is valid
4. Check directory paths exist

### Test Connection

Test the configuration before starting the agent service:

```bash
# From Cygwin terminal (Windows) or shell (Linux)
cd $HOME
java -jar epmware-agent.jar --spring.config.name=agent --test
```

## Security Considerations

### Protecting the Configuration File

The `agent.properties` file contains sensitive information:

- Set appropriate file permissions (read/write for agent user only)
- Never commit to version control
- Use encrypted storage for backups
- Rotate tokens periodically

#### Linux Permissions

```bash
chmod 600 agent.properties
chown epmadmin:epmadmin agent.properties
```

#### Windows Permissions

Right-click the file → Properties → Security → Edit:
- Remove unnecessary users
- Grant full control only to the agent service account

### Token Management

- Generate unique tokens per environment
- Implement token rotation schedule
- Monitor token usage in audit logs
- Revoke compromised tokens immediately

## Environment-Specific Configurations

### Development Environment

```properties
# Development settings - verbose logging, longer intervals
ew.portal.url=https://dev.epmwarecloud.com
agent.interval.millisecond=60000
agent.log.level=DEBUG
agent.timeout.seconds=7200
```

### Production Environment

```properties
# Production settings - standard logging, frequent polling
ew.portal.url=https://prod.epmwarecloud.com
agent.interval.millisecond=30000
agent.log.level=INFO
agent.timeout.seconds=3600
agent.retry.count=3
```

## Troubleshooting Configuration Issues

### Common Problems

| Issue | Possible Cause | Solution |
|-------|---------------|----------|
| Connection refused | Invalid URL | Verify `ew.portal.url` is correct |
| Authentication failed | Invalid token | Generate new token in EPMware |
| Path not found | Incorrect directory | Verify `agent.root.dir` exists |
| Polling not working | Invalid interval | Ensure interval is in milliseconds |

### Configuration Validation Checklist

- [ ] Server name matches EPMware configuration exactly
- [ ] URL protocol is correct (http:// or https://)
- [ ] Token is 36 characters long
- [ ] Paths use correct format for OS
- [ ] No trailing spaces in values
- [ ] File encoding is UTF-8
- [ ] No special characters in unquoted values

!!! warning "Path Separators"
    Always use four backslashes (`\\\\`) for Windows paths in the properties file. This accounts for Java escaping requirements.

!!! note "Property Changes"
    Changes to `agent.properties` require restarting the agent service to take effect.

## Next Steps

After configuring agent properties:

1. [Configure the Service](service-config.md)
2. [Generate REST API Token](rest-token.md)
3. [Test the Connection](testing.md)
4. [Schedule the Agent](../management/windows/scheduled-tasks.md)
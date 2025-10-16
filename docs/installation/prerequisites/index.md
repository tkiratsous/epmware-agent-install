# Prerequisites Overview

Before installing the EPMware Agent, certain software prerequisites must be met. This section guides you through installing and configuring the required components.

## Required Software

<div class="grid cards" markdown>

- :material-microsoft-windows: **[Cygwin](cygwin.md)** *(Windows only)*  
  Linux-like environment for Windows systems
  
- :material-language-java: **[Java](java.md)** *(All platforms)*  
  Java Runtime Environment 1.8 or higher
  
- :material-zip-box: **Compression Tools**  
  zip/unzip utilities for package extraction

</div>

## Platform-Specific Requirements

### Windows Prerequisites

For Windows servers, you need:

1. **Cygwin** - Provides Unix-like environment
   - Enables shell script execution
   - Creates user home directories
   - Provides command-line tools

2. **Java JRE/JDK** - Runtime environment
   - Version 1.8 or higher
   - 64-bit recommended
   - Added to system PATH

3. **Administrative Access** - For installation
   - Install software
   - Configure services
   - Modify system settings

### Linux Prerequisites

For Linux servers, you need:

1. **Java JRE/JDK** - Runtime environment
   - OpenJDK or Oracle Java
   - Version 1.8 or higher
   - Configured in PATH

2. **Standard Tools** - Usually pre-installed
   - bash shell
   - zip/unzip
   - curl or wget

3. **User Account** - For agent operation
   - Home directory access
   - Read/write permissions
   - Network access rights

## Quick Prerequisites Check

### Windows Quick Check

```cmd
REM Check Java
java -version

REM Check Cygwin
C:\cygwin64\bin\bash --version

REM Check zip
where zip
```

### Linux Quick Check

```bash
# Check Java
java -version

# Check shell
echo $SHELL

# Check tools
which zip unzip curl
```

## Installation Order

Follow this sequence for best results:

1. **Operating System Updates**
   - Apply latest patches
   - Reboot if required

2. **Cygwin** (Windows only)
   - Download and install
   - Configure user environment
   - Verify terminal access

3. **Java**
   - Install JRE or JDK
   - Set JAVA_HOME
   - Add to PATH
   - Verify installation

4. **Network Configuration**
   - Open required ports
   - Configure proxy (if needed)
   - Test connectivity

## Prerequisite Validation

### System Requirements Check

Verify your system meets minimum requirements:

```bash
# Check CPU
lscpu | grep "CPU(s)"  # Linux
wmic cpu get NumberOfCores  # Windows

# Check Memory
free -h  # Linux
wmic OS get TotalVisibleMemorySize  # Windows

# Check Disk Space
df -h  # Linux
wmic logicaldisk get size,freespace  # Windows
```

### Software Version Check

Ensure correct versions are installed:

| Software | Minimum Version | Check Command |
|----------|-----------------|---------------|
| Java | 1.8 | `java -version` |
| Cygwin | 3.0 | `uname -r` (in Cygwin) |
| bash | 4.0 | `bash --version` |

## Common Prerequisite Issues

### Issue: Java Not Found

**Symptoms:**
- `'java' is not recognized as an internal or external command`
- `bash: java: command not found`

**Solution:**
1. Install Java if missing
2. Add Java to PATH
3. Restart terminal/command prompt

### Issue: Cygwin Not Working (Windows)

**Symptoms:**
- Cannot open Cygwin terminal
- Scripts fail with "bad interpreter"

**Solution:**
1. Reinstall Cygwin
2. Ensure proper installation path
3. Check Windows environment variables

### Issue: Insufficient Permissions

**Symptoms:**
- Cannot create directories
- Permission denied errors

**Solution:**
1. Run as administrator (Windows)
2. Use sudo (Linux)
3. Check user permissions

## Environment Preparation

### Create Agent User (Recommended)

**Windows:**
```cmd
REM Create local user
net user epmware_agent Password123! /add
net localgroup Administrators epmware_agent /add
```

**Linux:**
```bash
# Create user with home directory
sudo useradd -m -s /bin/bash epmware_agent
sudo passwd epmware_agent
```

### Set Up Directory Structure

```bash
# Create directories
mkdir -p /opt/epmware/agent
mkdir -p /var/log/epmware
mkdir -p /var/run/epmware

# Set permissions
chown -R epmware_agent:epmware_agent /opt/epmware
chmod 755 /opt/epmware/agent
```

## Network Prerequisites

### Required Connectivity

Ensure the agent can reach:

1. **EPMware Server**
   - Cloud: Port 443 (HTTPS)
   - On-premise: Configured port

2. **Target Applications**
   - HFM: Port 19000 (typical)
   - Planning: Port 19000
   - Essbase: Port 1423

### Firewall Configuration

**Windows Firewall:**
```cmd
REM Allow outbound HTTPS
netsh advfirewall firewall add rule name="EPMware Agent HTTPS" ^
  dir=out action=allow protocol=TCP remoteport=443
```

**Linux iptables:**
```bash
# Allow outbound HTTPS
sudo iptables -A OUTPUT -p tcp --dport 443 -j ACCEPT
sudo iptables-save
```

### Proxy Configuration

If using a proxy server:

```bash
# Set proxy environment variables
export HTTP_PROXY=http://proxy.company.com:8080
export HTTPS_PROXY=http://proxy.company.com:8080
export NO_PROXY=localhost,127.0.0.1,internal.domain
```

## Prerequisites for Specific Applications

### HFM Prerequisites

Additional requirements for HFM integration:
- HFM client utilities installed
- Access to HFM registry files
- HFM user credentials

### Planning Prerequisites

Additional requirements for Planning:
- Planning utilities accessible
- Ability to create encrypted password files
- Planning admin credentials

### Cloud EPM Prerequisites

Additional requirements for cloud:
- EPM Automate utility
- Cloud service URL
- Identity domain information

## Validation Checklist

Before proceeding to agent installation:

### System Checklist
- [ ] Operating system is supported
- [ ] Sufficient CPU resources (2+ cores)
- [ ] Adequate memory (16+ GB)
- [ ] Available disk space (60+ GB)

### Software Checklist
- [ ] Cygwin installed (Windows)
- [ ] Java 1.8+ installed
- [ ] Java in system PATH
- [ ] zip/unzip available
- [ ] Network tools available

### Network Checklist
- [ ] Can reach EPMware server
- [ ] Required ports are open
- [ ] Proxy configured (if needed)
- [ ] DNS resolution working

### Security Checklist
- [ ] Agent user account created
- [ ] Appropriate permissions set
- [ ] Firewall rules configured
- [ ] Security policies reviewed

## Troubleshooting Prerequisites

### Diagnostic Commands

Run these commands to diagnose issues:

```bash
# System information
uname -a  # Linux/Cygwin
systeminfo  # Windows

# Network diagnostics
ping epmware-server.com
nslookup epmware-server.com
traceroute epmware-server.com  # Linux
tracert epmware-server.com  # Windows

# Java diagnostics
java -version
echo $JAVA_HOME
which java

# Permission check
id  # Linux
whoami /all  # Windows
```

### Common Fixes

1. **Path Issues**
   ```bash
   # Add to PATH
   export PATH=$PATH:/usr/local/bin
   # Make permanent in .bashrc or .profile
   ```

2. **Permission Issues**
   ```bash
   # Fix ownership
   sudo chown -R $(whoami) /path/to/directory
   ```

3. **Network Issues**
   ```bash
   # Test connectivity
   telnet server.com 443
   curl -I https://server.com
   ```

## Best Practices

### Documentation

Document your prerequisite configuration:
- Java version and location
- Cygwin installation path (Windows)
- Network settings
- User accounts created

### Standardization

Use consistent configurations across environments:
- Same Java version
- Identical Cygwin setup (Windows)
- Uniform directory structures
- Standard user naming

### Security

Follow security best practices:
- Use dedicated service accounts
- Apply principle of least privilege
- Keep software updated
- Document security exceptions

!!! tip "Prerequisite Script"
    Consider creating a script to automatically check all prerequisites. This ensures consistency and saves time during installation.

!!! warning "Version Compatibility"
    Always verify that prerequisite versions are compatible with your EPMware Agent version and target applications.

## Next Steps

After prerequisites are satisfied:

1. [Install Cygwin](cygwin.md) - Windows only
2. [Configure Java](java.md) - All platforms
3. [Download Agent](../agent/download.md) - Get agent files
4. [Begin Installation](../agent/index.md) - Deploy agent
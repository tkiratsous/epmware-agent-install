# Installation Overview

The EPMware Agent installation process consists of three main phases: prerequisites installation, agent deployment, and configuration. This section guides you through each phase to ensure a successful installation.

## Installation Process

<div class="grid cards" markdown>

- :material-check-circle: **Prerequisites**  
  Install required software including Java and Cygwin (Windows only)
  
- :material-download: **Agent Installation**  
  Download and extract agent files to the appropriate directory
  
- :material-cog: **Configuration**  
  Configure properties, tokens, and test connectivity

</div>

## Before You Begin

### Pre-Installation Checklist

- [ ] Verify [System Requirements](../getting-started/requirements.md) are met
- [ ] Obtain EPMware Agent installation package (`ew_agent_files.zip`)
- [ ] Have administrator or appropriate user access to the target server
- [ ] Know your EPMware server URL (cloud or on-premise)
- [ ] Have credentials for a dedicated EPMware service account
- [ ] Identify target applications for integration

### Required Information

Gather the following information before starting:

| Information | Description | Example |
|------------|-------------|---------|
| **EPMware URL** | Your EPMware instance URL | `https://client.epmwarecloud.com` |
| **Server Name** | Name configured in EPMware | `hfmserver01` |
| **Service Account** | EPMware user for agent | `svc_epmware_agent` |
| **Installation Path** | Where agent will be installed | `C:\cygwin64\home\Administrator` |
| **Target Applications** | Applications to integrate | HFM, Planning, PCMCS |

## Installation Options

### Windows Installation

For Windows servers, the installation requires:
1. Cygwin environment setup
2. Agent file extraction
3. Windows Task Scheduler configuration

**Estimated Time**: 30-45 minutes

### Linux Installation

For Linux servers, the process involves:
1. Java verification
2. Agent file extraction
3. Background service configuration

**Estimated Time**: 20-30 minutes

## Installation Phases

### Phase 1: Prerequisites

Install and configure required software:

- **[Cygwin Installation](prerequisites/cygwin.md)** (Windows only)
  - Download and install Cygwin
  - Configure user environment
  - Verify installation

- **[Java Configuration](prerequisites/java.md)**
  - Install Java 1.8 or higher
  - Set JAVA_HOME variable
  - Add Java to system PATH

### Phase 2: Agent Deployment

Deploy the EPMware Agent files:

- **[Download and Extract](agent/download.md)**
  - Obtain agent package
  - Extract to home directory
  - Verify file permissions

- **[File Structure](agent/file-structure.md)**
  - Understand agent components
  - Review directory layout
  - Check file integrity

### Phase 3: Initial Configuration

Complete basic configuration:

- Configure agent properties
- Generate REST API token
- Test connectivity
- Schedule agent service

## Quick Installation Guide

For experienced administrators, here's a quick reference:

### Windows Quick Install

```bash
# 1. Install Cygwin (if not present)
# Download from www.cygwin.com

# 2. Extract agent files
cd C:\cygwin64\home\Administrator
unzip ew_agent_files.zip

# 3. Configure properties
edit agent.properties

# 4. Test connection
./ew_target_service.sh

# 5. Schedule task
# Use Task Scheduler to create "EPMWARE TARGET AGENT SERVICE"
```

### Linux Quick Install

```bash
# 1. Verify Java
java -version

# 2. Extract agent files
cd /home/epmadmin
unzip ew_agent_files.zip

# 3. Configure properties
vi agent.properties

# 4. Test connection
./ew_target_service.sh

# 5. Run as background service
nohup ./ew_target_service.sh &
```

## Post-Installation Tasks

After installation, complete these tasks:

1. **Verify Installation**
   - Check agent logs for successful startup
   - Confirm polling is active
   - Test connection from EPMware

2. **Configure Applications**
   - Set up HFM integration if needed
   - Configure Planning applications
   - Set up Cloud EPM connections

3. **Security Hardening**
   - Set appropriate file permissions
   - Configure firewall rules
   - Implement token rotation schedule

4. **Documentation**
   - Document configuration settings
   - Record service account details
   - Note any customizations

## Common Installation Scenarios

### Scenario 1: Single Server, Multiple Applications

Installing agent on a server hosting multiple EPM applications:
- Install agent once
- Configure for all applications
- Use single polling interval

### Scenario 2: Distributed Environment

Installing agents across multiple servers:
- Install agent on each application server
- Use unique tokens per agent
- Coordinate polling intervals

### Scenario 3: Cloud and On-Premise Hybrid

Installing for mixed environment:
- Install on-premise agent for local apps
- Configure EPM Automate for cloud apps
- Manage both through EPMware

## Troubleshooting Installation

### Common Installation Issues

| Issue | Solution |
|-------|----------|
| Permission denied during extraction | Run as administrator or check user permissions |
| Java not found | Install Java and set PATH variable |
| Cygwin not working | Reinstall with default packages |
| Cannot create directories | Check disk space and permissions |

### Getting Help

If you encounter issues during installation:

1. Check the [Troubleshooting Guide](../troubleshooting/index.md)
2. Review agent logs for error messages
3. Contact EPMware Support at support@epmware.com

!!! tip "Best Practice"
    Always perform a test installation in a non-production environment first to familiarize yourself with the process and identify any environment-specific issues.

!!! warning "Security Note"
    Never install the agent using a personal user account. Always use a dedicated service account with appropriate permissions.

## Next Steps

Begin the installation process:

1. **[Install Prerequisites](prerequisites/index.md)** - Set up required software
2. **[Deploy Agent Files](agent/index.md)** - Extract and organize agent components
3. **[Configure Agent](../configuration/index.md)** - Set up properties and authentication
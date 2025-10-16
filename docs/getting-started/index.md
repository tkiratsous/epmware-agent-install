# Getting Started

Welcome to the EPMware Agent Installation Guide. This section provides essential information to help you understand the agent's purpose, architecture, and requirements before beginning installation.

## What is the EPMware Agent?

The EPMware Agent is a secure bridge between EPMware's cloud or on-premise application and your target EPM systems. It enables automated metadata deployment without exposing your internal applications to external networks.

### Key Benefits

- **Secure Communication** - No inbound firewall rules required
- **Automated Deployment** - Hands-free metadata updates
- **Multi-Application Support** - Single agent for multiple targets
- **Audit Trail** - Complete logging of all operations
- **Reliable Operations** - Automatic retry and error recovery

## Quick Start Path

For experienced administrators familiar with EPMware:

<div class="grid cards" markdown>

- :material-speedometer: **Fast Track Installation**  
  1. Check [Requirements](requirements.md)
  2. Install [Prerequisites](../installation/prerequisites/index.md)
  3. [Deploy Agent](../installation/agent/index.md)
  4. [Configure](../configuration/index.md)
  5. [Test](../configuration/testing.md)

- :material-book-open-variant: **Detailed Installation**  
  Follow the complete guide starting with:
  - [Introduction](introduction.md)
  - [System Requirements](requirements.md)
  - [Architecture Overview](architecture.md)

</div>

## Installation Overview

The complete installation process involves:

### Phase 1: Preparation (30 minutes)
- Review system requirements
- Understand architecture
- Gather required information
- Prepare target server

### Phase 2: Installation (45 minutes)
- Install prerequisites (Cygwin, Java)
- Extract agent files
- Set file permissions
- Verify installation

### Phase 3: Configuration (30 minutes)
- Configure agent properties
- Generate REST token
- Set up service script
- Test connectivity

### Phase 4: Integration (Variable)
- Configure target applications
- Set up scheduled tasks
- Implement monitoring
- Document setup

## Before You Begin

### Required Information

Gather this information before starting:

| Information | Description | Where to Find |
|------------|-------------|---------------|
| **EPMware URL** | Your EPMware instance address | Provided by EPMware team |
| **Server Name** | Name in EPMware configuration | Infrastructure → Servers |
| **REST Token** | Authentication token | Generate in User Management |
| **Target Applications** | Applications to integrate | Your EPM landscape |

### Required Access

Ensure you have:

- **Server Access**
  - Administrator privileges (Windows)
  - Root or sudo access (Linux)
  - Ability to install software
  - Permission to create services

- **Network Access**
  - Outbound HTTPS (port 443)
  - Access to target applications
  - Proxy credentials (if applicable)

- **EPMware Access**
  - User account in EPMware
  - Permission to generate tokens
  - Access to server configuration

## Supported Configurations

### Operating Systems

| Platform | Versions | Notes |
|----------|----------|-------|
| **Windows Server** | 2016, 2019, 2022 | Requires Cygwin |
| **Red Hat Linux** | 7.x, 8.x | Recommended |
| **Oracle Linux** | 7.x, 8.x | Recommended |
| **Ubuntu** | 18.04, 20.04, 22.04 LTS | Supported |

### Target Applications

| Application | Versions | Integration Type |
|------------|----------|------------------|
| **Hyperion HFM** | 11.1.2.4.x, 11.2.x | Direct via utilities |
| **Hyperion Planning** | 11.1.2.4.x, 11.2.x | Direct via utilities |
| **Essbase** | 11.1.2.4.x, 21c | MaxL scripts |
| **PCMCS** | Cloud | EPM Automate |
| **Other Cloud EPM** | Current | EPM Automate |

### Deployment Scenarios

The agent supports various deployment models:

1. **Single Agent** - One agent managing multiple applications
2. **Multiple Agents** - Dedicated agents per application
3. **High Availability** - Active/passive agent configuration
4. **Hybrid Cloud** - Managing both on-premise and cloud

## Decision Points

### Installation Location

Choose the optimal location for your agent:

| Option | Pros | Cons |
|--------|------|------|
| **Application Server** | Direct access, no network latency | Resource competition |
| **Dedicated Server** | Isolated, better security | Additional infrastructure |
| **Shared Services Server** | Centralized management | Single point of failure |

### User Account Strategy

Decide on the user account approach:

| Strategy | Use Case | Considerations |
|----------|----------|----------------|
| **Single Service Account** | Simple environments | Easier management |
| **Per-Application Accounts** | Complex security | More configuration |
| **Dedicated Agent Account** | Recommended | Best security isolation |

## Common Use Cases

### Use Case 1: HFM Metadata Management

**Scenario:** Automate HFM dimension updates from EPMware

**Requirements:**
- Agent on HFM server or connected server
- HFM utilities accessible
- Registry properties configured

### Use Case 2: Cloud EPM Integration

**Scenario:** Deploy to PCMCS from EPMware

**Requirements:**
- Agent with internet access
- EPM Automate installed
- Cloud credentials

### Use Case 3: Multi-Application Deployment

**Scenario:** Single workflow deploys to multiple targets

**Requirements:**
- Agent with access to all applications
- Credentials for each system
- Coordinated deployment windows

## Success Criteria

Your agent installation is successful when:

- ✓ Agent connects to EPMware
- ✓ Polling shows in logs
- ✓ Test deployment completes
- ✓ Status updates in EPMware
- ✓ No errors in agent logs

## Getting Help

### Documentation Resources

- **This Guide** - Complete installation instructions
- **EPMware Admin Guide** - Application configuration
- **EPMware User Guide** - Using the application
- **Release Notes** - Latest features and fixes

### Support Channels

- **Email:** support@epmware.com
- **Phone:** 408-614-0442
- **Portal:** support.epmware.com

### Information to Provide

When requesting help, include:

1. Agent version
2. Operating system
3. Error messages
4. Log excerpts
5. Configuration files (sanitized)

## Installation Timeline

Typical installation timeline:

| Phase | Duration | Activities |
|-------|----------|------------|
| Planning | 1-2 hours | Requirements review, information gathering |
| Prerequisites | 1-2 hours | Software installation, network configuration |
| Agent Installation | 1 hour | File deployment, initial configuration |
| Testing | 1-2 hours | Connectivity tests, trial deployments |
| Integration | 2-4 hours | Application-specific configuration |
| Documentation | 1 hour | Record configuration, create runbooks |

**Total: 8-12 hours** for complete production setup

## Risk Mitigation

### Common Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Network connectivity issues | Agent cannot communicate | Test connectivity before installation |
| Insufficient permissions | Cannot deploy metadata | Verify account privileges |
| Version incompatibility | Integration failures | Check compatibility matrix |
| Resource constraints | Performance issues | Monitor system resources |

## Next Steps

Ready to begin? Proceed through these sections:

1. **[Introduction](introduction.md)** - Understand EPMware and the agent
2. **[System Requirements](requirements.md)** - Verify your environment
3. **[Architecture Overview](architecture.md)** - Learn how it works
4. **[Installation](../installation/index.md)** - Begin installation process

!!! tip "Preparation is Key"
    Time spent in preparation saves troubleshooting time later. Review all prerequisites and gather required information before starting installation.

!!! note "Version Information"
    This guide covers EPMware Agent version 1.7. Check the release notes for version-specific information.
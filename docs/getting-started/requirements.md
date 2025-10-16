# System Requirements

## Hardware Requirements

The following specifications are recommended for optimal agent performance:

### Minimum Requirements

| Component | Specification |
|-----------|--------------|
| **Processor** | 2 CPU x64 Intel or AMD64 Processor |
| **Memory** | 16 GB RAM |
| **Storage** | 60 GB available disk space |
| **Network** | 1 Gbps network connection |

### Recommended Configuration

| Component | Specification |
|-----------|--------------|
| **Processor** | 4+ CPU cores x64 Intel or AMD64 Processor |
| **Memory** | 32 GB RAM or higher |
| **Storage** | 100+ GB available disk space |
| **Network** | 10 Gbps network connection |

## Software Requirements

### Operating Systems

The EPMware Agent supports the following operating systems:

- **Linux** (Recommended)
  - Red Hat Enterprise Linux 7.x, 8.x
  - Oracle Linux 7.x, 8.x
  - CentOS 7.x, 8.x
  - Ubuntu 18.04 LTS, 20.04 LTS, 22.04 LTS

- **Windows**
  - Windows Server 2016
  - Windows Server 2019
  - Windows Server 2022
  - Windows 10 (for development/testing only)

### Required Software

| Software | Version | Notes |
|----------|---------|-------|
| **Java** | 1.8 or higher | JRE or JDK required |
| **Cygwin** | Latest stable | Required for Windows installations only |
| **zip/unzip** | Any version | Must be in system PATH |

### Target Application Compatibility

The agent supports integration with:

| Application | Supported Versions |
|-------------|-------------------|
| **Hyperion HFM** | 11.1.2.4.x, 11.2.x |
| **Hyperion Planning** | 11.1.2.4.x, 11.2.x |
| **Essbase** | 11.1.2.4.x, 21c |
| **Oracle Cloud EPM** | Current versions |
| **PCMCS** | Current versions |
| **EPM Automate** | Latest version (for cloud integrations) |

## Network Requirements

### Port Configuration

Ensure the following ports are open for communication:

| Direction | Port | Protocol | Purpose |
|-----------|------|----------|---------|
| **Outbound** | 443 | HTTPS | EPMware Cloud communication |
| **Outbound** | 8080 | HTTP | EPMware On-Premise (configurable) |
| **Outbound** | Target App Ports | Various | Application-specific communication |

### Firewall Rules

Configure firewall rules to allow:

- Outbound HTTPS traffic to EPMware cloud URL
- Communication with target application servers
- DNS resolution for cloud services

### Network Bandwidth

- **Minimum**: 10 Mbps dedicated bandwidth
- **Recommended**: 100 Mbps or higher for large metadata deployments
- **Latency**: Less than 200ms to EPMware servers

## Security Requirements

### User Permissions

The agent requires:

- **Windows**: Local administrator rights or service account with appropriate permissions
- **Linux**: User account with read/write access to agent directory
- **Target Applications**: Valid user credentials with metadata management permissions

### Authentication

- REST API token for EPMware authentication
- Application-specific credentials for target systems
- SSL/TLS certificates for secure communication

## Environment-Specific Requirements

### Hyperion HFM

- Access to HFM application server
- HFM user with metadata load permissions
- Registry properties file access

### Hyperion Planning

- Access to Planning application server
- Planning user with administrator privileges
- Ability to generate encrypted password files

### Oracle Cloud EPM

- EPM Automate utility installed
- Valid cloud service credentials
- Network access to Oracle Cloud infrastructure

## Pre-Installation Checklist

Before installing the agent, verify:

- [ ] Operating system meets requirements
- [ ] Java is installed and in PATH
- [ ] Required ports are open
- [ ] User accounts are created
- [ ] Target application credentials are available
- [ ] Network connectivity to EPMware is confirmed
- [ ] Sufficient disk space is available
- [ ] Cygwin is installed (Windows only)

!!! tip "Performance Considerations"
    For environments with multiple target applications or high-volume metadata operations, consider dedicating a server specifically for the EPMware Agent to ensure optimal performance.

!!! warning "Java Version"
    Ensure Java version compatibility with both the EPMware Agent and your target applications. Some older EPM applications may require specific Java versions.

## Next Steps

Once you've confirmed your environment meets these requirements:

1. Review the [Architecture Overview](architecture.md)
2. Proceed to [Installation Prerequisites](../installation/prerequisites/index.md)
3. Begin the [Agent Installation](../installation/agent/index.md) process
# EPMware Agent Installation Guide

Welcome to the EPMware Agent Installation Guide. This comprehensive documentation provides detailed instructions for installing, configuring, and managing the EPMware On-Premise Agent.

## About the EPMware Agent

The EPMware On-Premise Agent enables secure integration between EPMware Cloud applications and your on-premise target applications. It acts as a bridge, allowing EPMware to deploy metadata to your Hyperion Financial Management (HFM), Essbase, Planning, and Oracle Cloud EPM applications without direct network exposure.

## What's in This Guide

<div class="grid cards" markdown>

- :material-download: **Installation**  
  Step-by-step instructions for installing the agent on Windows and Linux servers
  
- :material-cog: **Configuration**  
  Detailed configuration settings for agent properties, REST tokens, and service setup
  
- :material-server: **Application Integration**  
  Specific setup instructions for HFM, Planning, PCMCS, and other EPM applications
  
- :material-wrench: **Troubleshooting**  
  Solutions to common issues and debugging techniques

</div>

## Key Features

- **Secure Communication** - REST API-based authentication with encrypted tokens
- **Multi-Platform Support** - Compatible with Windows and Linux operating systems
- **Application Support** - Integrates with Hyperion HFM, Planning, Essbase, and Oracle Cloud EPM
- **Automated Deployment** - Scheduled metadata deployments with configurable polling intervals
- **Comprehensive Logging** - Detailed logs for monitoring and troubleshooting

## Prerequisites

Before installing the EPMware Agent, ensure you have:

- [ ] Java 1.8 or higher installed
- [ ] Administrative access to the target server
- [ ] Network connectivity to EPMware application (port 443 for cloud, configurable for on-premise)
- [ ] Cygwin installed (for Windows servers)
- [ ] Valid EPMware user account with REST API token

## Quick Start

1. **[Download](installation/agent/download.md)** the EPMware Agent package
2. **[Install Prerequisites](installation/prerequisites/index.md)** (Cygwin for Windows, Java)
3. **[Configure](configuration/agent-properties.md)** the agent properties
4. **[Test](configuration/testing.md)** the connection to EPMware
5. **[Schedule](management/windows/scheduled-tasks.md)** the agent as a service

## Support

For additional assistance, please contact:

- **Email**: support@epmware.com
- **Phone**: 408-614-0442
- **Website**: [www.epmware.com](https://www.epmware.com)

## Document Information

- **Version**: 1.7
- **Updated**: November 2023
- **Copyright**: © 2023 EPMware, Inc. All rights reserved.

!!! note "License Agreement"
    This document and the software described herein are proprietary to EPMware, Inc. and are protected by copyright and other intellectual property laws. Use is subject to the license agreement between you and EPMware, Inc.
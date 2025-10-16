# Introduction

## Overview

EPMware is a master data management and workflow tool that manages master data and enforces your organization's workflow around the everyday processes that surround your metadata changes. By configuring shared dimensions in EPMware, users request metadata once and our workflow engine routes the request to obtain approvals and deploys the metadata to the participating target systems.

## Key Capabilities

### Centralized Metadata Management

- **Single Source of Truth** - Standardization and rationalization of metadata across all EPM applications
- **Workflow Automation** - Automated routing of metadata requests through approval stages
- **Real-time Dashboard** - Monitor request status from creation through review, approval, and deployment
- **Visual Workflow** - Graphical representation of each request's progress

### Seamless Integration

EPMware provides seamless integration with:

- Hyperion Financial Management (HFM)
- Hyperion Planning
- Essbase
- Oracle Cloud EPM applications
- PCMCS (Profitability and Cost Management Cloud Service)

### Security and Compliance

- **LDAP/Active Directory Integration** - Leverages existing enterprise security infrastructure
- **Complete Audit Trail** - Every transaction, sign-off, and deployment is logged
- **Role-based Access Control** - Configurable security module with granular permissions

## Purpose of This Guide

This guide provides comprehensive instructions for:

- Installing the EPMware On-Premise Agent
- Configuring agent connectivity and properties
- Setting up integration with target applications
- Managing and monitoring agent operations
- Troubleshooting common issues

## Target Audience

This guide is intended for:

- System Administrators
- EPM Application Administrators
- IT Infrastructure Teams
- Technical Consultants

## Document Conventions

Throughout this guide, we use the following conventions:

!!! note
    Important information or tips that help you use the product more effectively

!!! warning
    Critical information that could prevent data loss or system issues

!!! tip
    Best practices and recommendations for optimal configuration

```bash
# Command line examples are shown in code blocks
java -version
```

## Related Documentation

- EPMware Logic Builder Guide
- EPMware Administration Guide
- EPMware User Guide
- EPMware API Reference

## Next Steps

- Review [System Requirements](requirements.md) to ensure your environment meets prerequisites
- Understand the [Architecture Overview](architecture.md) to see how the agent fits into your infrastructure
- Proceed to [Installation](../installation/index.md) to begin setting up the agent
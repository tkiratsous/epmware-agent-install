# Hyperion HFM Configuration

## Overview

This section provides specific configuration steps for integrating the EPMware Agent with Oracle Hyperion Financial Management (HFM) applications. HFM requires additional configuration beyond the standard agent setup.

## Prerequisites

Before configuring HFM integration:

- [ ] EPMware Agent is installed and configured
- [ ] HFM application server access is available
- [ ] HFM user account with appropriate permissions exists
- [ ] Registry properties file location is known

## Registry Properties Configuration

### Understanding Registry Properties

The `reg.properties` file contains HFM instance configuration that the agent needs to communicate with HFM applications. This file must be copied to a specific location for the agent to function properly.

### Locating the Registry File

The `reg.properties` file is located in the Foundation configuration directory:

**Standard Location:**
```
[MIDDLEWARE]\user_projects\config\foundation\11.1.2.0\reg.properties
```

**Example Paths:**
- Windows: `D:\Oracle\Middleware\user_projects\config\foundation\11.1.2.0\`
- Linux: `/opt/Oracle/Middleware/user_projects/config/foundation/11.1.2.0/`

![Registry Properties Location](../../assets/images/integration/hfm-registry-location.png)<br/>
*Location of reg.properties in the Foundation directory*

### Copying Registry Properties

!!! warning "Critical Step"
    This step is mandatory for HFM integration. The agent will fail to communicate with HFM without the registry file in the correct location.

#### Step 1: Identify Source and Destination

**Source Path:**
```
[MIDDLEWARE]\user_projects\config\foundation\11.1.2.0\reg.properties
```

**Destination Path:**
```
[MIDDLEWARE]\user_projects\[EPM_INSTANCE]\config\foundation\11.1.2.0\
```

Where `[EPM_INSTANCE]` is typically `epmsystem1` or your custom instance name.

#### Step 2: Copy the File

**Windows Command:**
```cmd
copy D:\Oracle\Middleware\user_projects\config\foundation\11.1.2.0\reg.properties ^
     D:\Oracle\Middleware\user_projects\epmsystem1\config\foundation\11.1.2.0\
```

**Linux Command:**
```bash
cp /opt/Oracle/Middleware/user_projects/config/foundation/11.1.2.0/reg.properties \
   /opt/Oracle/Middleware/user_projects/epmsystem1/config/foundation/11.1.2.0/
```

#### Step 3: Verify File Permissions

Ensure the agent user has read access to the copied file:

**Windows:**
```cmd
icacls D:\Oracle\Middleware\user_projects\epmsystem1\config\foundation\11.1.2.0\reg.properties
```

**Linux:**
```bash
ls -la /opt/Oracle/Middleware/user_projects/epmsystem1/config/foundation/11.1.2.0/reg.properties
```

## HFM Application Configuration in EPMware

### Adding HFM Application

1. Navigate to **Configuration** → **Applications** in EPMware
2. Click **Add Application**
3. Configure HFM-specific settings:

| Field | Value |
|-------|-------|
| **Application Name** | Your HFM application name |
| **Application Type** | HFM |
| **Server** | Select configured HFM server |
| **Cluster** | HFM cluster name (if applicable) |
| **Database** | HFM application database |

![HFM Application Configuration](../../assets/images/integration/hfm-application-config.png)<br/>
*HFM application configuration in EPMware*

### HFM Connection Parameters

Configure the following connection parameters:

| Parameter | Description | Example |
|-----------|-------------|---------|
| **HFM_SERVER** | HFM application server hostname | `hfmserver.domain.com` |
| **HFM_CLUSTER** | HFM cluster name | `Cluster1` |
| **HFM_APP** | HFM application name | `HFMPROD` |
| **HFM_USER** | Service account username | `hfm_admin` |
| **HFM_PASSWORD** | Encrypted password | `{encrypted}...` |

## HFM User Configuration

### Creating HFM Service Account

Create a dedicated service account for EPMware operations:

1. **In HFM Shared Services:**
   - Create new user (e.g., `svc_epmware`)
   - Assign to appropriate groups

2. **Required Roles:**
   - Application Administrator
   - Metadata Load
   - Dimension Editor
   - Rules Load (if managing rules)

### Provisioning User Access

```sql
-- Example provisioning in Shared Services
GRANT HFM_APPLICATION_ADMIN TO svc_epmware;
GRANT HFM_METADATA_LOAD TO svc_epmware;
GRANT HFM_DIMENSION_EDITOR TO svc_epmware;
```

## HFM-Specific Agent Properties

Add HFM-specific settings to `agent.properties`:

```properties
# HFM Configuration
hfm.timeout.seconds=3600
hfm.batch.size=1000
hfm.validation.enabled=true
hfm.backup.before.deploy=true
hfm.log.verbose=false
```

### Configuration Options

| Property | Description | Default |
|----------|-------------|---------|
| `hfm.timeout.seconds` | Maximum time for HFM operations | 3600 |
| `hfm.batch.size` | Records per batch for large deployments | 1000 |
| `hfm.validation.enabled` | Validate metadata before deployment | true |
| `hfm.backup.before.deploy` | Create backup before deployment | true |
| `hfm.log.verbose` | Enable detailed HFM logging | false |

## HFM Utilities Configuration

### Required HFM Utilities

The agent uses these HFM utilities:

| Utility | Purpose | Location |
|---------|---------|----------|
| **LoadMetadata.bat** | Load metadata files | `[EPM_ORACLE_HOME]/products/FinancialManagement/bin` |
| **ExtractMetadata.bat** | Extract metadata | `[EPM_ORACLE_HOME]/products/FinancialManagement/bin` |
| **LoadRules.bat** | Load calculation rules | `[EPM_ORACLE_HOME]/products/FinancialManagement/bin` |

### Path Configuration

Ensure utilities are accessible:

```bash
# Add to system PATH
export PATH=$PATH:/opt/Oracle/Middleware/EPMSystem11R1/products/FinancialManagement/bin

# Or specify in agent.properties
hfm.utility.path=/opt/Oracle/Middleware/EPMSystem11R1/products/FinancialManagement/bin
```

## Testing HFM Integration

### Step 1: Test Utility Access

Verify the agent can access HFM utilities:

```bash
# From agent directory
cd /home/epmware_agent
./test_hfm_utilities.sh
```

### Step 2: Test HFM Connection

Test connection to HFM application:

```bash
# Using EPMware test script
java -jar epmware-agent.jar --test-hfm \
  --app HFMPROD \
  --user svc_epmware \
  --server hfmserver.domain.com
```

### Step 3: Test Metadata Extract

Perform a test metadata extraction:

```bash
# Extract sample metadata
ExtractMetadata.bat -a:HFMPROD -u:svc_epmware -p:password \
  -e:Entity -f:entity_test.xml
```

Expected output:
```
Connecting to HFM application...
Extracting Entity dimension...
Extract completed successfully
File created: entity_test.xml
```

### Step 4: Verify in EPMware

1. Navigate to **Infrastructure** → **Servers** in EPMware
2. Right-click on HFM server
3. Select **Test Connection**

![Test HFM Connection](../../assets/images/integration/hfm-test-connection.png)<br/>
*Testing HFM connection from EPMware*

## HFM Deployment Configuration

### Deployment Options

Configure HFM deployment preferences in EPMware:

| Option | Description | Recommended |
|--------|-------------|-------------|
| **Replace Mode** | Replace entire dimension | Use with caution |
| **Merge Mode** | Merge changes only | ✓ Recommended |
| **Validate Only** | Test without deployment | For testing |
| **Zero Base Load** | Clear before loading | Special cases only |

### Metadata File Formats

HFM supports these metadata formats:

| Format | Extension | Use Case |
|--------|-----------|----------|
| **XML** | `.xml` | Standard metadata loads |
| **APP** | `.app` | Application definitions |
| **RLE** | `.rle` | Calculation rules |
| **SEC** | `.sec` | Security classes |

## Troubleshooting HFM Integration

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Registry file not found | File not copied to EPM instance | Copy reg.properties to correct location |
| Connection timeout | Network or firewall issues | Check port 19000 (default HFM port) |
| Permission denied | Insufficient HFM privileges | Review user provisioning |
| Utility not found | Path not configured | Add HFM bin to system PATH |

### HFM-Specific Log Files

Check these logs for HFM issues:

```bash
# Agent logs
tail -f /home/epmware_agent/logs/agent.log | grep HFM

# HFM logs
tail -f $EPM_ORACLE_INSTANCE/diagnostics/logs/FinancialManagement/HFM.log

# Windows Event Log (Windows only)
eventvwr.msc → Applications and Services → HFM
```

### Debug Mode

Enable HFM debug logging:

```properties
# In agent.properties
hfm.log.verbose=true
hfm.debug.enabled=true
hfm.trace.operations=true
```

## Performance Optimization

### Batch Processing

Optimize large deployments:

```properties
# Batch configuration
hfm.batch.enabled=true
hfm.batch.size=5000
hfm.batch.parallel=false
hfm.batch.commit.interval=1000
```

### Memory Configuration

For large HFM applications:

```properties
# JVM memory for HFM operations
hfm.jvm.xms=2048m
hfm.jvm.xmx=4096m
hfm.jvm.maxpermsize=512m
```

### Connection Pooling

Configure connection pooling:

```properties
# Connection pool settings
hfm.pool.enabled=true
hfm.pool.min=1
hfm.pool.max=5
hfm.pool.timeout=30000
```

## Security Considerations

### Encrypted Passwords

Never store plain text passwords:

1. Generate encrypted password:
```bash
java -jar epmware-agent.jar --encrypt-password
```

2. Store in configuration:
```properties
hfm.password={encrypted}AES256:1a2b3c4d...
```

### Secure File Transfer

For metadata files:
- Use secure protocols (SFTP/SCP)
- Implement file encryption
- Clean up temporary files

### Audit Configuration

Enable comprehensive auditing:

```properties
# Audit settings
hfm.audit.enabled=true
hfm.audit.detailed=true
hfm.audit.include.data=false
hfm.audit.retention.days=90
```

## Best Practices

### Regular Maintenance

1. **Weekly Tasks:**
   - Review deployment logs
   - Check error rates
   - Monitor performance metrics

2. **Monthly Tasks:**
   - Clean up temporary files
   - Archive old logs
   - Review user permissions

3. **Quarterly Tasks:**
   - Update HFM utilities if needed
   - Review security settings
   - Performance tuning

### Backup Strategy

Implement automated backups:

```bash
#!/bin/bash
# Backup before deployment
BACKUP_DIR="/backups/hfm/$(date +%Y%m%d)"
mkdir -p $BACKUP_DIR
ExtractMetadata.bat -a:$HFM_APP -all -f:$BACKUP_DIR/backup.xml
```

### Monitoring Setup

Configure monitoring alerts:

| Metric | Threshold | Action |
|--------|-----------|--------|
| Deployment failure rate | >5% | Alert administrators |
| Connection timeout | >3 in 1 hour | Check network/server |
| Deployment duration | >2x average | Review performance |
| Log file size | >1GB | Archive and rotate |

## Next Steps

After configuring HFM integration:

1. [Configure Planning Integration](../planning/index.md) if using Planning
2. [Set up Cloud EPM](../cloud/index.md) for cloud applications
3. [Configure Monitoring](../../management/monitoring.md)
4. [Review Troubleshooting Guide](../../troubleshooting/index.md)
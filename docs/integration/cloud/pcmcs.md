# PCMCS Configuration

This guide covers the specific configuration for integrating EPMware Agent with Oracle Profitability and Cost Management Cloud Service (PCMCS).

## Overview

PCMCS integration allows EPMware to:
- Deploy dimension metadata
- Manage calculation rules
- Import and export POV data
- Execute calculations
- Manage application settings

## Architecture Options

### Option 1: EPMware Cloud Server

```mermaid
graph LR
    A[EPMware Cloud] --> B[EPMware AWS Server]
    B --> C[EPM Automate]
    C --> D[Oracle PCMCS]
```

### Option 2: Customer On-Premise Server

```mermaid
graph LR
    A[EPMware Cloud] --> B[Customer Server]
    B --> C[EPM Automate]
    C --> D[Oracle PCMCS]
```

![PCMCS Architecture Options](../../assets/images/integration/pcmcs-architecture-options.png)<br/>
*Two deployment options for PCMCS integration*

## Prerequisites

### Required Components

| Component | Requirement | Location |
|-----------|------------|----------|
| EPM Automate | Latest version | Agent server |
| Internet Access | Outbound HTTPS | Port 443 |
| PCMCS Subscription | Active | Oracle Cloud |
| Service Administrator | Role assigned | Identity domain |

### EPM Automate Installation

#### Windows Installation

```powershell
# Download EPM Automate installer
# Default installation path
C:\Oracle\EPM Automate\

# Add to PATH
$env:PATH += ";C:\Oracle\EPM Automate\bin"
```

#### Linux Installation

```bash
# Download and extract
wget https://download-url/EPMAutomate.tar
tar xf EPMAutomate.tar -C ~/

# Set environment
export JAVA_HOME=/usr/java/latest
export PATH=$PATH:~/epmautomate/bin

# Verify installation
epmautomate --version
```

## PCMCS-Specific Configuration

### Connection Setup

```bash
# PCMCS connection format
epmautomate login ServiceAdmin password https://pcmcs-test-a123456.epm.em3.oraclecloud.com

# Components:
# - ServiceAdmin: Your service administrator username
# - password: Account password
# - URL: Your PCMCS instance URL
```

### Agent Configuration

Add to `agent.properties`:

```properties
# PCMCS configuration
pcmcs.enabled=true
pcmcs.url=https://pcmcs-test-a123456.epm.em3.oraclecloud.com
pcmcs.user=ServiceAdmin
pcmcs.identityDomain=mycompany
pcmcs.epmautomate.path=/home/epmware/epmautomate/bin

# PCMCS-specific settings
pcmcs.application=PCMAPP
pcmcs.database=Database1
pcmcs.timeout=7200000
```

### Directory Structure

Create the EPM Automate directory structure:

```bash
# Create EPM Automate directory
mkdir -p ~/epmautomate

# Expected structure
home/epmware/
├── epmautomate/
│   ├── bin/
│   │   ├── epmautomate.sh
│   │   └── epmautomate.bat
│   ├── lib/
│   └── jre/
├── agent.properties
└── ew_target_service.sh
```

![EPM Automate Directory Structure](../../assets/images/integration/epmautomate-directory.png)<br/>
*EPM Automate directory structure under agent home*

## PCMCS Operations

### Dimension Management

#### Upload Dimensions

```bash
# Upload dimension file
epmautomate uploadfile dimensions.csv

# Import dimensions
epmautomate importdimension dimensions.csv

# Delete uploaded file
epmautomate deletefile dimensions.csv
```

#### Export Dimensions

```bash
# Export all dimensions
epmautomate exportdimension ALL dimensions_backup.csv

# Export specific dimension
epmautomate exportdimension Account account_dim.csv

# Download exported file
epmautomate downloadfile dimensions_backup.csv
```

### Rule Management

#### Deploy Calculation Rules

```bash
# Upload rule file
epmautomate uploadfile calc_rules.txt

# Import rules
epmautomate importrules calc_rules.txt REPLACE

# Validate rules
epmautomate validaterules
```

#### Execute Calculations

```bash
# Run calculation
epmautomate runpcmcalc POV="Year=FY21,Period=Jan,Scenario=Actual"

# Check calculation status
epmautomate getpcmcalcstatus

# Download calc results
epmautomate downloadfile calculation_results.csv
```

### Data Management

#### Import Data

```bash
# Upload data file
epmautomate uploadfile data.csv

# Import data
epmautomate importpcmdata data.csv

# Import with options
epmautomate importpcmdata data.csv REPLACE=true VALIDATEONLY=false
```

#### Export Data

```bash
# Export data for POV
epmautomate exportpcmdata "Year=FY21,Period=Jan" output.csv

# Export all data
epmautomate exportpcmdata ALL full_export.csv

# Download exported data
epmautomate downloadfile full_export.csv
```

## PCMCS Application Tasks

### Application Management

```bash
# Get application status
epmautomate getpcmstatus

# List POVs
epmautomate listpovs

# Clear POV data
epmautomate clearpcmdata "Year=FY21,Period=Jan"

# Reset application
epmautomate resetpcmapplication
```

### Model Management

```bash
# Export model
epmautomate exportpcmmodel model_backup.zip

# Import model
epmautomate importpcmmodel model.zip

# Validate model
epmautomate validatepcmmodel
```

## Automation Scripts

### Deployment Script

```bash
#!/bin/bash
# deploy_pcmcs.sh

# Configuration
URL="https://pcmcs-instance.oraclecloud.com"
USER="ServiceAdmin"
PASSWORD="password"
DIMENSION_FILE="dimensions.csv"

# Login
echo "Logging into PCMCS..."
epmautomate login $USER $PASSWORD $URL || exit 1

# Backup existing dimensions
echo "Backing up dimensions..."
epmautomate exportdimension ALL backup_$(date +%Y%m%d).csv

# Upload new dimensions
echo "Uploading new dimensions..."
epmautomate uploadfile $DIMENSION_FILE

# Import dimensions
echo "Importing dimensions..."
epmautomate importdimension $DIMENSION_FILE

# Validate
echo "Validating..."
epmautomate validatedimension

# Clean up
epmautomate deletefile $DIMENSION_FILE

# Logout
epmautomate logout

echo "Deployment complete!"
```

### Backup Script

```bash
#!/bin/bash
# backup_pcmcs.sh

BACKUP_DIR="/backup/pcmcs/$(date +%Y%m%d)"
mkdir -p $BACKUP_DIR

# Login
epmautomate login $USER $PASSWORD $URL

# Export dimensions
epmautomate exportdimension ALL $BACKUP_DIR/dimensions.csv

# Export rules
epmautomate exportrules $BACKUP_DIR/rules.txt

# Export model
epmautomate exportpcmmodel $BACKUP_DIR/model.zip

# Export data
epmautomate exportpcmdata ALL $BACKUP_DIR/data.csv

# Download all files
for file in dimensions.csv rules.txt model.zip data.csv; do
    epmautomate downloadfile $file $BACKUP_DIR/$file
done

# Logout
epmautomate logout
```

## Testing and Validation

### Connection Test

```bash
#!/bin/bash
# test_pcmcs_connection.sh

echo "Testing PCMCS connection..."

# Test login
if epmautomate login $USER $PASSWORD $URL; then
    echo "✓ Login successful"
    
    # Test operations
    epmautomate listfiles
    echo "✓ List files successful"
    
    epmautomate getpcmstatus
    echo "✓ Get status successful"
    
    # Logout
    epmautomate logout
    echo "✓ Logout successful"
else
    echo "✗ Login failed"
    exit 1
fi
```

### Deployment Validation

```bash
# Validate dimension import
epmautomate validatedimension

# Check for errors
epmautomate getjoberrors

# Review import log
epmautomate downloadfile import.log
```

## Performance Optimization

### Batch Processing

```bash
# Process multiple files
for file in *.csv; do
    epmautomate uploadfile "$file"
    epmautomate importdimension "$file"
    epmautomate deletefile "$file"
done
```

### Compression

```bash
# Compress before upload
gzip -9 large_data.csv
epmautomate uploadfile large_data.csv.gz

# PCMCS automatically handles .gz files
epmautomate importpcmdata large_data.csv.gz
```

### Parallel Processing

```bash
# Upload files in parallel
ls *.csv | xargs -P 4 -I {} epmautomate uploadfile {}
```

## Troubleshooting

### Common PCMCS Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Login fails | Wrong URL format | Verify full URL including https:// |
| Import fails | Invalid data format | Check CSV format and encoding |
| Timeout errors | Large data sets | Increase timeout or split files |
| Permission denied | Insufficient role | Verify Service Administrator role |
| Connection reset | Proxy issues | Configure proxy settings |

### Debug Logging

```bash
# Enable debug mode
export EPM_AUTOMATE_LOG_LEVEL=DEBUG

# Run with verbose output
epmautomate login $USER $PASSWORD $URL -v

# Check logs
tail -f ~/epmautomate/logs/epmautomate.log
```

### Error Recovery

```bash
#!/bin/bash
# recover_failed_import.sh

# Check for failed jobs
epmautomate listjobs | grep FAILED

# Get error details
epmautomate getjoberrors > errors.log

# Retry failed imports
if grep -q "dimension import failed" errors.log; then
    echo "Retrying dimension import..."
    epmautomate importdimension dimensions.csv
fi
```

## Security Considerations

### Password Management

```bash
# Use encrypted password file
openssl enc -aes-256-cbc -salt -in password.txt -out password.enc

# Use in script
PASSWORD=$(openssl enc -aes-256-cbc -d -in password.enc)
epmautomate login $USER $PASSWORD $URL
```

### Audit Logging

```properties
# Enable audit logging
pcmcs.audit.enabled=true
pcmcs.audit.operations=true
pcmcs.audit.data.changes=true
```

### Secure Communication

```bash
# Verify TLS version
openssl s_client -connect pcmcs-instance.oraclecloud.com:443 -tls1_2

# Check certificate
openssl s_client -connect pcmcs-instance.oraclecloud.com:443 -showcerts
```

## Maintenance Tasks

### Regular Maintenance

```bash
#!/bin/bash
# maintenance_pcmcs.sh

# Login
epmautomate login $USER $PASSWORD $URL

# Clean up old files
epmautomate listfiles | grep "backup_" | while read file; do
    FILE_DATE=$(echo $file | grep -oE '[0-9]{8}')
    if [[ $FILE_DATE < $(date -d '30 days ago' +%Y%m%d) ]]; then
        epmautomate deletefile "$file"
    fi
done

# Optimize application
epmautomate optimizepcmapplication

# Logout
epmautomate logout
```

### EPM Automate Updates

```bash
# Check for updates
epmautomate upgrade

# Auto-upgrade
epmautomate upgrade -f

# Verify version after upgrade
epmautomate --version
```

## Best Practices

### PCMCS-Specific Guidelines

1. **Always backup before changes** - Export dimensions and data
2. **Use validation mode** - Test imports before applying
3. **Monitor job status** - Check for failures immediately
4. **Implement retry logic** - Handle transient failures
5. **Clean up files** - Delete uploaded files after processing

### Performance Tips

1. **Batch small changes** - Group related updates
2. **Split large files** - Files over 100MB
3. **Schedule off-hours** - Reduce user impact
4. **Use compression** - For large data files
5. **Monitor execution time** - Track performance trends

## Integration Checklist

Before production deployment:

- [ ] EPM Automate installed and updated
- [ ] Connection to PCMCS verified
- [ ] Service Administrator role assigned
- [ ] Backup procedures implemented
- [ ] Error handling in scripts
- [ ] Monitoring configured
- [ ] Documentation updated
- [ ] Recovery procedures tested
- [ ] Security measures in place
- [ ] Performance benchmarked

!!! tip "Version Management"
    Keep EPM Automate updated to ensure compatibility with the latest PCMCS features. Oracle releases updates monthly.

!!! warning "Data Validation"
    Always validate dimension and data files before importing to prevent application corruption. Use VALIDATEONLY=true for testing.

## Next Steps

- [EPM Automate Setup](epm-automate.md) - Detailed utility configuration
- [Upgrade Process](upgrade.md) - Keep tools current
- [Cloud Integration Overview](index.md) - Other cloud services
- [Troubleshooting](../../troubleshooting/index.md) - Resolve issues
# Planning Application Properties

This guide covers the configuration of Planning-specific properties in EPMware for successful integration with Hyperion Planning applications.

## Overview

Application properties define how EPMware interacts with Planning applications, including:
- Connection parameters
- Authentication settings
- Deployment options
- Performance tuning
- Error handling

## EPMware Application Configuration

### Accessing Application Properties

1. Log into EPMware
2. Navigate to **Configuration** → **Applications**
3. Select your Planning application
4. Click **Edit Properties** or right-click → **Properties**

![Application Properties Screen](../../assets/images/integration/planning-app-properties.png)<br/>
*Planning application properties in EPMware*

### Core Properties

| Property | Description | Example | Required |
|----------|-------------|---------|----------|
| **APPLICATION_NAME** | Planning application name | PLANPROD | Yes |
| **SERVER** | Planning server hostname | planning.company.com | Yes |
| **PORT** | RMI Registry port | 11333 | Yes |
| **USER** | Planning admin username | admin | Yes |
| **PASSWORD_FILE** | Encrypted password file path | /opt/secure/planning_pwd.txt | Yes |
| **ESSBASE_SERVER** | Associated Essbase server | essbase.company.com | Yes |
| **ESSBASE_APP** | Essbase application name | PLANPROD | Yes |

## Connection Properties

### Server Configuration

```properties
# Server connection properties
planning.server=planning.company.com
planning.port=11333
planning.protocol=RMI
planning.timeout=3600000
planning.retry.count=3
planning.retry.delay=5000
```

### Authentication Properties

```properties
# Authentication settings
planning.user=admin
planning.passwordFile=/opt/secure/planning/planning_pwd.txt
planning.authentication.type=NATIVE
planning.session.timeout=1800000
```

### Essbase Integration

```properties
# Essbase connection
planning.essbase.server=essbase.company.com
planning.essbase.port=1423
planning.essbase.application=PLANPROD
planning.essbase.database=Plan1
planning.essbase.refresh=true
```

## Deployment Properties

### Metadata Loading Options

```properties
# OutlineLoad options
planning.outlineload.path=/opt/Oracle/products/Planning/bin/OutlineLoad.sh
planning.outlineload.logLevel=INFO
planning.outlineload.delimiter=,
planning.outlineload.loadMethod=/L
planning.outlineload.refreshDatabase=true
```

### Load Methods

| Method | Property Value | Description |
|--------|---------------|-------------|
| Load | `/L` | Add new members (default) |
| Replace | `/R` | Replace entire dimension |
| Update | `/M` | Update member properties |
| Delete | `/D` | Remove members |

### Validation Settings

```properties
# Validation properties
planning.validation.enabled=true
planning.validation.stopOnError=true
planning.validation.logErrors=true
planning.validation.maxErrors=100
```

## Performance Properties

### Batch Processing

```properties
# Batch configuration
planning.batch.enabled=true
planning.batch.size=1000
planning.batch.commitInterval=5000
planning.batch.parallel=false
planning.batch.threads=4
```

### Memory Configuration

```properties
# JVM settings for OutlineLoad
planning.jvm.xms=1024m
planning.jvm.xmx=2048m
planning.jvm.maxPermSize=256m
planning.jvm.gc=G1GC
```

### Connection Pooling

```properties
# Connection pool
planning.pool.enabled=true
planning.pool.minSize=2
planning.pool.maxSize=10
planning.pool.timeout=30000
planning.pool.validate=true
```

## Advanced Properties

### Custom Properties

```properties
# Custom dimension properties
planning.dimension.Entity.dataStorage=StoreData
planning.dimension.Account.twoPassCalc=true
planning.dimension.Version.securityEnabled=false

# UDA assignments
planning.uda.Entity=CostCenter,Region
planning.uda.Account=Revenue,Expense
```

### Business Rule Properties

```properties
# Business rule execution
planning.businessrule.enabled=true
planning.businessrule.runtime.prompts=true
planning.businessrule.sequence=Calculate,Aggregate,Allocate
planning.businessrule.timeout=7200000
```

### Form Management

```properties
# Form properties
planning.forms.export.enabled=true
planning.forms.import.validate=true
planning.forms.backup.before.import=true
```

## Environment-Specific Properties

### Development Environment

```properties
# Development settings
planning.dev.server=dev-planning.company.com
planning.dev.application=PLANDEV
planning.dev.passwordFile=/opt/secure/planning/dev_pwd.txt
planning.dev.debug=true
planning.dev.validation.stopOnError=false
```

### Production Environment

```properties
# Production settings
planning.prod.server=prod-planning.company.com
planning.prod.application=PLANPROD
planning.prod.passwordFile=/opt/secure/planning/prod_pwd.txt
planning.prod.debug=false
planning.prod.validation.stopOnError=true
planning.prod.backup.required=true
```

## Property Management

### Setting Properties via UI

```markdown
1. Navigate to Configuration → Applications
2. Select Planning application
3. Right-click → Edit Properties
4. Add/Modify property:
   - Name: planning.batch.size
   - Value: 1000
5. Click Save
```

### Setting Properties via Script

```bash
#!/bin/bash
# set_planning_properties.sh

# EPMware API endpoint
API_URL="https://epmware.company.com/api/v1"
TOKEN="your-api-token"

# Set property
curl -X POST "$API_URL/applications/PLANPROD/properties" \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "planning.batch.size",
       "value": "1000"
     }'
```

### Bulk Property Import

```csv
# planning_properties.csv
Property,Value,Description
planning.server,planning.company.com,Planning server
planning.port,11333,RMI port
planning.user,admin,Admin user
planning.passwordFile,/opt/secure/pwd.txt,Password file
planning.batch.size,1000,Batch size
```

```bash
# Import properties
curl -X POST "$API_URL/applications/PLANPROD/properties/import" \
     -H "Authorization: Bearer $TOKEN" \
     -F "file=@planning_properties.csv"
```

## Property Validation

### Validation Script

```bash
#!/bin/bash
# validate_planning_properties.sh

echo "=== Planning Properties Validation ==="

# Required properties
REQUIRED_PROPS=(
    "APPLICATION_NAME"
    "SERVER"
    "USER"
    "PASSWORD_FILE"
)

# Check each property
for prop in "${REQUIRED_PROPS[@]}"; do
    VALUE=$(grep "^$prop=" application.properties | cut -d= -f2)
    
    if [ -n "$VALUE" ]; then
        echo "✓ $prop = $VALUE"
    else
        echo "✗ Missing: $prop"
    fi
done

# Validate password file
PASSWORD_FILE=$(grep "^PASSWORD_FILE=" application.properties | cut -d= -f2)
if [ -f "$PASSWORD_FILE" ]; then
    echo "✓ Password file exists"
else
    echo "✗ Password file not found: $PASSWORD_FILE"
fi
```

### Connection Test

```bash
#!/bin/bash
# test_planning_connection.sh

# Get properties
source application.properties

# Test connection
OutlineLoad.sh -f:$PASSWORD_FILE /A:$APPLICATION_NAME /U:$USER /V

if [ $? -eq 0 ]; then
    echo "✓ Connection successful"
else
    echo "✗ Connection failed"
fi
```

## Property Templates

### Standard Template

```properties
# planning_template.properties
# Standard Planning application configuration

# Connection
planning.server=${PLANNING_SERVER}
planning.port=11333
planning.timeout=3600000

# Authentication
planning.user=${PLANNING_USER}
planning.passwordFile=${PASSWORD_FILE}

# Essbase
planning.essbase.server=${ESSBASE_SERVER}
planning.essbase.application=${APPLICATION_NAME}
planning.essbase.refresh=true

# Deployment
planning.outlineload.loadMethod=/L
planning.validation.enabled=true
planning.backup.enabled=true

# Performance
planning.batch.size=1000
planning.pool.maxSize=5
```

### High-Performance Template

```properties
# high_performance_template.properties
# Optimized for large deployments

# Batch processing
planning.batch.enabled=true
planning.batch.size=5000
planning.batch.parallel=true
planning.batch.threads=8

# Memory
planning.jvm.xmx=4096m
planning.jvm.gc=G1GC
planning.jvm.gcThreads=4

# Connection pool
planning.pool.maxSize=20
planning.pool.minSize=5

# Timeouts
planning.timeout=7200000
planning.operation.timeout=3600000
```

## Monitoring Properties

### Property Change Tracking

```bash
#!/bin/bash
# track_property_changes.sh

PROP_FILE="application.properties"
HISTORY_FILE="property_history.log"

# Create snapshot
cp $PROP_FILE ${PROP_FILE}.$(date +%Y%m%d_%H%M%S)

# Log changes
echo "=== Property Changes $(date) ===" >> $HISTORY_FILE
diff ${PROP_FILE}.previous $PROP_FILE >> $HISTORY_FILE 2>/dev/null

# Update previous
cp $PROP_FILE ${PROP_FILE}.previous
```

### Property Usage Monitoring

```bash
# Monitor property usage in logs
grep -h "Using property" logs/*.log | \
    awk '{print $NF}' | \
    sort | uniq -c | \
    sort -rn
```

## Troubleshooting Properties

### Common Property Issues

| Issue | Symptom | Solution |
|-------|---------|----------|
| Missing property | "Property not found" | Add required property |
| Invalid value | "Invalid property value" | Check value format |
| Path not found | "File does not exist" | Verify file paths |
| Connection timeout | Operation times out | Increase timeout value |
| Memory issues | OutOfMemory errors | Increase JVM memory |

### Debug Property Loading

```bash
# Enable debug logging
export PLANNING_PROPERTY_DEBUG=true

# Run with verbose output
java -Dplanning.properties.debug=true \
     -jar epmware-agent.jar
```

### Property Precedence

Properties are loaded in this order (later overrides earlier):
1. Default values
2. Application properties file
3. Environment variables
4. Command line arguments

```bash
# Example precedence
# 1. Default: planning.timeout=30000
# 2. File: planning.timeout=60000
# 3. Env: export PLANNING_TIMEOUT=90000
# 4. Cmd: -Dplanning.timeout=120000
# Final value: 120000
```

## Best Practices

### Property Management Guidelines

1. **Use descriptive names** - Clear property naming
2. **Document properties** - Include descriptions
3. **Version control** - Track property changes
4. **Environment separation** - Different configs per environment
5. **Regular review** - Audit and update properties

### Security Practices

1. **No passwords in properties** - Use password files
2. **Encrypt sensitive values** - Use encryption for sensitive data
3. **Restrict access** - Limit who can view/modify
4. **Audit changes** - Log all modifications
5. **Regular rotation** - Update credentials periodically

### Performance Optimization

1. **Tune batch sizes** - Based on data volume
2. **Adjust timeouts** - For network latency
3. **Configure pools** - For concurrent operations
4. **Monitor usage** - Track property effectiveness
5. **Regular testing** - Validate optimal values

!!! tip "Property Documentation"
    Maintain a property reference document listing all custom properties, their purpose, and valid values for your team's reference.

!!! warning "Production Changes"
    Always test property changes in non-production environments first. Some properties require application restart to take effect.

## Next Steps

- [Password Encryption](password-encryption.md) - Set up password files
- [Planning Integration Overview](index.md) - Complete Planning setup
- [HFM Integration](../hfm/index.md) - HFM configuration
- [Troubleshooting](../../troubleshooting/index.md) - Resolve issues
# Multi-Environment Databricks Asset Bundle

This project demonstrates how to use Databricks **Declarative Automation Bundles** to manage DEV, TEST, and PROD environments in a single workspace using Hive metastore (Databricks Free Edition).

## 🎉 Verified Deployments

This bundle has been successfully deployed and tested:

 Environment | Status | Database | Records | Sampling | Job Run Time |
-------------|--------|----------|---------|----------|--------------|
 **DEV** | ✅ Deployed & Tested | `dev_analytics` | 3/5 (60%) | 10% sample | ~23 seconds |
 **TEST** | ✅ Deployed & Tested | `test_analytics` | 5/5 (100%) | 50% sample | ~24 seconds |
 **PROD** | 📋 Ready to Deploy | `prod_analytics` | - | 100% full data | - |

**Workspace**: https://dbc-4b1ecb7b-9c81.cloud.databricks.com  
**Repository**: https://github.com/dineshvrao/rao-innovation-lab.git  
**Bundle Path**: `/Repos/dineshv.rao7@outlook.com/rao-innovation-lab/multi-env-bundle`

## Project Structure

```
multi-env-bundle/
├── databricks.yml              # Main bundle configuration
├── resources/                  # Resource definitions (jobs, pipelines, etc.)
│   └── data_processing_job.yml
├── src/                        # Source code (notebooks, scripts)
│   └── data_processing.py
└── README.md                   # This file
```

## Key Features

### Environment Separation

* **DEV Environment**: Development with 10% data sampling, frequent checkpoints
* **TEST Environment**: Testing with 50% data sampling, validation enabled
* **PROD Environment**: Production with full data processing, optimized performance

### What's Different Per Environment?

1. **Data Isolation**: Separate databases (`dev_analytics`, `test_analytics`, `prod_analytics`)
2. **Resource Naming**: Job names prefixed with `[DEV]`, `[TEST]`, `[PROD]`
3. **Schedules**: Different cron schedules per environment
4. **Processing Logic**: Environment-aware code (sampling rates, validation)
5. **Workspace Paths**: Deployed to separate folders

### Free Edition Configuration

**Important**: This bundle is configured for Databricks Free Edition which uses:
* ✅ **Hive metastore** (not Unity Catalog)
* ✅ **Serverless compute** (no cluster configuration needed)
* ✅ **Database-level isolation** (instead of catalog.schema)
* ✅ **SQL CREATE DATABASE** (instead of CREATE SCHEMA)

## Prerequisites

1. **Clone the Repository**:
   ```bash
   # In Databricks Repos
   git clone https://github.com/dineshvrao/rao-innovation-lab.git
   ```

2. **Install Databricks CLI** (if running from local terminal):
   ```bash
   pip install databricks-cli
   ```

3. **Configure Authentication**:
   ```bash
   databricks auth login --host https://dbc-4b1ecb7b-9c81.cloud.databricks.com
   ```

## Deployment Commands

### Navigate to Bundle Directory

First, make sure you're in the bundle directory:

```bash
cd /Workspace/Repos/dineshv.rao7@outlook.com/rao-innovation-lab/multi-env-bundle
```

### Validate Configuration

Before deploying, validate your bundle:

```bash
# Validate DEV configuration
databricks bundle validate -t dev

# Validate TEST configuration
databricks bundle validate -t test

# Validate PROD configuration
databricks bundle validate -t prod
```

### Deploy to Environments

**Deploy to DEV** (default target):
```bash
databricks bundle deploy -t dev
```

**Deploy to TEST**:
```bash
databricks bundle deploy -t test
```

**Deploy to PROD**:
```bash
# Note: PROD deployment may require manual approval for safety
databricks bundle deploy -t prod
```

### Run Jobs

After deployment, run the job:

```bash
# Run in DEV
databricks bundle run data_processing_job -t dev

# Run in TEST
databricks bundle run data_processing_job -t test

# Run in PROD
databricks bundle run data_processing_job -t prod
```

### View Deployment Status

```bash
# Check what's deployed in DEV
databricks bundle summary -t dev

# Check TEST
databricks bundle summary -t test

# Check PROD
databricks bundle summary -t prod
```

### Destroy Resources

To remove deployed resources:

```bash
# Destroy DEV resources
databricks bundle destroy -t dev

# Destroy TEST resources
databricks bundle destroy -t test

# Destroy PROD resources (use with caution!)
databricks bundle destroy -t prod
```

## Environment Configuration

Each environment has its own variables defined in `databricks.yml`:

 Variable | DEV | TEST | PROD |
----------|-----|------|------|
 `database_name` | dev_analytics | test_analytics | prod_analytics |
 **Data Sampling** | 10% | 50% | 100% |
 **Schedule** | 8 AM daily | 6 AM daily | 2 AM daily |
 **Checkpoint Interval** | 100 | 50 | 1000 |

## Workflow: DEV → TEST → PROD

### Step 1: Develop in DEV ✅ COMPLETED

```bash
# Deploy to dev
cd /Workspace/Repos/dineshv.rao7@outlook.com/rao-innovation-lab/multi-env-bundle
databricks bundle deploy -t dev

# Test your changes
databricks bundle run data_processing_job -t dev

# Verify results
# ✅ Successfully created dev_analytics.processed_data with 3 records
```

### Step 2: Promote to TEST ✅ COMPLETED

```bash
# Deploy to test
databricks bundle deploy -t test

# Run integration tests
databricks bundle run data_processing_job -t test

# Verify results
# ✅ Successfully created test_analytics.processed_data with 5 records
```

### Step 3: Release to PROD 📋 READY

```bash
# After test validation, deploy to prod
databricks bundle deploy -t prod

# Run the production job
databricks bundle run data_processing_job -t prod

# Monitor the job via the returned URL
```

## Verification Results

### DEV Environment ✅

**Job Details**:
* Job Name: `[DEV] multi_env_demo - Data Processing`
* Job ID: 581989555684086
* Database: `dev_analytics`
* Table: `dev_analytics.processed_data`

**Data Verification**:
```sql
USE dev_analytics;
SELECT * FROM processed_data;
```

**Results**:
* Total records: 3 (10% sample of 5 original records)
* Products: Product A ($100), Product C ($200), Product E ($225)
* Average amount: $175
* Environment tag: `dev`
* Processed timestamp: 2026-06-08 23:56:22 UTC

### TEST Environment ✅

**Job Details**:
* Job Name: `[TEST] multi_env_demo - Data Processing`
* Job ID: 752479889624048
* Database: `test_analytics`
* Table: `test_analytics.processed_data`

**Data Verification**:
```sql
USE test_analytics;
SELECT * FROM processed_data;
```

**Results**:
* Total records: 5 (50% sample - all records due to small dataset)
* Products: All 5 products (A through E)
* Average amount: $170
* Environment tag: `test`
* Processed timestamp: 2026-06-08 23:59:20 UTC

### Environment Comparison

```sql
-- Compare all environments
SELECT 
  'DEV' as environment_name,
  COUNT(*) as record_count,
  AVG(amount) as avg_amount
FROM dev_analytics.processed_data

UNION ALL

SELECT 
  'TEST' as environment_name,
  COUNT(*) as record_count,
  AVG(amount) as avg_amount
FROM test_analytics.processed_data

ORDER BY environment_name;
```

**Output**:
 environment_name | record_count | avg_amount |
------------------|--------------|------------|
 DEV | 3 | $175 |
 TEST | 5 | $170 |

## Workspace Deployment Paths

Each environment is deployed to its own workspace folder:

```bash
# DEV resources are in:
/Users/dineshv.rao7@outlook.com/.bundle/multi_env_demo/dev/

# TEST resources are in:
/Users/dineshv.rao7@outlook.com/.bundle/multi_env_demo/test/

# PROD resources are in:
/Users/dineshv.rao7@outlook.com/.bundle/multi_env_demo/prod/
```

## Access Deployed Jobs

After deployment, you can access jobs via these URLs:

* **DEV Job**: https://dbc-4b1ecb7b-9c81.cloud.databricks.com/?o=7474644658813962#job/581989555684086
* **TEST Job**: https://dbc-4b1ecb7b-9c81.cloud.databricks.com/?o=7474644658813962#job/752479889624048
* **PROD Job**: (will be created after PROD deployment)

## Tips for Free Edition

Since this is configured for Databricks Free Edition:

1. ✅ **Serverless compute** - No cluster configuration needed
2. ✅ **Hive metastore** - Uses `CREATE DATABASE` instead of Unity Catalog
3. ✅ **Database-based isolation** - Each environment has its own database
4. ✅ **Job name prefixes** - `[DEV]`, `[TEST]`, `[PROD]` to distinguish environments
5. ✅ **Separate workspace folders** - Each deployment in its own folder
6. ✅ **Tags for tracking** - Environment and project tags on all resources

## Customization

### Add More Environments

You can add staging, QA, or other environments to `databricks.yml`:

```yaml
targets:
  staging:
    mode: production
    workspace:
      root_path: /Users/dineshv.rao7@outlook.com/.bundle/${bundle.name}/staging
    variables:
      database_name: "staging_analytics"
```

### Add More Resources

Create additional resource files in the `resources/` folder:

* `resources/pipeline.yml` - For Lakeflow Spark Declarative Pipelines
* `resources/model_serving.yml` - For ML model serving endpoints
* `resources/dashboards.yml` - For Lakeview dashboards

### Parameterize Notebooks

Notebooks receive parameters via `base_parameters` in the job definition. Access them with:

```python
database_name = dbutils.widgets.get("database_name")
environment = dbutils.widgets.get("environment")
```

## Troubleshooting

### Bundle Validation Fails

```bash
# Get detailed error information
databricks bundle validate -t dev --debug
```

### Job Fails with NO_SUCH_CATALOG_EXCEPTION

**Issue**: Free edition doesn't support Unity Catalog.

**Solution**: This bundle is already configured to use Hive metastore with:
* `CREATE DATABASE` (not `CREATE SCHEMA`)
* Database names without catalog prefix
* Direct table references like `database_name.table_name`

### Resources Not Deployed

```bash
# Force redeployment
databricks bundle deploy -t dev --force
```

### Safety Guardrails Block PROD Deployment

**Issue**: Automated tools may block production deployments for safety.

**Solution**: Run the deployment command manually from terminal:
```bash
databricks bundle deploy -t prod
```

## Best Practices

1. ✅ **Always validate before deploying**: Run `bundle validate` first
2. ✅ **Test in DEV first**: Never deploy directly to PROD
3. ✅ **Use version control**: Commit changes to GitHub before deployment
4. ✅ **Tag resources**: Use tags to track environment and ownership
5. ✅ **Monitor job runs**: Check job logs after each deployment
6. ✅ **Verify data isolation**: Query each database to confirm separation
7. ✅ **Document changes**: Update README with configuration changes

## Git Integration

This bundle is version controlled in GitHub:

**Repository**: https://github.com/dineshvrao/rao-innovation-lab.git

### Commit Changes

```bash
cd /Workspace/Repos/dineshv.rao7@outlook.com/rao-innovation-lab/multi-env-bundle

git add .
git commit -m "Update bundle configuration"
git push origin main
```

### Pull Latest Changes

```bash
git pull origin main
```

## Next Steps

1. ✅ **DEV Deployed** - Successfully tested with 3 records
2. ✅ **TEST Deployed** - Successfully tested with 5 records
3. 📋 **Deploy PROD** - Run `databricks bundle deploy -t prod`
4. 📊 **Add Monitoring** - Set up alerts and dashboards
5. 🔄 **Add CI/CD** - Automate deployments via GitHub Actions
6. 📈 **Add More Jobs** - Extend with additional data processing jobs

## Resources

* [Declarative Automation Bundles Documentation](https://docs.databricks.com/dev-tools/bundles/index.html)
* [Bundle YAML Reference](https://docs.databricks.com/dev-tools/bundles/reference.html)
* [Databricks CLI](https://docs.databricks.com/dev-tools/cli/index.html)
* [GitHub Repository](https://github.com/dineshvrao/rao-innovation-lab.git)

---

**Created**: 2026-06-08  
**Last Updated**: 2026-06-08  
**Environment**: Databricks Free Edition (Hive metastore)  
**Bundle Version**: 1.0  
**Status**: DEV ✅ | TEST ✅ | PROD 📋

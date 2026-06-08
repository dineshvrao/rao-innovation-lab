# Multi-Environment Databricks Asset Bundle

This project demonstrates how to use Databricks Asset Bundles (now called **Declarative Automation Bundles**) to manage DEV, TEST, and PROD environments in a single workspace.

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

1. **Data Isolation**: Separate schemas (`dev_analytics`, `test_analytics`, `prod_analytics`)
2. **Resource Naming**: Job names prefixed with `[DEV]`, `[TEST]`, `[PROD]`
3. **Compute Resources**: Different cluster sizes and worker counts
4. **Schedules**: Different cron schedules per environment
5. **Processing Logic**: Environment-aware code (sampling rates, validation)
6. **Workspace Paths**: Deployed to separate folders

## Prerequisites

1. **Install Databricks CLI**:
   ```bash
   pip install databricks-cli
   ```

2. **Configure Authentication**:
   ```bash
   databricks auth login --host https://dbc-4b1ecb7b-9c81.cloud.databricks.com
   ```

## Deployment Commands

### Navigate to Bundle Directory

First, make sure you're in the bundle directory:

```bash
cd /Workspace/Users/dineshv.rao7@outlook.com/multi-env-bundle
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
databricks bundle deploy
# or explicitly:
databricks bundle deploy -t dev
```

**Deploy to TEST**:
```bash
databricks bundle deploy -t test
```

**Deploy to PROD**:
```bash
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

# Destroy PROD resources
databricks bundle destroy -t prod
```

## Environment Variables

Each environment has its own variables defined in `databricks.yml`:

| Variable | DEV | TEST | PROD |
|----------|-----|------|------|
| `catalog` | main | main | main |
| `schema_prefix` | dev | test | prod |
| `cluster_size` | i3.xlarge | i3.xlarge | i3.2xlarge |
| `max_workers` | 1 | 2 | 4 |
| **Schedule** | 8 AM daily | 6 AM daily | 2 AM daily |

## Workflow: DEV → TEST → PROD

### Step 1: Develop in DEV

```bash
# Deploy to dev
databricks bundle deploy -t dev

# Test your changes
databricks bundle run data_processing_job -t dev

# Make changes, redeploy as needed
databricks bundle deploy -t dev
```

### Step 2: Promote to TEST

```bash
# When ready, deploy to test
databricks bundle deploy -t test

# Run integration tests
databricks bundle run data_processing_job -t test

# Verify results in test schema
spark.sql("SELECT * FROM main.test_analytics.processed_data").show()
```

### Step 3: Release to PROD

```bash
# After test validation, deploy to prod
databricks bundle deploy -t prod

# Monitor the production job
databricks bundle run data_processing_job -t prod
```

## Verification

After deployment, verify the environment separation:

### Check Deployed Jobs

```sql
-- In Databricks SQL or notebook
SELECT * FROM system.compute.jobs 
WHERE job_name LIKE '%multi_env_demo%'
ORDER BY job_name;
```

You should see three jobs:
* `[DEV] multi_env_demo - Data Processing`
* `[TEST] multi_env_demo - Data Processing`
* `[PROD] multi_env_demo - Data Processing`

### Check Data Isolation

```sql
-- Check DEV data
SELECT * FROM main.dev_analytics.processed_data;

-- Check TEST data
SELECT * FROM main.test_analytics.processed_data;

-- Check PROD data
SELECT * FROM main.prod_analytics.processed_data;
```

Each environment's data is isolated in its own schema.

### Check Workspace Deployment Paths

```bash
# DEV resources are in:
/Users/dineshv.rao7@outlook.com/.bundle/multi_env_demo/dev/

# TEST resources are in:
/Users/dineshv.rao7@outlook.com/.bundle/multi_env_demo/test/

# PROD resources are in:
/Users/dineshv.rao7@outlook.com/.bundle/multi_env_demo/prod/
```

## Tips for Free Edition

Since you're using a free edition workspace:

1. **Schema-based isolation** instead of catalog isolation
2. **Job name prefixes** to distinguish environments
3. **Separate workspace folders** for each deployment
4. **Tags** to identify environment ownership
5. **Different schedules** to avoid resource conflicts

## Customization

### Add More Environments

You can add staging, QA, or other environments:

```yaml
targets:
  staging:
    mode: production
    workspace:
      root_path: /Users/dineshv.rao7@outlook.com/.bundle/${bundle.name}/staging
    variables:
      schema_prefix: "staging"
      max_workers: 2
```

### Add More Resources

Create additional resource files in the `resources/` folder:

* `resources/pipeline.yml` - For Lakeflow Spark Declarative Pipelines
* `resources/model_serving.yml` - For ML model serving endpoints
* `resources/dashboards.yml` - For Lakeview dashboards

### Parameterize Notebooks

Notebooks receive parameters via `base_parameters` in the job definition. Access them with:

```python
dbutils.widgets.get("parameter_name")
```

## Troubleshooting

### Bundle Validation Fails

```bash
# Get detailed error information
databricks bundle validate -t dev --debug
```

### Job Fails to Run

1. Check job logs in the Databricks UI
2. Verify schema exists: `spark.sql("SHOW SCHEMAS LIKE '*analytics*'")`
3. Check cluster configuration matches available sizes

### Resources Not Deployed

```bash
# Force redeployment
databricks bundle deploy -t dev --force
```

## Best Practices

1. ✓ **Always validate before deploying**: Run `bundle validate` first
2. ✓ **Test in DEV first**: Never deploy directly to PROD
3. ✓ **Use version control**: Commit `databricks.yml` to Git
4. ✓ **Tag resources**: Use tags to track environment and ownership
5. ✓ **Monitor costs**: Set different cluster sizes per environment
6. ✓ **Automate promotion**: Use CI/CD to promote DEV → TEST → PROD

## Next Steps

1. **Add CI/CD**: Integrate with GitHub Actions or Azure DevOps
2. **Add More Resources**: Include pipelines, dashboards, models
3. **Add Tests**: Include data quality checks and unit tests
4. **Add Monitoring**: Set up alerts and logging
5. **Document Runbooks**: Create operational procedures

## Resources

* [Databricks Asset Bundles Documentation](https://docs.databricks.com/dev-tools/bundles/index.html)
* [Bundle YAML Reference](https://docs.databricks.com/dev-tools/bundles/reference.html)
* [Databricks CLI](https://docs.databricks.com/dev-tools/cli/index.html)

---

**Created**: 2026-06-08
**Environment**: Databricks Free Edition
**Bundle Version**: 1.0

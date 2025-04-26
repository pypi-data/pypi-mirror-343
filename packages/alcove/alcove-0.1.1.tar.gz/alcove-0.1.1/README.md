# alcove

[![CI](https://github.com/larsyencken/alcove/actions/workflows/ci.yml/badge.svg)](https://github.com/larsyencken/alcove/actions/workflows/ci.yml)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)

_A personal ETL and data lake._

Status: in alpha, changing often

## Overview

Alcove is an opinionated small-scale ETL framework for managing data files and directories in a content-addressable way.

## Core principles

- **A reusable framework.** Alcove provides a structured way of managing data files, scripts and their interdependencies that can be used across multiple projects.
- **First class metadata.** Every data file has an accompanying metadata sidecar that can be used to store provenance, licensing and other information.
- **Content addressed.** An `alcove` DAG is a Merkle tree of checksums that includes data, metadata and scripts, used to lazily rebuild only what is out of date.
- **Data versioning.** Every step in the DAG has a URI that includes a version, which can be an ISO date or `latest`, to encourage a reproducible workflow that still allows for change.
- **SQL support.** Alcove is a Python framework, but allows you to write steps in SQL which will be executed by DuckDB.
- **Parquet interchange.** All derived tables are generated as Parquet, which makes reuse easier.

## Usage

### Install the package

Start by installing the alcove package, either globally, or into an existing Python project.

`pip install git+https://github.com/larsyencken/alcove`

### Initialise an alcove

Enter the folder where you want to store your data and metadata, and run:

`alcove init`

This will create a `alcove.yaml` file, which will serve as the catalogue of all the data in your alcove.

### Configure object storage

You will need to configure your S3-compatible storage credentials in a `.env` file, in the same directory as your `alcove.yaml` file. Define:

```
S3_ACCESS_KEY=your_application_key_id
S3_SECRET_KEY=your_application_key
S3_BUCKET_NAME=your_bucket_name
S3_ENDPOINT_URL=your_endpoint_url
```

Now your alcove is ready to use.

### Adding a file or folder

From within your alcove folder, run `alcove snapshot path/to/your/file_or_folder dataset_name` to add a file to your alcove. See the earlier overview for choosing a dataset name.

```
alcove snapshot ~/Downloads/countries.csv countries/latest
```

This will upload the file to your S3-compatible storage, and create a metadata file at `data/<dataset_name>.meta.yaml` directory for you to complete.

The metadata format has some minimum fields, but is meant for you to extend as needed for your own purposes. Best practice would be to retain the provenance and licence information of any data you add to your alcove, especially if it originates from a third party.

### Creating a new table

To create a new table, use the `alcove new-table <table-path> [dep1 [dep2 [...]]` command. This command will create a placeholder executable script that generates an example data file of the given type based on the file extension (.parquet or .sql).

For example, to create a new table with a Parquet placeholder script:

```
alcove new-table path/to/your/table
```

This will create a placeholder script that generates an example Parquet file with the following content:

```
#!/usr/bin/env python3
import sys
import polars as pl

data = {
    "a": [1, 1, 3],
    "b": [2, 3, 5],
    "c": [3, 4, 6]
}

df = pl.DataFrame(data)

output_file = sys.argv[-1]
df.write_parquet(output_file)
```

For example, to create a new table with a SQL placeholder script:

```
alcove new-table path/to/your/table.sql
```

This will create a placeholder script that generates an example SQL file with the following content:

```
-- SQL script to create a table
CREATE TABLE example_table AS
SELECT
    1 AS a,
    2 AS b,
    3 AS c
```

The command also supports the `--edit` option to open the metadata file for the table in your editor:

```
alcove new-table path/to/your/table --edit
```

### Executing SQL step definitions

If a `.sql` step definition is detected, it will be executed using DuckDB with an in-memory database. The SQL file can use `{variable}` to interpolate template variables. The following template variables are available:

- `{output_file}`: The path to the output file.
- `{dependency}`: The path of each dependency, simplified to a semantic name.

### Building your alcove

Run `alcove run` to fetch any data that's out of date, and build any derived tables.

## Development

### Testing with MinIO

For testing with S3-compatible storage, this project uses automatically managed containers:

```bash
# Regular testing - continues even if MinIO isn't available
make test

# Strict testing - fails if MinIO container isn't available
make test-strict
```

The test environment provides two modes:
1. **Default mode**: Attempts to use MinIO container but won't fail if unavailable
2. **Strict mode**: Requires MinIO container, fails if Docker isn't running

### Docker Context Support

The testing framework automatically detects your current Docker context and uses it for container operations. This ensures tests work properly with:
- Docker Desktop
- Colima
- OrbStack
- Remote Docker contexts

### MinIO Configuration

With Docker, these credentials are automatically used:
- Access Key: minioadmin
- Secret Key: minioadmin
- Bucket: test-bucket
- Endpoint: http://localhost:9000

Containers are automatically managed and kept running between test runs for performance.
MinIO's health is verified before tests run to ensure proper S3 compatibility.

## Bugs

Please report any issues at: https://github.com/larsyencken/alcove/issues

## Changelog

- `0.1.1` (2025-04-25)
  - Renamed project from "shelf" to "alcove"
  - Added automated Docker container management for testing with MinIO
  - Added two testing modes: standard and strict (requires Docker)
  - Enhanced Docker context support for different environments (Docker Desktop, Colima, OrbStack)
  - Improved S3-compatible storage testing reliability
  - Fixed test fixtures to use consistent credentials

- `0.1.0` (Initial release)
  - Initialise a repo with `alcove.yaml`
  - `alcove snapshot` and `alcove run` with file and directory support
  - Only fetch things that are out of date
  - `alcove list` to see what datasets are available
  - `alcove audit` to ensure your alcove is coherent and correct
  - `alcove db` to enter an interactive DuckDB shell with all your data

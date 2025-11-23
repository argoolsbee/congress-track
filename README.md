# Congress Track

ETL and web app for exploring information about U.S. Congress members, their district offices, and legislative terms.

- [Overview](#overview)
- [Architecture](#architecture)
  - [Data Sources](#data-sources)
  - [Stack](#stack)
- [Setup](#setup)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Data Pipeline](#data-pipeline)
  - [Extract (dlt)](#extract-dlt)
  - [Transform (dbt)](#transform-dbt)
  - [Load](#load)
- [Frontend](#frontend)
  - [Pages](#pages)
  - [Design Patterns](#design-patterns)
- [Development](#development)
  - [Code Quality](#code-quality)

## Overview

Congress Track provides an interactive interface to search, analyze, and visualize data about current and historical U.S. legislators.

## Architecture

### Data Sources

- **Congress Legislators Data**: [unitedstates/congress-legislators](https://github.com/unitedstates/congress-legislators)
- **Geocoding**: OpenStreetMap via Nominatim

### Stack

- **Data Extraction**: [dlt](https://dlthub.com/)
- **Database**: [DuckDB](https://duckdb.org/)
- **Data Transformation**: [dbt](https://www.getdbt.com/)
- **Frontend**: [Streamlit](https://streamlit.io/)

## Setup

### Prerequisites

- [uv](https://docs.astral.sh/uv/)

### Installation

1. Create a virtual environment and install dependencies:

```bash
uv sync
```

1. Run the data pipeline:

```bash
cd extract
uv run python congress_legislators_pipeline.py
```

1. Build dbt models and create analytics tables:

```bash
cd ../transform
uv run dbt build
```

1. Launch the Streamlit app:

```bash
cd ..
uv run streamlit run app/main.py
```

The app will be available at `http://localhost:8501`

## Data Pipeline

### Extract (dlt)

The `congress_legislators_pipeline.py` fetches data from the [Congress Legislators GitHub repository](https://github.com/unitedstates/congress-legislators):

- `legislators-current.json` - Current Congress members
- `legislators-historical.json` - Historical Congress members
- `legislators-district-offices.json` - District office locations
- `legislators-social-media.json` - Social media accounts

**Features:**

- Uses dlt rest_api source as a glorified json parser
- Writes to DuckDB destination
- Geocode missing district office coordinates

### Transform (dbt)

The dbt project transforms raw data into analytical models:

- **Staging**: Cleans and standardizes raw data
- **Intermediate**: Aggregates and enriches staging data
- **Mart**: Final analytics-ready tables

### Load

Processed data is exported to Parquet files for efficient access: `load/<model_name>.parquet`

## Frontend

Built with Streamlit, the app provides an interactive interface to explore and analyze the extracted and transformed data.

### Pages

- **Legislator Lookup**: Search Congress members by state and name, view personal details and district offices
- **District Map**: Interactive map showing all district offices across the US with geocoded locations
- **Term Length Analysis**: Filter and analyze House and Senate members by years of service

### Design Patterns

1. **Component Reuse** - Shared object rendering eliminating duplication
2. **Caching** - `@st.cache_data` to optimize performance for expensive operations

## Development

### Code Quality

**Python** = ruff:

```bash
uv run ruff format
uv run ruff check
```

**SQL** = sqlfluff:

```bash
uv run sqlfluff fix
uv run sqlfluff lint
```

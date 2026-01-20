# Agentic Review Intelligence System

This project is a review intelligence system that uses autonomous agents to collect and analyze customer and employee reviews from various online platforms. It provides a real-time dashboard to visualize key performance indicators (KPIs) related to sentiment, satisfaction, and other metrics.

## Overview

The system automates the process of gathering reviews from sources like Reddit, X (formerly Twitter), the Google Play Store, and Glassdoor. It then normalizes the collected data, enriches it with sentiment analysis and other calculated scores, and aggregates the results into structured reports. A Gradio-based dashboard provides a live view of the consolidated KPIs, offering insights into customer and employee sentiment.

## Features

- **Autonomous Data Collection**: Deploys agents to autonomously gather reviews from multiple platforms.
- **Sentiment Analysis**: Utilizes VaderSentiment to compute sentiment scores for each review.
- **KPI Calculation**: Generates CSAT and NPS-like scores from the review data.
- **Structured Data**: Employs Pydantic models to ensure data is structured and validated.
- **Real-time Dashboard**: Presents live KPIs and agent events through a Gradio web interface.
- **Consolidated Insights**: Offers a single view of customer and employee health, useful for competitive analysis and brand monitoring.

## How It Works

The system is composed of several key components:

1.  **Agents**: Specialized agents are defined for each platform (e.g., `X_agent`, `Reddit_agent`). These agents are responsible for navigating the target platform and extracting review data.
2.  **Droidrun Integration**: The agents leverage Droidrun to orchestrate interactions with mobile applications for data collection.
3.  **Data Processing**: Once reviews are collected, they are processed to compute sentiment, CSAT, and NPS-like scores.
4.  **Data Modeling**: The processed data is structured into Pydantic models for consistency and validation.
5.  **Dashboard**: A Gradio UI streams and displays the aggregated data and KPIs in real time, providing an interactive dashboard for analysis.

## Setup and Installation

1.  **Prerequisites**:
    *   Python 3.13 or higher.
    *   `uv` package manager (or `pip`).

2.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd field-agents
    ```

3.  **Create and activate a virtual environment**:
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

4.  **Install dependencies**:
    The project uses `uv` to manage dependencies as specified in `pyproject.toml`.
    ```bash
    uv pip install -r requirements.txt 
    ```
    (Note: If a `requirements.txt` is not present, you can generate one from `pyproject.toml` or install dependencies directly.)

    Alternatively, using `pip`:
    ```bash
    pip install "asyncio>=4.0.0" "dotenv>=0.9.9" "gradio>=6.3.0" "llama-index>=0.14.12" "vadersentiment>=3.3.2"
    ```

5.  **Configuration**:
    - The `config.yaml` file may need to be configured with API keys or other settings for the different platforms.
    - Application-specific configurations can be found in the `config/app_cards/` directory.

## Usage

To run the Gradio web interface and view the dashboard, execute the following command:

```bash
python run.py
```

This will start the web server and provide a local URL to access the dashboard.

To run the agent processes directly and see the output in the console, you can execute:

```bash
python main.py
```

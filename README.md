# Instagram Follower Audit Tool

A powerful tool for analyzing and managing your Instagram followers, helping you identify engaged followers and potential fake accounts.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Core Features](#core-features)
- [System Architecture](#system-architecture)
- [Configuration](#configuration)
- [Performance & Security](#performance--security)
- [Troubleshooting](#troubleshooting)
- [Development](#development)

## Features

- **Engagement Analysis**: Evaluate follower engagement based on likes, comments, shares, and saves
- **Risk Assessment**: Analyze follower profiles for potential risks and suspicious behavior
- **Action Recommendations**: Get clear recommendations (Keep/Remove/Monitor) for each follower
- **Detailed Metrics**: View comprehensive engagement and risk scores
- **Real-time Processing**: Process followers asynchronously for better performance
- **Robust Error Handling**: Graceful handling of errors with retry mechanisms
- **Comprehensive Logging**: Detailed audit logs for tracking decisions

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/instagram-follower-audit.git
cd instagram-follower-audit
```

2. Create and activate a virtual environment:
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

3. Install the package in development mode:
```bash
pip install -e .
```

## Quick Start

1. Run the application:
```bash
python run.py
```

2. Open your browser and navigate to `http://localhost:8501`

3. Upload your follower data in JSON format:
```json
[
    {
        "username": "example_user",
        "id": "123456789",
        "profile_pic_url": "https://example.com/profile.jpg",
        "bio": "User bio",
        "is_public": true,
        "following": 500,
        "following_count": 1000
    }
]
```

4. Click "Start Audit" to begin the analysis

## Core Features

### Evaluation Criteria

The tool evaluates followers based on:

#### Engagement Score (0-1)
- Likes (weighted)
- Comments (weighted)
- Shares (weighted)
- Saves (weighted)
- Last interaction date
- Interaction count

#### Risk Score (0-1)
- Profile authenticity
- Following patterns
- Account age
- Activity patterns
- Suspicious behavior indicators

#### Actions
- **KEEP**: High engagement (≥0.7) and low risk (≤0.3)
- **MONITOR**: Moderate engagement (≥0.5) and moderate risk (≤0.5)
- **REMOVE**: Low engagement (≤0.3) or high risk (≥0.7)

### Custom Scoring

You can customize the scoring weights in `app/core/engagement.py`:

```python
ENGAGEMENT_WEIGHTS = {
    'likes': 0.4,
    'comments': 0.3,
    'shares': 0.2,
    'saves': 0.1
}
```

## System Architecture

### Core Components

1. **Profile Analyzer** (`app/core/profile.py`)
   - Analyzes follower profiles
   - Evaluates account authenticity
   - Calculates risk scores
   - Uses machine learning for pattern detection

2. **Engagement Checker** (`app/core/engagement.py`)
   - Processes engagement metrics
   - Calculates engagement scores
   - Handles rate limiting
   - Implements retry mechanisms

3. **Workflow Controller** (`app/core/workflow.py`)
   - Orchestrates the audit process
   - Manages async operations
   - Handles error recovery
   - Generates recommendations

4. **Audit Logger** (`app/core/logger.py`)
   - Records audit activities
   - Tracks decision points
   - Maintains audit trail
   - Handles log rotation

### Data Flow

1. **Input Processing**
   ```
   JSON Data → Data Validation → Profile Analysis
   ```

2. **Analysis Pipeline**
   ```
   Profile Analysis → Engagement Check → Risk Assessment → Action Determination
   ```

3. **Output Generation**
   ```
   Results → Logging → Dashboard Update → Export Options
   ```

## Configuration

### Environment Variables

```bash
# API Configuration
INSTAGRAM_API_KEY=your_api_key
MAX_RETRIES=3

# Logging
LOG_LEVEL=INFO

# Performance
BATCH_SIZE=100
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_PERIOD=3600
```

### Logging Structure

```
logs/
├── audit.log      # Main audit logs
├── error.log      # Error logs
└── debug.log      # Debug information
```

## Performance & Security

### Async Processing

The system uses Python's asyncio for efficient processing:

```python
async def process_followers(followers):
    tasks = [audit_follower(follower) for follower in followers]
    return await asyncio.gather(*tasks)
```

### Security Features

1. **Data Protection**
   - JSON schema validation
   - Data sanitization
   - Type checking
   - PII handling
   - Data encryption

2. **Access Control**
   - API key management
   - Rate limiting
   - IP restrictions
   - Secure storage

## Troubleshooting

### Common Issues

1. **API Rate Limiting**
   ```bash
   # Solution: Adjust rate limits in config
   RATE_LIMIT_REQUESTS=100
   RATE_LIMIT_PERIOD=3600
   ```

2. **Memory Issues**
   ```bash
   # Solution: Adjust batch size
   BATCH_SIZE=100
   ```

3. **Performance Issues**
   ```bash
   # Solution: Enable caching
   ENABLE_CACHING=true
   CACHE_TTL=3600
   ```

### Debug Mode

Enable debug mode for detailed logging:

```bash
# Set environment variable
LOG_LEVEL=DEBUG

# Or modify logger configuration
logging.basicConfig(level=logging.DEBUG)
```

## Development

### Project Structure

```
instagram-follower-audit/
├── app/
│   ├── core/
│   │   ├── engagement.py    # Engagement analysis
│   │   ├── profile.py      # Profile analysis
│   │   ├── workflow.py     # Main workflow control
│   │   └── logger.py       # Logging functionality
│   ├── ui/
│   │   ├── dashboard.py    # Main dashboard
│   │   └── components.py   # UI components
│   └── utils/
│       └── helpers.py      # Utility functions
├── data/
│   ├── mock_engagement.json
│   └── mock_profiles.json
├── logs/                   # Audit logs
├── tests/                  # Test data
├── pyproject.toml
├── setup.py
└── run.py
```

### Development Setup

1. **Local Environment**
   ```bash
   # Create virtual environment
   python -m venv env
   source env/bin/activate
   
   # Install dependencies
   pip install -e ".[dev]"
   
   # Run tests
   pytest
   ```

2. **Code Standards**
   - Follow PEP 8
   - Use type hints
   - Write docstrings
   - Include comments
   - Run pre-commit hooks

### API Reference

#### Core Functions

1. **Profile Analysis**
   ```python
   async def analyze_profile(profile_data: Dict) -> ProfileAnalysis:
       """
       Analyzes a follower's profile.
       
       Args:
           profile_data: Dictionary containing profile information
           
       Returns:
           ProfileAnalysis object with analysis results
       """
   ```

2. **Engagement Check**
   ```python
   async def check_engagement(username: str) -> EngagementResult:
       """
       Checks follower engagement metrics.
       
       Args:
           username: Instagram username
           
       Returns:
           EngagementResult with engagement scores
       """
   ```

3. **Audit Follower**
   ```python
   async def audit_follower(follower_data: Dict) -> AuditResult:
       """
       Performs complete follower audit.
       
       Args:
           follower_data: Dictionary containing follower information
           
       Returns:
           AuditResult with complete analysis
       """
   ``` 
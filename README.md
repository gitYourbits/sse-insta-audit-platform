# Instagram Follower Audit Tool

A powerful tool for analyzing and managing your Instagram followers, helping you identify engaged followers and potential fake accounts.

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

## Usage

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

## Evaluation Criteria

The tool evaluates followers based on:

### Engagement Score (0-1)
- Likes (weighted)
- Comments (weighted)
- Shares (weighted)
- Saves (weighted)
- Last interaction date
- Interaction count

### Risk Score (0-1)
- Profile authenticity
- Following patterns
- Account age
- Activity patterns
- Suspicious behavior indicators

### Actions
- **KEEP**: High engagement (≥0.7) and low risk (≤0.3)
- **MONITOR**: Moderate engagement (≥0.5) and moderate risk (≤0.5)
- **REMOVE**: Low engagement (≤0.3) or high risk (≥0.7)

## Project Structure

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

## Development

### Running Tests
```bash
pytest tests/
```

### Adding New Features
1. Create a new branch
2. Implement your changes
3. Add tests
4. Submit a pull request

### Code Style
- Follow PEP 8 guidelines
- Use type hints
- Document all functions and classes
- Write meaningful commit messages

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Streamlit for the web interface
- Python's asyncio for async operations
- The Instagram community for feedback and suggestions

## Advanced Usage

### Configuration

The tool can be configured through environment variables or a config file:

```bash
# Environment Variables
INSTAGRAM_API_KEY=your_api_key
LOG_LEVEL=INFO
MAX_RETRIES=3
```

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

### Logging Configuration

The system uses a hierarchical logging structure:

```
logs/
├── audit.log      # Main audit logs
├── error.log      # Error logs
└── debug.log      # Debug information
```

Log levels can be configured in `app/core/logger.py`.

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

### Error Handling

The system implements a robust error handling strategy:

1. **Retry Mechanism**
   - Configurable retry attempts
   - Exponential backoff
   - Error categorization

2. **Fallback Options**
   - Default values for missing data
   - Graceful degradation
   - Error recovery procedures

3. **Error Logging**
   - Detailed error tracking
   - Stack trace preservation
   - Error categorization

## Performance Optimization

### Async Processing

The system uses Python's asyncio for efficient processing:

```python
async def process_followers(followers):
    tasks = [audit_follower(follower) for follower in followers]
    return await asyncio.gather(*tasks)
```

### Caching

Implements caching for frequently accessed data:
- Profile data caching
- Engagement metrics caching
- Result caching

### Rate Limiting

Implements rate limiting to prevent API throttling:
- Configurable rate limits
- Queue management
- Priority processing

## Security Considerations

### Data Protection

1. **Input Validation**
   - JSON schema validation
   - Data sanitization
   - Type checking

2. **Access Control**
   - API key management
   - Rate limiting
   - IP restrictions

3. **Data Privacy**
   - PII handling
   - Data encryption
   - Secure storage

### Best Practices

1. **API Security**
   - Use environment variables
   - Implement API key rotation
   - Monitor API usage

2. **Data Handling**
   - Regular data cleanup
   - Secure data transmission
   - Proper error handling

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

## API Reference

### Core Functions

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

## Contributing Guidelines

### Code Standards

1. **Style Guide**
   - Follow PEP 8
   - Use type hints
   - Write docstrings
   - Include comments

2. **Testing Requirements**
   - Unit tests
   - Integration tests
   - Performance tests
   - Documentation tests

3. **Pull Request Process**
   - Create feature branch
   - Write tests
   - Update documentation
   - Submit PR

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

2. **Pre-commit Hooks**
   ```bash
   # Install pre-commit hooks
   pre-commit install
   
   # Run checks
   pre-commit run --all-files
   ```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Streamlit for the web interface
- Python's asyncio for async operations
- The Instagram community for feedback and suggestions
- Contributors and maintainers 
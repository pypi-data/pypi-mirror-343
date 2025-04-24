# TikTok Collector

A Python library for collecting TikTok data including hashtags and keywords.

## Installation

```bash
pip install tiktok-collector
```

## Features

- Collect TikTok posts by hashtag
- Collect TikTok posts by keyword
- Export data to various formats (CSV, Excel)
- Configurable collection parameters

## Usage

### Collecting by Hashtag

```python
from tiktok_collector import TiktokHashtagCollector

collector = TiktokHashtagCollector()
posts = collector.collect_by_hashtag("#python", limit=100)
```

### Collecting by Keyword

```python
from tiktok_collector import TiktokKeywordCollector

collector = TiktokKeywordCollector()
posts = collector.collect_by_keyword("python programming", limit=100)
```

## Configuration

The library can be configured using environment variables:

- `TIKTOK_API_KEY`: Your TikTok API key
- `TIKTOK_API_SECRET`: Your TikTok API secret

## Requirements

- Python 3.7+
- requests>=2.25.1
- pandas>=1.2.0
- numpy>=1.19.0
- python-dotenv>=0.19.0
- boto3>=1.26.0
- pytz>=2021.1
- httplib2>=0.20.0
- sqlalchemy>=1.4.0
- openpyxl>=3.1.0

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
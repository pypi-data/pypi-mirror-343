# TikTok Hashtag Collector

A Python package to collect TikTok posts by hashtag using the RapidAPI TikTok API.

## Installation

```bash
pip install tiktok-hashtag-collector
```

## Usage

```python
from tiktok_hashtag_collector import TiktokHashtagCollector

# Initialize the collector with your RapidAPI key
collector = TiktokHashtagCollector(
    api_key="YOUR_RAPIDAPI_KEY",  # Required: Your RapidAPI key
    country_code="US",            # Optional: Default is "US"
    max_post_by_hashtag=100,      # Optional: Default is 100
    max_hashtag_post_retry=3,     # Optional: Default is 3
    max_profile_retry=3           # Optional: Default is 3
)

# Collect posts for a hashtag
df = collector.collect_posts_by_hashtag("python")

# The DataFrame will contain the following columns:
# - search_method
# - input_kw_hst
# - post_id
# - post_link
# - caption
# - hashtag
# - hashtags
# - created_date
# - num_view
# - num_like
# - num_comment
# - num_share
# - target_country
# - user_id
# - username
# - bio
# - full_name
# - display_url
# - taken_at_timestamp
```

## Requirements

- Python 3.6+
- requests
- pandas
- boto3

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
#!/usr/bin/env python3
"""
Yandex Search API Usage Example

This script demonstrates how to use the Yandex Search API client with:
1. Direct IAM token authentication
2. OAuth token authentication (automatic conversion to IAM token)

Environment variables needed:
- YANDEX_FOLDER_ID: Your Yandex Cloud folder ID
- YANDEX_IAM_TOKEN: Your IAM token (for direct auth)
- YANDEX_OAUTH_TOKEN: Your OAuth token (for OAuth flow)
"""

import logging

from src.yandex_search_api import YandexSearchAPIClient, YandexSearchAPIError
from src.yandex_search_api.client import SearchType

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main execution function"""
    # Get credentials from environment variables
    folder_id = "b1gh198vm9k97rpvsl27"
    oauth_token = "y0__xCdssJXGMHdEyCwwvnbEqbqDqcjXUoukwbk_iRiXb0x_BLC"

    logger.info("\n=== Example 2: Using OAuth token ===")
    client = YandexSearchAPIClient(
        folder_id=folder_id,
        oauth_token=oauth_token
    )
    links = client.get_links(
        query_text="УК МИР отзывы",
        search_type=SearchType.RUSSIAN,
        max_wait=300,
        interval=10,
        )
    logger.info(f"{links}")


if __name__ == '__main__':
    main()
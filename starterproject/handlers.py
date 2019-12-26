import requests
from typing import Dict, Any

from starterproject.core import TSVFileProcessor
from OneTicketLogging import elasticsearch_logger


_logger = elasticsearch_logger(__name__)


def calc_total_value_post(event: Dict[str, Any], _: Any) -> Dict:
    """Handle example post request."""
    _logger.info(event)

    if 'url' in event:
        file_url = event['url']
    else:
        return {'error_message': "Failed reading url"}

    r = requests.get(file_url)
    # Check that the download is a success.
    r.raise_for_status()
    # Get contents of the file.
    contents = r.text

    t = TSVFileProcessor(contents)

    return {
        'total_value': t.total_value
    }

import logging
import requests
import pandas as pd
from datetime import datetime, timezone

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler("pipeline.log"),
        logging.StreamHandler(),
    ],
    force=True,
)
logger = logging.getLogger(__name__)


def ingest_data(url: str, limit: int = 1000) -> tuple[pd.DataFrame, dict]:
    logger.info("Starting ingestion from %s (limit=%d)", url, limit)

    try:
        response = requests.get(url, params={"$limit": limit}, timeout=15)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.Timeout:
        logger.error("Request timed out after 15s for %s", url)
        raise
    except requests.exceptions.HTTPError as e:
        logger.error("HTTP error %s for %s: %s", e.response.status_code, url, e)
        raise
    except requests.exceptions.RequestException as e:
        logger.error("Network error while fetching %s: %s", url, e)
        raise
    except ValueError as e:
        logger.error("Invalid/corrupt JSON received from %s: %s", url, e)
        raise

    if not data:
        logger.warning("API returned 0 records from %s", url)
        raise ValueError("Empty dataset returned from API")

    df = pd.json_normalize(data)
    metadata = {
        "ingested_at": datetime.now(timezone.utc).isoformat(),
        "source_url": url,
        "row_count": len(df),
        "col_count": len(df.columns),
    }

    logger.info("Ingested %d rows and %d columns", metadata["row_count"], metadata["col_count"])
    return df, metadata
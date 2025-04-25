import sys
import time
import threading
from typing import Union, List, Dict, Optional, Literal
import requests
from datetime import datetime, timezone
import logging
import json
import uuid
import atexit
from raindrop.version import VERSION


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

write_key = None
api_url = "https://api.raindrop.ai/v1/"
max_queue_size = 10000
upload_size = 10
upload_interval = 1.0
buffer = []
flush_lock = threading.Lock()
debug_logs = False
flush_thread = None
shutdown_event = threading.Event()
max_ingest_size_bytes = 1 * 1024 * 1024  # 1 MB

def set_debug_logs(value: bool):
    global debug_logs
    debug_logs = value
    if debug_logs:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

def start_flush_thread():
    logger.debug("Opening flush thread")
    global flush_thread
    if flush_thread is None:
        flush_thread = threading.Thread(target=flush_loop)
        flush_thread.daemon = True
        flush_thread.start()

def flush_loop():
    while not shutdown_event.is_set():
        try:
            flush()
        except Exception as e:
            logger.error(f"Error in flush loop: {e}")
        time.sleep(upload_interval)

def flush() -> None:
    global buffer

    if buffer is None:
        logger.error("No buffer available")
        return

    logger.debug("Starting flush")

    with flush_lock:
        current_buffer = buffer
        buffer = []

    logger.debug(f"Flushing buffer size: {len(current_buffer)}")

    grouped_events = {}
    for event in current_buffer:
        endpoint = event["type"]
        data = event["data"]
        if endpoint not in grouped_events:
            grouped_events[endpoint] = []
        grouped_events[endpoint].append(data)

    for endpoint, events_data in grouped_events.items():
        for i in range(0, len(events_data), upload_size):
            batch = events_data[i:i+upload_size]
            logger.debug(f"Sending {len(batch)} events to {endpoint}")
            send_request(endpoint, batch)

    logger.debug("Flush complete")

def send_request(endpoint: str, data_entries: List[Dict[str, Union[str, Dict]]]) -> None:
    
    url = f"{api_url}{endpoint}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {write_key}",
    }

    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.post(url, json=data_entries, headers=headers)
            response.raise_for_status()
            logger.debug(f"Request successful: {response.status_code}")
            break
        except requests.exceptions.RequestException as e:
            logger.error(f"Error sending request (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt == max_retries - 1:
                logger.error(f"Failed to send request after {max_retries} attempts")

def save_to_buffer(event: Dict[str, Union[str, Dict]]) -> None:
    global buffer

    if len(buffer) >= max_queue_size * 0.8:
        logger.warning(f"Buffer is at {len(buffer) / max_queue_size * 100:.2f}% capacity")

    if len(buffer) >= max_queue_size:
        logger.error("Buffer is full. Discarding event.")
        return

    logger.debug(f"Adding event to buffer: {event}")

    with flush_lock:
        buffer.append(event)

    start_flush_thread()

def identify(user_id: str, traits: Dict[str, Union[str, int, bool, float]]) -> None:
    if not _check_write_key():
        return
    data = {"user_id": user_id, "traits": traits}
    save_to_buffer({"type": "users/identify", "data": data})

def track(
    user_id: str,
    event: str,
    properties: Optional[Dict[str, Union[str, int, bool, float]]] = None,
    timestamp: Optional[str] = None,
) -> None:
    if not _check_write_key():
        return

    data = {
        "event_id": str(uuid.uuid4()),
        "user_id": user_id,
        "event": event,
        "properties": properties,
        "timestamp": timestamp if timestamp else _get_timestamp(),
    }
    data.setdefault("properties", {})["$context"] = _get_context()

    save_to_buffer({"type": "events/track", "data": data})

def track_ai(
    user_id: str,
    event: str,
    model: Optional[str] = None,
    user_input: Optional[str] = None,
    output: Optional[str] = None,
    convo_id: Optional[str] = None,
    properties: Optional[Dict[str, Union[str, int, bool, float]]] = None,
    timestamp: Optional[str] = None,
) -> None:
    if not _check_write_key():
        return

    if not user_input and not output:
        raise ValueError("One of user_input or output must be provided and not empty.")

    event_id = str(uuid.uuid4())

    data = {
        "event_id": event_id,
        "user_id": user_id,
        "event": event,
        "properties": properties or {},
        "timestamp": timestamp if timestamp else _get_timestamp(),
        "ai_data": {
            "model": model,
            "input": user_input,
            "output": output,
            "convo_id": convo_id,
        },
    }
    data.setdefault("properties", {})["$context"] = _get_context()

    size = _get_size(data)
    if size > max_ingest_size_bytes:
        logger.warning(
            f"[raindrop] Events larger than {max_ingest_size_bytes / (1024 * 1024)} MB may have properties truncated - "
            f"an event of size {size / (1024 * 1024):.2f} MB was logged"
        )
        return None  # Skip adding oversized events to buffer

    save_to_buffer({"type": "events/track", "data": data})
    return event_id

def shutdown():
    logger.info("Shutting down raindrop analytics")
    shutdown_event.set()
    if flush_thread:
        flush_thread.join(timeout=10)
    flush()  # Final flush to ensure all events are sent

def _check_write_key():
    if write_key is None:
        logger.warning("write_key is not set. Please set it before using raindrop analytics.")
        return False
    return True

def _get_context():
    return {
        "library": {
            "name": "python-sdk",
            "version": VERSION,
        },
        "metadata": {
            "pyVersion": f"v{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        },
    }

def _get_timestamp():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _get_size(event: dict[str, any]) -> int:
    try:
        data = json.dumps(event)
        return len(data.encode('utf-8'))
    except (TypeError, OverflowError) as e:
        logger.error(f"Error serializing event for size calculation: {e}")
        return 0 

# Signal types
SignalType = Literal["default", "feedback", "edit"]

def track_signal(
    event_id: str,
    name: str,
    signal_type: Optional[SignalType] = "default",
    timestamp: Optional[str] = None,
    properties: Optional[Dict[str, any]] = None,
    attachment_id: Optional[str] = None,
    comment: Optional[str] = None,
    after: Optional[str] = None,
) -> None:
    """
    Track a signal event.

    Args:
        event_id: The ID of the event to attach the signal to
        name: Name of the signal (e.g. "thumbs_up", "thumbs_down")
        signal_type: Type of signal ("default", "feedback", or "edit")
        timestamp: Optional timestamp for the signal
        properties: Optional properties for the signal
        attachment_id: Optional ID of an attachment
        comment: Optional comment (only for feedback signals)
        after: Optional after content (only for edit signals)
    """
    if not _check_write_key():
        return

    # Prepare properties with optional comment and after fields
    signal_properties = properties or {}
    if comment is not None:
        signal_properties["comment"] = comment
    if after is not None:
        signal_properties["after"] = after

    data = {
        "event_id": event_id,
        "signal_name": name,
        "signal_type": signal_type,
        "timestamp": timestamp if timestamp else _get_timestamp(),
        "properties": signal_properties,
        "attachment_id": attachment_id,
    }

    size = _get_size(data)
    if size > max_ingest_size_bytes:
        logger.warning(
            f"[raindrop] Events larger than {max_ingest_size_bytes / (1024 * 1024)} MB may have properties truncated - "
            f"an event of size {size / (1024 * 1024):.2f} MB was logged"
        )
        return  # Skip adding oversized events to buffer

    save_to_buffer({"type": "signals/track", "data": data})

atexit.register(shutdown)
"""URL utility functions for portal URL manipulation.

Generated - do not edit directly.
"""

import base64
import json
from typing import Any
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse


def append_theme_to_url(base_url: str, theme: str | dict[str, Any] | None = None) -> str:
    """Append theme parameters to a portal URL.
    
    Args:
        base_url: The base portal URL (may already have query parameters)
        theme: The theme configuration (preset string or custom dict)
    
    Returns:
        The portal URL with theme parameters appended

    """
    if not theme:
        return base_url

    try:
        parsed = urlparse(base_url)
        query_params = parse_qs(parsed.query)

        if isinstance(theme, str):
            # Preset theme
            query_params['theme'] = [theme]
        elif isinstance(theme, dict):
            if theme.get('preset'):
                # Preset theme from object
                query_params['theme'] = [theme['preset']]
            elif theme.get('custom'):
                # Custom theme
                encoded_theme = base64.b64encode(json.dumps(theme['custom']).encode()).decode()
                query_params['theme'] = ['custom']
                query_params['themeObject'] = [encoded_theme]

        new_query = urlencode(query_params, doseq=True)
        new_parsed = parsed._replace(query=new_query)
        return urlunparse(new_parsed)
    except Exception:
        # If URL parsing fails, return original URL
        return base_url


def append_broker_filter_to_url(base_url: str, broker_names: list[str] | None = None) -> str:
    """Append broker filter parameters to a portal URL.
    
    Args:
        base_url: The base portal URL (may already have query parameters)
        broker_names: Array of broker names/IDs to filter by
    
    Returns:
        The portal URL with broker filter parameters appended

    """
    if not broker_names or len(broker_names) == 0:
        return base_url

    try:
        parsed = urlparse(base_url)
        query_params = parse_qs(parsed.query)
        encoded_brokers = base64.b64encode(json.dumps(broker_names).encode()).decode()
        query_params['brokers'] = [encoded_brokers]
        new_query = urlencode(query_params, doseq=True)
        new_parsed = parsed._replace(query=new_query)
        return urlunparse(new_parsed)
    except Exception:
        # If URL parsing fails, return original URL
        return base_url


def append_kind_to_url(base_url: str, kind: str | None = None) -> str:
    """Append broker/exchange type filter to a portal URL.
    
    Args:
        base_url: The base portal URL (may already have query parameters)
        kind: Filter by provider type: 'broker' or 'exchange'
    
    Returns:
        The portal URL with type parameter appended

    """
    if not kind:
        return base_url

    try:
        parsed = urlparse(base_url)
        query_params = parse_qs(parsed.query)
        query_params['type'] = [kind]
        new_query = urlencode(query_params, doseq=True)
        new_parsed = parsed._replace(query=new_query)
        return urlunparse(new_parsed)
    except Exception:
        return base_url


def append_asset_types_to_url(base_url: str, asset_types: list[str] | None = None) -> str:
    """Append asset types (capabilities) filter to a portal URL.
    
    Multiple values are AND-filtered (brokers that support all listed asset types).
    
    Args:
        base_url: The base portal URL (may already have query parameters)
        asset_types: List of capability names (e.g. ['equity', 'crypto', 'options'])
    
    Returns:
        The portal URL with capabilities parameter appended

    """
    if not asset_types or len(asset_types) == 0:
        return base_url

    try:
        parsed = urlparse(base_url)
        query_params = parse_qs(parsed.query)
        query_params['capabilities'] = [','.join(asset_types)]
        new_query = urlencode(query_params, doseq=True)
        new_parsed = parsed._replace(query=new_query)
        return urlunparse(new_parsed)
    except Exception:
        return base_url


def append_stage_to_url(
    base_url: str,
    stages: list[str] | None = None,
) -> str:
    """Append stage filter to a portal URL.

    Portal shows only brokers in any of the given stages (OR). Omit or empty = show all.
    Valid stages: 'production', 'beta', 'alpha'.

    Args:
        base_url: The base portal URL (may already have query parameters)
        stages: One or more of 'production' | 'beta' | 'alpha'

    Returns:
        The portal URL with stage parameter appended

    """
    if not stages or len(stages) == 0:
        return base_url

    try:
        parsed = urlparse(base_url)
        query_params = parse_qs(parsed.query)
        query_params['stage'] = [','.join(stages)]
        new_query = urlencode(query_params, doseq=True)
        new_parsed = parsed._replace(query=new_query)
        return urlunparse(new_parsed)
    except Exception:
        return base_url

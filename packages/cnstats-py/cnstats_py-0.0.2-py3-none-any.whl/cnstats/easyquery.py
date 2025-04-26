import json
import logging
import random
import time
from http import HTTPStatus
from typing import Any, List, Optional

import pandas as pd
import requests

from . import cache
from .dbcode import DBCode
from .quicktypes import IndicatorNode, ReturnData

logger = logging.getLogger(__name__)

_session = requests.Session()
_session.headers.update(
    {
        "Accept": "application/json, */*; q=0.01",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        "Origin": "https://data.stats.gov.cn",
        "Referer": "https://data.stats.gov.cn/easyquery.htm",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }
)

def _response_hook(response: requests.Response, *args, **kwargs):
    response.raise_for_status()
    response.encoding = response.apparent_encoding

    if response.is_redirect:
        logger.warning("Redirect detected: %s", response.url)

    time.sleep(random.uniform(0, 5))
    return response

_session.cookies.clear()
_session.hooks["response"].append(_response_hook)


def get_tree(
    dbcode: DBCode,
    id: str = "zb",
) -> List[IndicatorNode]:
    """
    Recursively fetch tree data starting from the given id.

    Args:
        dbcode: The database code.
        id: The current node ID to fetch children for (default is "zb").

    Returns:
        A list of all nodes in the subtree starting from the initial current_id.
    """

    url = "https://data.stats.gov.cn/easyquery.htm"
    cache_key = f"getTree_{dbcode.name}_{id}"
    cached_data = cache.get(cache_key)
    nodes: List[IndicatorNode] = []

    if cached_data:
        try:
            nodes = IndicatorNode.from_list(json.loads(cached_data))
            logger.debug("Using cached data for key %s", cache_key)
        except json.JSONDecodeError:
            logger.warning(
                "Failed to decode cached data for key %s. Re-fetching.", cache_key
            )
            cached_data = None  # Force re-fetch

    if not cached_data:
        payload = {
            "id": id,
            "dbcode": dbcode.name,
            "wdcode": "zb",
            "m": "getTree",
        }
        try:
            response = _session.post(
                url,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                data=payload,
            )
            nodes = IndicatorNode.from_list(response.json())
            if len(nodes) > 0:
                # Cache the response if it contains nodes
                cache.set(cache_key, response.text)
        except Exception as e:
            logger.error(
                "Unexpected error fetching tree for id %s: %s", id, e, exc_info=True
            )
            raise

    for node in nodes:
        if not node.isParent:
            continue
        node.children = get_tree(DBCode[node.dbcode], node.id)

    return nodes


def query_data(
    dbcode: DBCode,
    zbcode: str,
    sj: str,
    regcode: Optional[str] = None,
) -> pd.DataFrame:
    """
    Perform a GET request to fetch data from the specified endpoint.
    """
    url = "https://data.stats.gov.cn/easyquery.htm"
    params = {
        "m": "QueryData",
        "dbcode": dbcode.name,
        "rowcode": "sj",
        "colcode": "zb",
        "wds": json.dumps(
            [{"wdcode": "reg", "valuecode": regcode}] if regcode else [],
        ),
        "dfwds": json.dumps(
            [
                {"wdcode": "zb", "valuecode": zbcode},
                {"wdcode": "sj", "valuecode": sj},
            ]
        ),
        "k1": str(int(time.time() * 1000)),  # Current time in milliseconds
        "h": "1",
    }

    response = _session.get(url, params=params)
    data: dict[str, Any] = response.json()

    if data["returncode"] != HTTPStatus.OK:
        # Use a more specific error or log the actual return data
        error_details = data.get("returndata", "No details provided")
        logger.error("API returned an error: %s", error_details)
        raise ValueError(f"API returned an error: {error_details}")

    returndata = ReturnData.from_dict(data["returndata"])

    return _root_to_dataframe(returndata)


# Optimized conversion of Root to pd.DataFrame
def _root_to_dataframe(returndata: ReturnData) -> pd.DataFrame:
    # Extract time (sj) and indicator (zb) nodes
    sj_wd = returndata.sj_dimension()
    sj_nodes = sj_wd.nodes
    sj_map = {sj.code: sj for sj in sj_nodes}
    zb_nodes = sorted(returndata.zb_dimension().nodes, key=lambda x: x.sortcode)
    zb_map = {zb.code: zb for zb in zb_nodes}

    datarows: dict[str, dict[str, str]] = {}
    datanodes = filter(lambda x: x.data.hasdata, returndata.datanodes)
    for datanode in datanodes:
        sj_code = datanode.sj_code()
        zb_code = datanode.zb_code()
        if sj_code not in datarows:
            datarows[sj_code] = {sj_wd.wdname: sj_map[sj_code].cname}
        datarows[sj_code][zb_map[zb_code].cname] = datanode.data.strdata

    return pd.DataFrame(
        data=list(datarows.values()),
        columns=[sj_wd.wdname] + [zb.cname for zb in zb_nodes],
    )

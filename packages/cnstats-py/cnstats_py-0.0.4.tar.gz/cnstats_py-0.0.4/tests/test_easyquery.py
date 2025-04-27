import pandas as pd
import pytest

import cnstats
from cnstats.dbcode import DBCode


@pytest.mark.parametrize(
    "dbcode_param",
    [
        DBCode.hgyd,
        DBCode.hgjd,
        DBCode.hgnd,
    ],
)
def test_get_tree(dbcode_param):
    """Test the get_tree function for various database codes."""
    nodes = cnstats.get_tree(dbcode_param)
    assert isinstance(nodes, list)
    assert len(nodes) > 0


# Basic test for query_data function
def test_query_data():
    # Example query parameters (these might need adjustment based on available data)
    # Using hgyd (monthly), indicator A01010G (Consumer Prodct Index), time 2023
    # Note: 'sj' (time) format might vary. Using a recent year range as an example.
    # This specific query might fail if the data structure changes or data for this exact period isn't available.
    df = cnstats.query_data(dbcode=DBCode.hgyd, zbcode="A01010G", sj="2023")
    assert isinstance(df, pd.DataFrame)
    # Check if the DataFrame is not empty
    assert not df.empty
    # Check for expected columns (time column + indicator column)
    # The exact column names depend on the query results (sj_wd.wdname and zb.cname)
    # We check if there are at least two columns as a basic validation
    assert len(df.columns) >= 2

import argparse
import logging
import os
import sys
from typing import List

from .dbcode import DBCode
from .easyquery import get_tree, query_data
from .quicktypes import IndicatorNode


# Helper function to format the tree nodes
def format_tree_nodes(nodes: List[IndicatorNode], indent: str = "") -> str:
    output = ""
    for node in nodes:
        output += f"{indent}{node.name} ({node.id})\n"
        if node.children:
            output += format_tree_nodes(node.children, indent + "  ")
    return output


def find_indicator(indicators: List[IndicatorNode], zbcode: str) -> IndicatorNode:
    """
    Recursively search for an indicator by zbcode in a list of IndicatorNode objects.
    """
    for indicator in indicators:
        if indicator.id == zbcode:
            return indicator
        else:
            found = find_indicator(indicator.children, zbcode)
            if found:
                return found
    return None


def add_get_tree_parser(subparsers: argparse._SubParsersAction):
    """Adds the parser for the get_tree command."""
    parser_get_tree: argparse.ArgumentParser = subparsers.add_parser(
        "get_tree",
        help="Fetch the indicator tree (metadata) for a specific database.",
        description="Fetches the hierarchical structure of indicators (metadata) for a given database code. The output is a JSON representation of the tree.",
    )
    parser_get_tree.add_argument(
        "--dbcode",
        type=str,
        required=True,
        choices=[db.name for db in DBCode],
        metavar="",
        help=f"Required. The database code (e.g., {', '.join([str(db) for db in DBCode])}).",
    )
    parser_get_tree.add_argument(
        "--id",
        type=str,
        default="zb",
        metavar="",
        help="The starting indicator ID for the tree (default: 'zb', the root).",
    )
    parser_get_tree.add_argument(
        "-o",
        "--output",
        type=str,
        metavar="",
        help="Optional. Path to save the output text file. Defaults to '.txt' if no extension is provided. If omitted, prints to stdout.",
    )


def add_query_data_parser(subparsers: argparse._SubParsersAction):
    """Adds the parser for the query_data command."""
    parser_query_data: argparse.ArgumentParser = subparsers.add_parser(
        "query_data",
        help="Query actual statistical data based on indicators and time periods.",
        description="Queries statistical data for specific indicators (zbcode) and time periods (sj) within a database. Can optionally filter by region (regcode).",
        formatter_class=argparse.RawTextHelpFormatter,  # Use RawTextHelpFormatter for better formatting
    )
    parser_query_data.add_argument(
        "--dbcode",
        type=str,
        required=True,
        choices=[db.name for db in DBCode],
        metavar="",
        help=f"Required. The database code (e.g., {', '.join([str(db) for db in DBCode])}).",
    )
    parser_query_data.add_argument(
        "--zbcode",
        type=str,
        required=True,
        metavar="",
        help="Required. The indicator code(s).",
    )
    parser_query_data.add_argument(
        "--sj",
        type=str,
        required=True,
        metavar="",
        help="Required. The time period code(s) (e.g., '2023', '2021-', '-2024', '202401').",
    )
    parser_query_data.add_argument(
        "--regcode",
        type=str,
        metavar="",
        help="Optional. The region code(s).",
    )
    parser_query_data.add_argument(
        "-o",
        "--output",
        type=str,
        metavar="",
        help="""
Optional. Path to save the output data file.
Format is determined by the file extension:
  .csv   - Comma Separated Values (default if no extension)
  .xlsx  - Excel spreadsheet (requires 'openpyxl')
  .dta   - Stata data file
If omitted, use the indicator name or zbcode as the filename.
""",
    )


def run_get_tree(args):
    """Executes the get_tree command."""
    nodes = get_tree(
        dbcode=DBCode[args.dbcode],
        id=args.id,
    )
    # Format the nodes into the desired text tree structure
    output_text = format_tree_nodes(nodes)

    if args.output:
        # Ensure the output file has a .txt extension if none is provided
        output_path = args.output
        if not os.path.splitext(output_path)[1]:
            output_path += ".txt"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(output_text)
        logging.info(f"Indicator tree saved to {output_path}")
    else:
        print(output_text)


def run_query_data(args):
    """Executes the query_data command."""
    output_path = args.output
    if output_path:
        _, file_extension = os.path.splitext(output_path)
        file_extension = file_extension.lower()

        # default to CSV if no extension is provided
        if not file_extension:
            logging.info("No file extension provided. Defaulting to .csv")
            output_path += ".csv"
            file_extension = ".csv"

        if file_extension not in [".csv", ".xls", ".xlsx", ".dta"]:
            logging.error(
                f"Unsupported file extension '{file_extension}'. Supported formats are: .csv, .xls, .xlsx, .dta"
            )
            sys.exit(1)

    df = query_data(
        dbcode=DBCode[args.dbcode],
        zbcode=args.zbcode,
        sj=args.sj,
        regcode=args.regcode,
    )

    if df.empty:
        logging.warning(
            f"No data found for the given parameters: dbcode={args.dbcode}, zbcode={args.zbcode}, sj={args.sj}, regcode={args.regcode}"
        )
        sys.exit(1)

    if output_path is None:
        try:
            # Attempt to fetch the indicator name for a more descriptive default filename
            indicators = get_tree(
                dbcode=DBCode[args.dbcode],
                id=args.zbcode[:-2] if len(args.zbcode) > 3 else "zb",
            )
            indicator = find_indicator(indicators, args.zbcode)
            if indicator and not indicator.isParent:
                # Sanitize indicator name for use as filename
                safe_name = "".join(
                    c for c in indicator.name if c.isalnum() or c in (" ", "_")
                ).rstrip()
                output_path = f"{safe_name}.csv"
            else:
                output_path = f"{args.zbcode}.csv"
        except Exception as e:
            # Fallback if fetching tree fails or indicator not found
            logging.warning(
                f"Could not determine indicator name, using zbcode as filename. Error: {e}"
            )
            output_path = f"{args.zbcode}.csv"

    if not output_path:  # Should not happen with the logic above, but keep as safeguard
        print(df.to_string(index=False))
        sys.exit(0)

    file_extension = os.path.splitext(output_path)[1].lower()

    try:
        if file_extension in [".xls", ".xlsx"]:
            df.to_excel(output_path, index=False)
            logging.info(f"Data saved to {output_path} as Excel")
        elif file_extension == ".dta":
            df.to_stata(output_path, write_index=False)
            logging.info(f"Data saved to {output_path} as Stata")
        else:  # Default to CSV
            df.to_csv(
                output_path, index=False, encoding="utf-8-sig"
            )  # Use utf-8-sig for better Excel compatibility
            logging.info(f"Data saved to {output_path} as CSV")
    except ImportError as ie:
        if "openpyxl" in str(ie) and file_extension in [".xls", ".xlsx"]:
            logging.error(
                "Error saving to Excel: 'openpyxl' library not found. "
                "Please install it: pip install openpyxl"
            )
        elif "stata" in str(ie) and file_extension == ".dta":
            logging.error(
                "Error saving to Stata: Potential issue with Stata writer or dependencies. "
                "Ensure pandas is up-to-date."
            )
        else:
            logging.error(f"Error saving file: {ie}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"An error occurred while saving the file: {e}", exc_info=True)
        sys.exit(1)


def main():
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    parser = argparse.ArgumentParser(
        prog="cnstats",
        description="A command-line interface for fetching data from the China National Bureau of Statistics.",
        formatter_class=argparse.RawTextHelpFormatter,  # Use RawTextHelpFormatter for better formatting
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # Add subparsers using the dedicated functions
    add_get_tree_parser(subparsers)
    add_query_data_parser(subparsers)

    args = parser.parse_args()

    # Execute the appropriate function based on the command
    if args.command == "get_tree":
        run_get_tree(args)
    elif args.command == "query_data":
        run_query_data(args)
    else:
        # If no command was provided, print help
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()  # Indent this line

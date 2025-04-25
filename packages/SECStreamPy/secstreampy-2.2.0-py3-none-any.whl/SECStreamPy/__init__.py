"""
This module initializes the package and makes it possible to use the package's functionality
by exposing key components, classes, and functions. It ensures that the package is properly set up
when imported.
"""
from SECStreamPy.metadata.__version__ import __version__
from SECStreamPy.src._constants import (
    SEC_BASE_URL, SEC_DATA_URL, IntString, YYYY_MM_DD, DATE_PATTERN, DATE_RANGE_PATTERN,
    text_extensions, binary_extensions, barchart, ticket, page_facing_up, classical_building, unicode_for_form
)
from SECStreamPy.src._errors import (
    DataDockError, APIConnectionError, IdentityError, TypeValueError, InvalidRequestMethodError, DataDockServerError
)
from SECStreamPy.src.config import check_sec_identity
from SECStreamPy.src.data_class import FilingsState, FilingInfo, FilingTxtDoc, FilingDocInfo
from SECStreamPy.src.logger import CustomLogger
from SECStreamPy.src.utils import parse_html_content

from SECStreamPy.core._rich_ import (
    add_columns_and_rows, repr_rich, colorize_words,
    format_value, financial_rich_table, display_r_files, df_to_rich_table
)
from SECStreamPy.core._table_ import (
    format_form_info, format_table_info, format_filer_info,
    FinancialTableDisplay, SectionsTableDisplay, FilingIndexDisplay
)
from SECStreamPy.core._xml_ import parse_xml, xml_namespaces
from SECStreamPy.core.filing import (
    form_types, is_valid_form, format_rich, format_repr,
    FilingListingIndex, get_filing
)

VERSION = __version__

__all__ = [
    'VERSION', 'SEC_BASE_URL', 'SEC_DATA_URL', 'IntString', 'YYYY_MM_DD', 'DATE_PATTERN', 'DATE_RANGE_PATTERN',
    'check_sec_identity', 'text_extensions', 'binary_extensions', 'barchart', 'ticket', 'page_facing_up',
    'classical_building', 'unicode_for_form', 'DataDockError', 'APIConnectionError', 'IdentityError',
    'TypeValueError', 'InvalidRequestMethodError', 'DataDockServerError', 'CustomLogger',
    'add_columns_and_rows', 'repr_rich', 'colorize_words', 'format_value', 'financial_rich_table',
    'display_r_files', 'df_to_rich_table', 'format_form_info', 'format_table_info', 'format_filer_info',
    'FinancialTableDisplay', 'SectionsTableDisplay', 'FilingIndexDisplay', 'form_types', 'is_valid_form',
    'format_rich', 'format_repr', 'FilingListingIndex', 'get_filing', "parse_xml",
    "xml_namespaces", "parse_html_content", "FilingInfo"
]

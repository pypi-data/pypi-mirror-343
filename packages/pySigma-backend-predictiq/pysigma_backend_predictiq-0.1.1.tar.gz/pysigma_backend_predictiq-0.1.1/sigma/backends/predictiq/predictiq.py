from sigma.rule import SigmaRule
from sigma.conversion.base import TextQueryBackend
from sigma.conversion.state import ConversionState, DeferredQueryExpression
from sigma.processing.pipeline import ProcessingPipeline
from sigma.conditions import ConditionItem, ConditionAND, ConditionOR, ConditionNOT, ConditionFieldEqualsValueExpression
from sigma.types import SigmaCompareExpression, SigmaRegularExpression, SigmaRegularExpressionFlag, SigmaString, SigmaNumber
from sigma.pipelines.predictiq import predictiq_pipeline
import sigma.backends as backends
import re
from typing import ClassVar, Dict, Tuple, List, Any, Optional, Union


class PredictIQBackend(TextQueryBackend):
    """predict-iq backend."""

    # Operator precedence: tuple of Condition{AND,OR,NOT} in order of precedence.
    # The backend generates grouping if required
    name : ClassVar[str] = "predict-iq backend"
    formats : ClassVar[Dict[str, str]] = {
        "default": "Simple log search query mode",
    }
    
    requires_pipeline : ClassVar[bool] = False

    # Built-in pipeline
    backend_processing_pipeline : ClassVar[ProcessingPipeline] = predictiq_pipeline()

    # iIn-expressions
    convert_or_as_in : ClassVar[bool] = True                     # Convert OR as in-expression
    convert_and_as_in : ClassVar[bool] = True                    # Convert AND as in-expression
    in_expressions_allow_wildcards : ClassVar[bool] = True       # Values in list can contain wildcards. If set to False (default) only plain values are converted into in-expressions.

    group_expression : ClassVar[str] = "({expr})"

    or_token : ClassVar[str] = "OR"
    and_token : ClassVar[str] = "AND"
    not_token : ClassVar[str] = "NOT"
    eq_token : ClassVar[str] = "="

    contains_token, starts_token, ends_token = "CONTAINS", "STARTS", "ENDS"

    str_double_quote : ClassVar[str] = '"'

    escape_char : ClassVar[str] = "\\"
    wildcard_multi : ClassVar[str] = "*"
    wildcard_single : ClassVar[str] = "*"

    re_expression : ClassVar[str] = "{field}=/{regex}/i"
    re_escape_char : ClassVar[str] = "\\"
    re_escape : ClassVar[Tuple[str]] = ('"')

    cidr_expression : ClassVar[str] = "{field} = IP({value})"

    compare_op_expression : ClassVar[str] = "{field} {operator} {value}"
    compare_operators : ClassVar[Dict[SigmaCompareExpression.CompareOperators, str]] = {
        SigmaCompareExpression.CompareOperators.LT  : "<",
        SigmaCompareExpression.CompareOperators.LTE : "<=",
        SigmaCompareExpression.CompareOperators.GT  : ">",
        SigmaCompareExpression.CompareOperators.GTE : ">=",
    }

    field_null_expression : ClassVar[str] = "{field} = null"

    field_in_list_expression : ClassVar[str] = "{field} IN [{list}]"
    contains_any_expression : ClassVar[Optional[str]] = "{field} CONTAINS-ANY [{list}]"
    contains_all_expression : ClassVar[Optional[str]] = "{field} CONTAINS-ALL [{list}]"
    startswith_any_expression : ClassVar[Optional[str]] = "{field} STARTS-WITH-ANY [{list}]"
    list_separator : ClassVar[str] = ", "

    # Basic conversion “Field = Value (string)” 
    def convert_condition_field_eq_val_str(self, cond, state):
        v = cond.value.to_plain()
        if v.startswith("*") and v.endswith("*"):
            return f'{cond.field} {self.contains_token} "{v.strip("*")}"'
        if v.endswith("*"):
            return f'{cond.field} {self.starts_token} "{v.strip("*")}"'
        if v.startswith("*"):
            return f'{cond.field} {self.ends_token} "{v.strip("*")}"'
        return f'{cond.field} {self.eq_token} "{v}"'

    # Finalization (simple where())
    def finalize_query_default(self, rule: SigmaRule, query: str, _, __):
        return f"where({query})"

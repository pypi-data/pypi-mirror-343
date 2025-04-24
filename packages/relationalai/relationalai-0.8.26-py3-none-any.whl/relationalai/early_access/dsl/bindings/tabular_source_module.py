import pandas as pd

from relationalai.early_access.dsl import DateTime, Date, Decimal
from relationalai.early_access.dsl.bindings.relations import AttributeView
from relationalai.early_access.dsl.bindings.tables import CsvTable
from relationalai.early_access.dsl.core import std
from relationalai.early_access.dsl.core.relations import rule

class TabularSourceModule:
    def generate(self, table: CsvTable, data: pd.DataFrame):
        for index, row in data.iterrows():
            for column_name in data.columns:
                value = row[column_name]
                if pd.notna(value):
                    column = table.__getattr__(column_name)
                    column_type = column.type().root_unconstrained_type()
                    relation = column.relation()
                    if column_type.name() == Date.name():
                        self._row_to_date_value_rule(relation, index, value)
                    elif column_type.name() == DateTime.name():
                        self._row_to_date_time_value_rule(relation, index, value)
                    elif column_type.name() == Decimal.name():
                        self._row_to_decimal_value_rule(relation, index, value)
                    else:
                        self._row_to_value_rule(relation, index, value)

    @staticmethod
    def _row_to_value_rule(relation: AttributeView, row, value):
        with relation:
            @rule()
            def row_to_value(r, v):
                r == row
                v == value

    @staticmethod
    def _row_to_date_value_rule(relation: AttributeView, row, value):
        with relation:
            @rule()
            def row_to_value(r, v):
                r == row
                std.parse_date(value, 'Y-m-d', v)

    @staticmethod
    def _row_to_date_time_value_rule(relation: AttributeView, row, value):
        with relation:
            @rule()
            def row_to_value(r, v):
                r == row
                std.parse_datetime(value, 'Y-m-d HH:MM:SS z', v)

    @staticmethod
    def _row_to_decimal_value_rule(relation: AttributeView, row, value):
        with relation:
            @rule()
            def row_to_value(r, v):
                r == row
                std.parse_decimal(64, 4, value, v)
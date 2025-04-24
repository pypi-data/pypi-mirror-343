import dataclasses
from abc import abstractmethod
from typing import Optional, Any

from relationalai.early_access.dsl.bindings.common import BindableAttribute, BindableTable
from relationalai.early_access.dsl.bindings.relations import AttributeView
from relationalai.early_access.dsl.core.types.standard import String, Integer, Decimal, Date, DateTime, Boolean, \
    BigInteger, Float, RowId
from relationalai.early_access.dsl.core.types.unconstrained import UnconstrainedValueType
from relationalai.early_access.dsl.core.utils import generate_stable_uuid
from relationalai.early_access.dsl.core.relations import Relation
from relationalai.early_access.dsl.core.namespaces import Namespace
from relationalai.early_access.dsl.types.entities import EntityType
from relationalai.early_access.dsl.ontologies.roles import Role
#=
# Physical metadata for a Snowflake table.
#=

@dataclasses.dataclass(frozen=True)
class ColumnRef:
    table: str
    column: str

@dataclasses.dataclass
class ForeignKey:
    name: str
    source_columns: list[ColumnRef] = dataclasses.field(default_factory=list)
    target_columns: list[ColumnRef] = dataclasses.field(default_factory=list)

    def __hash__(self):
        return hash(self.name)

@dataclasses.dataclass
class SchemaMetadata:
    name: str
    foreign_keys: list[ForeignKey] = dataclasses.field(default_factory=list)

@dataclasses.dataclass
class ColumnMetadata:
    name: str
    datatype: str
    is_nullable: bool
    numeric_precision: Optional[int] = None
    numeric_precision_radix: Optional[int] = None
    numeric_scale: Optional[int] = None

@dataclasses.dataclass
class CsvColumnMetadata:
    name: str
    datatype: 'UnconstrainedValueType'

@dataclasses.dataclass
class TabularMetadata:
    name: str
    columns: list[ColumnMetadata] = dataclasses.field(default_factory=list)
    foreign_keys: set[ForeignKey] = dataclasses.field(default_factory=set)

@dataclasses.dataclass(frozen=True)
class Binding:
    column: 'BindableColumn'

@dataclasses.dataclass(frozen=True)
class RoleBinding(Binding):
    role: 'Role'

    def __str__(self):
        return f'RoleBinding[{self.column.table.physical_name()}:{self.column.physical_name()} -> {self.role.player().name()}]'

@dataclasses.dataclass(frozen=True)
class IdentifierBinding(Binding):
    entity_type: 'EntityType'

    def __str__(self):
        return f'IdentifierBinding[{self.column.table.physical_name()}:{self.column.physical_name()} -> {self.entity_type.name()}]'

@dataclasses.dataclass(frozen=True)
class SubtypeBinding(Binding):
    sub_type: 'EntityType'

    def __str__(self):
        return f'SubtypeBinding[{self.column.table.physical_name()}:{self.column.physical_name()} -> {self.sub_type.name()}]'

@dataclasses.dataclass(frozen=True)
class FilteringSubtypeBinding(SubtypeBinding):
    has_value: Any

    def __str__(self):
        return f'FilteringSubtypeBinding[{self.column.table.physical_name()}:{self.column.physical_name()} == {self.has_value}]'

_sf_type_mapping = {
    'varchar': String,
    'char': String,
    'text': String,
    'date': Date,
    'datetime': DateTime,
    'timestamp_ntz': DateTime,
    'boolean': Boolean,
    'float': Float,
}
def _map_rai_type(col: ColumnMetadata) -> 'UnconstrainedValueType':
    datatype = col.datatype.lower()
    # TODO: do better with integer type conversion
    if datatype == 'number':
        if col.numeric_scale is not None and col.numeric_scale > 0:
            return Decimal
        elif col.numeric_precision is not None and col.numeric_precision > 9:
            return BigInteger
        else:
            return Integer
    else:
        return _sf_type_mapping[datatype]

class BindableColumn(BindableAttribute):
    _table: 'BindableTable'
    _references: Optional['ColumnRef']
    _attr_relation: 'AttributeView'

    def __init__(self, table: 'BindableTable', model):
        self._table = table
        self._model = model
        self._references = None

    def __call__(self, *args):
        if self._attr_relation is None:
            raise Exception(f'Attribute view for `{self.physical_name()}` not initialized')
        return self.relation()(*args)

    @abstractmethod
    def relation(self) -> 'AttributeView':
        pass

    def identifies(self, entity_type: 'EntityType'):
        binding = IdentifierBinding(column=self, entity_type=entity_type)
        self._model.binding(binding)

    def binds_to(self, role: 'Role'):
        binding = RoleBinding(role=role, column=self)
        self._model.binding(binding)

    def references_subtype(self, sub_type: 'EntityType'):
        binding = SubtypeBinding(column=self, sub_type=sub_type)
        self._model.binding(binding)

    def filters_subtype(self, sub_type: 'EntityType', by_value: Any):
        binding = FilteringSubtypeBinding(column=self, sub_type=sub_type, has_value=by_value)
        self._model.binding(binding)

    def binds(self, relation: 'Relation'):
        roles = relation.reading().roles
        # this binds to the last role in binary relations
        role = roles[-1]
        binding = RoleBinding(role=role, column=self)
        self._model.binding(binding)

    @property
    def table(self):
        return self._table

    @property
    def references(self):
        return self._references

    @references.setter
    def references(self, ref: 'ColumnRef'):
        self._references = ref

    @abstractmethod
    def physical_name(self) -> str:
        pass

    @abstractmethod
    def type(self) -> 'UnconstrainedValueType':
        pass

    def ref(self) -> 'ColumnRef':
        return ColumnRef(self._table.table_name, self.physical_name())

    def guid(self):
        return generate_stable_uuid(f'$attr:{self._table.physical_name()}_{self.physical_name()}')


class BindableSnowflakeColumn(BindableColumn):
    _metadata: 'ColumnMetadata'

    def __init__(self, metadata: 'ColumnMetadata', table: 'SnowflakeTable', model):
        super().__init__(table, model)
        self._metadata = metadata
        self._datatype = _map_rai_type(self._metadata)
        self._attr_relation = AttributeView(Namespace.top, self)

    def relation(self) -> 'AttributeView':
        return self._attr_relation

    @property
    def metadata(self):
        return self._metadata

    def physical_name(self) -> str:
        return self._metadata.name

    def type(self) -> 'UnconstrainedValueType':
        return _map_rai_type(self._metadata)


class BindableCsvColumn(BindableColumn):
    _metadata: 'CsvColumnMetadata'
    _column_basic_type: str

    def __init__(self, metadata: 'CsvColumnMetadata', table: 'CsvTable', model):
        super().__init__(table, model)
        self._metadata = metadata
        self._column_basic_type = "Int64" if metadata.datatype.root_unconstrained_type() == Integer else "string"
        self._attr_relation = model._add_relation(AttributeView(Namespace.top, self))

    def relation(self) -> 'AttributeView':
        return self._attr_relation

    @property
    def metadata(self):
        return self._metadata

    def physical_name(self) -> str:
        return self._metadata.name

    def type(self) -> 'UnconstrainedValueType':
        return self._metadata.datatype

    def basic_type(self):
        return self._column_basic_type


class SnowflakeTable(BindableTable):
    _columns: dict[str, BindableSnowflakeColumn]
    _foreign_keys: set[ForeignKey]

    def __init__(self, metadata: 'TabularMetadata', model):
        super().__init__(metadata.name)
        self._columns = {col.name: BindableSnowflakeColumn(col, self, model) for col in metadata.columns}
        self._foreign_keys = metadata.foreign_keys
        for fk in self._foreign_keys:
            # TODO : this doesn't work for composite FKs
            for col in fk.source_columns:
                target_col = fk.target_columns[0]
                self._columns[col.column].references = target_col

    def __getattr__(self, key):
        if key in self.__dict__:
            return self.__dict__[key]
        if key in self._columns:
            return self._columns[key]
        else:
             raise AttributeError(f'Snowflake table "{self._table_name}" has no column named "{key}"')

    def __str__(self):
        # returns the name of the table, as well as the columns and their types
        return self._table_name + ':\n' + '\n'.join(
            [f' {col.metadata.name} {col.metadata.datatype}' for _, col in self._columns.items()]
        ) + '\n' + '\n'.join(
            [f' {fk.source_columns} -> {fk.target_columns}' for fk in self._foreign_keys]
        )

    def physical_name(self):
        # physical relation name is always in the form of `{database}_{schema}_{table}
        return self._table_name.lower().replace('.', '_')

    def key_type(self) -> 'UnconstrainedValueType':
        return RowId


class CsvTable(BindableTable):
    _columns: dict[str, BindableCsvColumn]
    _basic_type_schema: dict[str, str]

    def __init__(self, name: str, schema: dict[str, 'UnconstrainedValueType'], model):
        super().__init__(name)
        self._columns = {column_name: BindableCsvColumn(CsvColumnMetadata(column_name, column_type), self, model)
                         for column_name, column_type in schema.items()}
        self._basic_type_schema = {col.metadata.name: col.basic_type() for col in self._columns.values()}

    def __getattr__(self, key):
        if key in self.__dict__:
            return self.__dict__[key]
        if key in self._columns:
            return self._columns[key]
        else:
            raise AttributeError(f'CSV table "{self._table_name}" has no column named "{key}"')

    def __str__(self):
        # returns the name of the table, as well as the columns and their types
        return self._table_name + ':\n' + '\n'.join(
            [f' {col.metadata.name} {col.metadata.datatype.root_unconstrained_type()}' for _, col in self._columns.items()]
        )

    @property
    def basic_type_schema(self):
        return self._basic_type_schema

    def physical_name(self) -> str:
        return self._table_name.lower()

    def key_type(self) -> 'UnconstrainedValueType':
        return RowId

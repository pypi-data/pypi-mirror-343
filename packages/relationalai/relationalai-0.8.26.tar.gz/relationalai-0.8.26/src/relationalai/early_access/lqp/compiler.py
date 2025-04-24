#--------------------------------------------------
# Compiler
#--------------------------------------------------

from typing import cast, Tuple, Sequence

from relationalai.early_access.metamodel import ir, compiler as c, builtins as rel_builtins
from relationalai.early_access.metamodel import types
from relationalai.early_access.lqp import ir as lqp
from relationalai.early_access.metamodel.rewrite import Splinter
from relationalai.early_access.metamodel.util import NameCache
from relationalai.early_access.metamodel.compiler import Pass

import hashlib

# TODO: take rewrite out of rel it doesnt belong there
from relationalai.early_access.rel import rewrite

from dataclasses import field

# TODO: assert theres no nested nested nested aggregates
# TODO: assert theres only one aggregate per rule
# TODO: is this correct?
# Move aggregates to the same level as updates (i.e. top-level logical)
class HoistAggregates(Pass):
    def rewrite(self, model: ir.Model, cache) -> ir.Model:
        root = cast(ir.Logical, model.root)
        new_subtasks = []
        for subtask in root.body:
            subtask = cast(ir.Logical, subtask)
            new_subsubtasks = []
            for subsubtask in subtask.body:
                if not isinstance(subsubtask, ir.Logical):
                    new_subsubtasks.append(subsubtask)
                    continue

                subsubtask = cast(ir.Logical, subsubtask)
                if self.has_aggregate(subsubtask):
                    new_subsubtask, aggr = self._hoist_aggregates(subsubtask)
                    new_subsubtasks.append(new_subsubtask)
                    new_subsubtasks.append(aggr)
                else:
                    new_subsubtasks.append(subsubtask)

            new_subtask = ir.Logical(
                    subtask.engine,
                    subtask.hoisted,
                    tuple(new_subsubtasks),
                )
            new_subtasks.append(new_subtask)

        new_root = ir.Logical(root.engine, root.hoisted, tuple(new_subtasks))
        model = ir.Model(
            model.engines,
            model.relations,
            model.types,
            new_root,
        )
        return model

    def has_aggregate(self, task: ir.Task) -> bool:
        assert isinstance(task, ir.Logical)
        for subtask in task.body:
            if isinstance(subtask, ir.Aggregate):
                return True
        return False

    def _hoist_aggregates(self, task: ir.Task) -> Tuple[ir.Task, ir.Aggregate]:
        assert isinstance(task, ir.Logical)
        aggr = None
        new_subtasks = []
        for subtask in task.body:
            if isinstance(subtask, ir.Aggregate):
                assert aggr is None, "only one aggregate supported at the moment"
                aggr = subtask
            else:
                new_subtasks.append(subtask)
        assert aggr is not None, "should have found an aggregate"
        return (ir.Logical(
            task.engine,
            task.hoisted,
            tuple(new_subtasks),
        ), aggr)

# Rewrites aggregates when necessary e.g. avg -> sum/count
class NormalizeAggregates(Pass):
    def rewrite(self, model: ir.Model, cache) -> ir.Model:
        self.var_name_cache: NameCache = NameCache()
        root = cast(ir.Logical, model.root)
        new_subtasks = []
        for subtask in root.body:
            subtask = cast(ir.Logical, subtask)
            if self.has_aggregate(subtask):
                new_subtask = self._rewrite_subtask(subtask)
                new_subtasks.append(new_subtask)
            else:
                new_subtasks.append(subtask)
        new_root = ir.Logical(root.engine, root.hoisted, tuple(new_subtasks))
        model = ir.Model(
            model.engines,
            model.relations,
            model.types,
            new_root,
        )
        return model

    def _rewrite_subtask(self, task: ir.Task) -> ir.Task:
        assert isinstance(task, ir.Logical)
        new_subtasks = []
        for subtask in task.body:
            if isinstance(subtask, ir.Aggregate):
                assert isinstance(subtask, ir.Aggregate)
                if subtask.aggregation.name == "sum":
                    new_subtasks.append(subtask)
                elif subtask.aggregation.name == "count":
                    new_subtasks.append(subtask)
                elif subtask.aggregation.name == "avg":
                    tasks = self._make_avg(subtask)
                    for tt in tasks:
                        new_subtasks.append(tt)
                else:
                    raise NotImplementedError(f"Unsupported aggregate: {subtask.aggregation.name}")
            else:
                new_subtasks.append(subtask)

        return ir.Logical(
            task.engine,
            task.hoisted,
            tuple(new_subtasks),
        )

    def _make_avg(self, task: ir.Aggregate) -> list[ir.Task]:
        assert isinstance(task, ir.Aggregate)
        assert task.aggregation.name == "avg"

        # TODO: confirm input args
        assert len(task.args) == 2
        input_arg = task.args[0]
        output_arg = task.args[1]
        assert isinstance(input_arg, ir.Var)
        assert isinstance(output_arg, ir.Var)

        new_sum_name = self.var_name_cache.get_name(input_arg.id, "sum")
        new_count_name = self.var_name_cache.get_name(input_arg.id, "count")
        new_sum = ir.Var(output_arg.type, new_sum_name)
        new_count = ir.Var(output_arg.type, new_count_name)

        sum_args = tuple([input_arg, new_sum])
        count_args = tuple([input_arg, new_count])

        sum_task = ir.Aggregate(
            task.engine,
            rel_builtins.sum,
            task.projection,
            task.group,
            sum_args,
        )
        count_task = ir.Aggregate(
            task.engine,
            rel_builtins.count,
            task.projection,
            task.group,
            count_args,
        )

        final_sum = ir.Lookup(
            task.engine,
            rel_builtins.plus,
            tuple([new_sum, new_count, output_arg]),
        )

        return [
            sum_task,
            count_task,
            final_sum,
        ]

    def has_aggregate(self, task: ir.Task) -> bool:
        assert isinstance(task, ir.Logical)
        for subtask in task.body:
            if isinstance(subtask, ir.Aggregate):
                return True
        return False

class Compiler(c.Compiler):
    def __init__(self):
        # TODO: are these all needed from the Rel emitter?
        # TODO: should there be a pass to remove aliases from output?
        super().__init__([
            rewrite.Flatten(),

            # Adds missing existentials + splits multi-headed rules into single rules
            Splinter(),

            HoistAggregates(),
            NormalizeAggregates(),
        ])

    # TODO: what should return value be? string according to parents?
    def do_compile(self, model: ir.Model, options:dict={}) -> str:
        lqp_ir, debugging_ctx = Model2Lqp().to_lqp(model)
        self._lqp_result = lqp_ir
        lqp_str = lqp_ir.to_llqp()

        debug_str = ""
        if len(debugging_ctx.id_to_orig_name) > 0:
            debug_str += ";; Original names\n"

        for (rid, name) in debugging_ctx.id_to_orig_name.items():
            debug_str += ";; \t " + str(rid) + " -> `" + name + "`\n"

        if debug_str != "":
            lqp_str += "\n\n"
            lqp_str += ";; Debug information\n"
            lqp_str += ";; -----------------------\n"
            lqp_str += debug_str

        return lqp_str

    def get_lqp_ir(self) -> lqp.LqpProgram:
        """ Returns the LQP IR generated by the compiler. """
        assert self._lqp_result is not None, "LQP IR not generated yet"
        return self._lqp_result

class DebuggingCtx:
    """ Extra information only used for debugging. """
    def __init__(self, id_to_orig_name: dict[lqp.RelationId, str]):
       self.id_to_orig_name = id_to_orig_name

class Model2Lqp:
    """ Generates LQP IR from the model IR. """
    def __init__(self):
        # TODO: comment htese fields
        # TODO: should we have a pass to rename variables instead of this?
        self.var_name_cache: NameCache = field(default_factory=NameCache)
        self.id_to_orig_name: dict[lqp.RelationId, str] = field(default_factory=dict)
        self.output_ids: list[lqp.RelationId] = field(default_factory=list)

    """ Main access point. Converts the model IR to an LQP program. """
    def to_lqp(self, model: ir.Model) -> Tuple[lqp.LqpProgram, DebuggingCtx]:
        _assert_valid_input(model)
        self._reset_state()
        program = self._translate_to_program(model)
        debugging_ctx = DebuggingCtx(self.id_to_orig_name)
        return (program, debugging_ctx)

    def _reset_state(self):
        self.var_name_cache = NameCache()
        self.id_to_orig_name = {}
        self.output_ids = []

    def _translate_to_program(self, model: ir.Model) -> lqp.LqpProgram:
        decls: list[lqp.Declaration] = []
        outputs: list[Tuple[str, lqp.RelationId]] = []

        # LQP only accepts logical tasks
        # These are asserted at init time
        root = cast(ir.Logical, model.root)

        for subtask in root.body:
            # TODO: when do we get more than one?
            child_l = cast(ir.Logical, subtask)
            decl = self._translate_to_decl(child_l)
            for d in decl:
                assert isinstance(d, lqp.Declaration)
                decls.append(d)

        for output_id in self.output_ids:
            assert isinstance(output_id, lqp.RelationId)
            outputs.append(("output", output_id))

        return lqp.LqpProgram(decls, outputs)

    def _translate_to_decl(self, rule: ir.Logical) -> list[lqp.Declaration]:
        outputs = []
        updates = []
        body_tasks = []
        aggregates = []

        for task in rule.body:
            if isinstance(task, ir.Output):
                outputs.append(task)
            elif isinstance(task, ir.Lookup):
                body_tasks.append(task)
            elif isinstance(task, ir.Logical):
                body_tasks.append(task)
            elif isinstance(task, ir.Exists):
                body_tasks.append(task)
            elif isinstance(task, ir.Aggregate):
                aggregates.append(task)
            elif isinstance(task, ir.Update):
                updates.append(task)
            else:
                raise NotImplementedError(f"Unknown task type: {type(task)}")

        conjuncts = []
        for task in body_tasks:
            conjunct = self._translate_to_formula(task)
            conjuncts.append(conjunct)
        body = lqp.Conjunction(conjuncts) if len(conjuncts) != 1 else conjuncts[0]

        # TODO: unify all the def/rel-id generation
        if len(aggregates) > 0:
            assert len(outputs) == 0, "cannot have both outputs and aggregates"
            assert len(updates) == 1, "aggregates should derive into another relation"

            update = updates[0]
            assert isinstance(update, ir.Update)
            assert update.effect == ir.Effect.derive, "only derive supported at the moment"

            final_defs = []
            for aggr in aggregates:
                assert isinstance(aggr, ir.Aggregate)
                final_defs.append(self._translate_aggregate(aggr, body, update))

            return final_defs

        assert len(aggregates) == 0, "aggregates should have already been done"

        if len(outputs) > 0:
            assert len(outputs) == 1, "only one output supported at the moment"
            output = outputs[0]
            assert isinstance(output, ir.Output)
            output_vars = []
            for _, v in output.aliases:
                # TODO: we dont yet handle aliases
                assert isinstance(v, ir.Var)
                var = self._translate_to_var(v)
                output_vars.append(var)
            abstraction = lqp.Abstraction(output_vars, body)
            # TODO: is this correct? might need attrs tooo?
            rel_id = _gen_rel_id(abstraction)
            self.output_ids.append(rel_id)
            return [lqp.Def(rel_id, abstraction, [])]

        assert len(updates) == 1, "only one update supported at the moment"
        update = updates[0]
        assert isinstance(update, ir.Update)
        effect = update.effect
        assert effect == ir.Effect.derive, "only derive supported at the moment"

        args = []
        for var in update.args:
            assert isinstance(var, ir.Var)
            args.append(self._translate_to_var(var))

        abstraction = lqp.Abstraction(args, body)
        # TODO: is this correct? might need attrs tooo?
        rel_id = _gen_rel_id(abstraction)
        self.id_to_orig_name[rel_id] = update.relation.name
        return [lqp.Def(rel_id, abstraction, [])]

    def _translate_aggregate(self, aggr: ir.Aggregate, body: lqp.Formula, update: ir.Update) -> lqp.Def:
        assert isinstance(aggr, ir.Aggregate)

        # TODO: hadnle this properly
        aggr_name = aggr.aggregation.name
        assert aggr_name == "sum" or aggr_name == "count", f"only support sum or count for now, not {aggr.aggregation.name}"

        group_bys = []
        for arg in aggr.group:
            assert isinstance(arg, ir.Var)
            group_bys.append(self._translate_to_var(arg))

        projected_args = []
        for arg in aggr.projection:
            assert isinstance(arg, ir.Var)
            projected_args.append(self._translate_to_var(arg))

        # TODO: differentiate between results and more args
        result_args = []
        if aggr_name == "count":
            # TODO: this is wrong?? why sometimes it has two args and sometimes one :(
            assert len(aggr.args) >= 1
            result_args.append(lqp.Constant(1))
            output_arg = aggr.args[0]
            assert isinstance(output_arg, ir.Var)
            result_args.append(self._translate_to_var(output_arg))

        op = self._lqp_operator(aggr.aggregation)
        inner_abstr = lqp.Abstraction(
            group_bys,
            body,
        )
        reduce = lqp.Reduce(
            op,
            inner_abstr,
            result_args,
        )
        abstraction = lqp.Abstraction(
            projected_args,
            reduce,
        )
        rel_id = _gen_rel_id(abstraction)
        self.id_to_orig_name[rel_id] = update.relation.name
        return lqp.Def(rel_id, abstraction, [])

    def _lqp_sum_op(self) -> lqp.Abstraction:
        # TODO: make sure gensym'd properly
        vs = [
            lqp.Var("x", lqp.PrimitiveType.INT),
            lqp.Var("y", lqp.PrimitiveType.INT),
            lqp.Var("z", lqp.PrimitiveType.INT),
        ]

        body = lqp.Primitive("rel_primitive_add", [vs[0], vs[1], vs[2]])

        return lqp.Abstraction(vs, body)

    def _lqp_operator(self, op: ir.Relation) -> lqp.Abstraction:
        if op.name == "sum":
            return self._lqp_sum_op()
        elif op.name == "count":
            return self._lqp_sum_op()
        else:
            raise NotImplementedError(f"Unsupported aggregation: {op.name}")

    def _translate_to_formula(self, task: ir.Task) -> lqp.Formula:
        if isinstance(task, ir.Logical):
            conjuncts = []
            for child in task.body:
                conjunct = self._translate_to_formula(child)
                conjuncts.append(conjunct)
            return lqp.Conjunction(conjuncts)
        elif isinstance(task, ir.Lookup):
            return self._translate_to_atom(task)
        elif isinstance(task, ir.Exists):
            lqp_vars = []
            for var in task.vars:
                lqp_vars.append(self._translate_to_var(var))
            formula = self._translate_to_formula(task.task)
            return lqp.Exists(lqp_vars, formula)
        else:
            raise NotImplementedError(f"Unknown task type (formula): {type(task)}")

    def _translate_to_var(self, var: ir.Var) -> lqp.Var:
        name = self.var_name_cache.get_name(var.id, var.name)
        t = type_from_var(var)
        return lqp.Var(name, t)

    def _translate_to_atom(self, task: ir.Lookup) -> lqp.Formula:
        # TODO: want signature not name
        rel_name = task.relation.name
        assert isinstance(rel_name, str)
        terms = []
        sig_types = []
        for arg in task.args:
            if isinstance(arg, lqp.PrimitiveValue):
                term = lqp.Constant(arg)
                terms.append(term)
                t = type_from_constant(arg)
                sig_types.append(t)
                continue
            assert isinstance(arg, ir.Var)
            var = self._translate_to_var(arg)
            terms.append(var)
            sig_types.append(var.type)

        # TODO: wrong
        if rel_builtins.is_builtin(task.relation):
            return self._translate_builtin_to_primitive(task.relation, terms)

        return lqp.RelAtom(lqp.RelationSig(rel_name, sig_types), terms)

    def _translate_builtin_to_primitive(self, relation: ir.Relation, terms: list[lqp.Term]) -> lqp.Primitive:
        lqp_name = self._name_to_lqp_name(relation.name)
        return lqp.Primitive(lqp_name, terms)

    def _name_to_lqp_name(self, name: str) -> str:
        # TODO: do these proprly
        if name == "+":
            return "rel_primitive_add"
        elif name == "-":
            return "rel_primitive_subtract"
        elif name == "*":
            return "rel_primitive_multiply"
        elif name == "=":
            return "rel_primitive_eq"
        elif name == "<=":
            return "rel_primitive_lt_eq"
        else:
            raise NotImplementedError(f"missing primitive case: {name}")

def _gen_rel_id(abstr: lqp.Abstraction) -> lqp.RelationId:
    return lqp.RelationId(hash_to_uint128(_lqp_hash(abstr)))

# TODO: this is NOT a good hash its just to get things working for now to get
# a stable id.
def _lqp_hash(node: lqp.LqpNode) -> int:
    if isinstance(node, lqp.Abstraction):
        h1 = _lqp_hash_list(node.vars)
        h2 = _lqp_hash(node.value)
        return _lqp_hash_fn((h1, h2))
    elif isinstance(node, lqp.Exists):
        h1 = _lqp_hash_list(node.vars)
        h2 = _lqp_hash(node.value)
        return _lqp_hash_fn((h1, h2))
    elif isinstance(node, lqp.Conjunction):
        h1 = _lqp_hash_list(node.args)
        return _lqp_hash_fn((h1,))
    elif isinstance(node, lqp.Var):
        return _lqp_hash_fn((node.name, node.type))
    elif isinstance(node, lqp.Constant):
        return _lqp_hash_fn((node.value,))
    elif isinstance(node, lqp.RelAtom):
        h1 = _lqp_hash(node.sig)
        h2 = _lqp_hash_list(node.terms)
        return _lqp_hash_fn((h1, h2))
    elif isinstance(node, lqp.RelationSig):
        return _lqp_hash_fn((node.name, tuple(node.types)))
    elif isinstance(node, lqp.Primitive):
        h1 = _lqp_hash_fn(node.name)
        h2 = _lqp_hash_list(node.terms)
        return _lqp_hash_fn((h1, h2))
    elif isinstance(node, lqp.Reduce):
        h1 = _lqp_hash(node.op)
        h2 = _lqp_hash(node.body)
        h3 = _lqp_hash_list(node.terms)
        return _lqp_hash_fn((h1, h2, h3))
    else:
        raise NotImplementedError(f"Unsupported LQP node type: {type(node)}")

# TODO: this is NOT a good hash its just to get things working for now to get
# a stable id.
def _lqp_hash_fn(node) -> int:
    return int.from_bytes(hashlib.sha256(str(node).encode()).digest(), byteorder='big', signed=False)

def _lqp_hash_list(node: Sequence[lqp.LqpNode]) -> int:
    hashes = [_lqp_hash(n) for n in node]
    return hash(tuple(hashes))

def hash_to_uint128(h: int) -> int:
    return h % (2**128)  # Ensure it's within the 128-bit range

# Preconditions
def _assert_valid_input(model: ir.Model) -> bool:
    # TODO: flesh this out more?
    _assert_root_is_logical(model.root)
    return True

def _assert_root_is_logical(task: ir.Task) -> bool:
    assert isinstance(task, ir.Logical), f"expected logical task, got {type(task)}"
    for subtask in task.body:
        # TODO: assert what subtasks should look like
        assert isinstance(subtask, ir.Logical), f"expected logical task, got {type(subtask)}"

    return True

def type_from_var(arg: ir.Var) -> lqp.PrimitiveType:
    assert isinstance(arg, ir.Var)
    assert isinstance(arg.type, ir.ScalarType)
    if types.is_builtin(arg.type):
        # TODO: just ocompare to types.py
        if arg.type.name == "Int":
            return lqp.PrimitiveType.INT
        else:
            # TODO: fix this
            assert arg.type.name == "Any" or arg.type.name == "Number", f"Unknown type: {arg.type.name}"
            return lqp.PrimitiveType.UNKNOWN
    else:
        return lqp.PrimitiveType.UNKNOWN

def type_from_constant(arg: lqp.PrimitiveValue) -> lqp.PrimitiveType:
    if isinstance(arg, int):
        return lqp.PrimitiveType.INT
    elif isinstance(arg, float):
        return lqp.PrimitiveType.FLOAT
    elif isinstance(arg, str):
        return lqp.PrimitiveType.STRING
    else:
        raise NotImplementedError(f"Unknown constant type: {type(arg)}")

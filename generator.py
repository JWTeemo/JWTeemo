import string
from collections import namedtuple
import time
import lark
from config import target
from pathlib import Path
import importlib
from math import log, sqrt
import random
import uuid
import copy
import json
from utils import interact_with_harness

parser = lark.Lark(Path("grammar/fbnf.lark").read_text())
REPEAT_MAX = 8
MODULE_BASE = "module."
REPEAT_RAND_COUNT = 3
path = ""
Mutate_Type = None
# 0 : Content; 1: Structure
Mutate_Node = None

mutate_pool = []]

def mutate(value):
    # print(value, end=" -> ")
    global Mutate_Type, path
    if Mutate_Type == 0:
        type_ = random.choice([1, 2, 3])

        if type_ == 1:
            if random.randint(1, 10) == 1:
                num_bytes_to_insert = 100000000
            else:
                num_bytes_to_insert = random.randint(1, 1000)
            insert_position = random.randint(0, len(value))
            random_char = random.choice(string.ascii_letters)
            random_byte = random_char.encode('ascii')
            repeated_bytes = random_byte * num_bytes_to_insert
            value = value[:insert_position] + repeated_bytes + value[insert_position:]

        elif type_ == 2:
            if len(value) == 0:
                return value
            num_bytes_to_delete = random.randint(1, len(value))
            indices_to_delete = set(random.sample(range(len(value)), num_bytes_to_delete))
            value = bytes([b for i, b in enumerate(value) if i not in indices_to_delete])

        elif type_ == 3:
            if value.isdigit():
                new_length = random.randint(1, len(value) * 2)
                new_value = ''.join(random.choices('0123456789', k=new_length))
                value = new_value.encode()
            else:
                if len(value) == 0:
                    return value
                num_bytes_to_modify = random.randint(1, len(value))
                indices_to_modify = set(random.sample(range(len(value)), num_bytes_to_modify))
                value = bytes([
                    random.choice(string.ascii_letters).encode()[0] if i in indices_to_modify else b
                    for i, b in enumerate(value)
                ])
    else:
        type_ = random.choice([1, 2, 3])
        back_path = path
        if type_ == 1:
            value = b""
        elif type_ == 2:
            new_node = random.choice(mutate_pool)
            while new_node == Mutate_Node:
                new_node = random.choice(mutate_pool)
            new_value,_ = G.generate(new_node, False)
            value += new_value
        elif type_ == 3:
            new_node = random.choice(mutate_pool)
            while new_node == Mutate_Node:
                new_node = random.choice(mutate_pool)
            value, _ = G.generate(new_node, False)
        path = back_path
    # print(value)
    return value

def call_function(module_name: str, params: list):
    try:
        module = importlib.import_module(MODULE_BASE + module_name)
        func = getattr(module, "main")
        # print(module, params)
        return func(*params)

    except Exception as e:
        print(module_name, params, e)

class DAG:
    class Selector:
        class Record:
            def __init__(self, used=0, succ=0) -> None:
                self.used = used
                self.succ = succ

            def use(self) -> None:
                self.used += 1

            def success(self) -> None:
                self.succ += 1

            def __repr__(self) -> str:
                return repr({"used": self.used, "succ": self.succ})

        history = {}  # save all the records of the path, pair of (succ, fail)
        records = []

        def __init__(self) -> None:
            pass

        def choice(self, path: str, total: int, mcts: bool) -> int:
            if total == 1:
                return 0
            """ use UCT alrogithm to choose the next node """
            if not mcts:
                # self.history[path] = None
                return random.choice(range(total))
            if path in self.history:
                history = self.history[path]
            else:
                history = self.history[path] = [DAG.Selector.Record() for _ in range(total)]
            sum = 0
            for idx, rc in enumerate(history):
                if rc.used == 0:
                    rc.use()
                    self.records.append(rc)
                    return idx
                else:
                    sum += rc.used
            # UCB formula
            weight = [sqrt(2 * log(sum) / rc.used) + rc.succ / rc.used for rc in history]
            # choice = weight.index(max(weight))
            choice = random.choices(range(total), weight)[0]
            history[choice].use()
            self.records.append(history[choice])
            return choice

        def valid(self, records) -> None:
            """when the jwtpayload is valid, record success in history"""
            for r in records:
                r.success()

    class Node:
        Limit = namedtuple("Limit", ["min", "max"])

        def __init__(self, name: str, clause: lark.Tree, selector) -> None:
            self.name = name
            self.dag = clause
            self.selector = selector
            self.father = None
            while self.dag.data in ["clause", "brackets_set", "values", "brackets"]:
                self.dag = self.dag.children[0]

        def build(self, nodes: dict) -> None:
            if self.dag.data == "clause_or":
                self.type = "OR"
                self.items = []
                for idx, x in enumerate(self.dag.children):
                    node = DAG.Node(f"O{uuid.uuid4().hex}", x, self.selector)
                    self.items.append(node)
                    node.build(nodes)
            elif self.dag.data == "clause_and":
                self.type = "AND"
                self.items = []
                for idx, x in enumerate(self.dag.children):
                    node = DAG.Node(f"A{uuid.uuid4().hex}", x, self.selector)
                    self.items.append(node)
                    node.build(nodes)
            elif self.dag.data == "item":
                token = self.dag.children[0]
                if token.type == "TOKEN":
                    self.type = "NODE"
                    self.value = nodes[token.value]
                elif token.type == "STRING":
                    self.type = "STRING"
                    self.value = eval("b" + token.value)
                else:
                    raise NotImplementedError(self.dag.type)
            elif self.dag.data == "func":
                token = self.dag.children[0]
                self.type = "FUNC"
                self.items = []
                self.subject = token.value
                if len(self.dag.children) == 2:
                    params = self.dag.children[1]
                    for idx, x in enumerate(params.children):
                        node = DAG.Node(f"P{uuid.uuid4().hex}", x, self.selector)
                        self.items.append(node)
                        node.build(nodes)
                # print(self.type, token.value, len(self.dag.children))
            elif self.dag.data == "if_statement":
                self.type = "IF"
                node = DAG.Node(f"P{uuid.uuid4().hex}", self.dag.children[0], self.selector)
                self.subject = node
                self.items = []
                self.params = []
                node.build(nodes)
                condition = self.dag.children[1]
                for idx, x in enumerate(condition.children):
                    if len(x.children) == 2:
                        node = DAG.Node(f"P{uuid.uuid4().hex}", x.children[1], self.selector)
                        self.items.append((eval("b" + x.children[0].value), node))
                        node.build(nodes)
                    else:
                        node = DAG.Node(f"P{uuid.uuid4().hex}", x.children[0], self.selector)
                        self.items.append(node)
                        node.build(nodes)
                # params = self.dag.children[2]
                # for idx, x in enumerate(params.children):
                #     node = DAG.Node(f"P{uuid.uuid4().hex}", x, self.selector)
                #     self.params.append(node)
                #     node.build(nodes)
                pass
            elif self.dag.data.startswith("brackets_"):
                self.type = "REPEAT"
                self.limit = self.getLimit()
                node = DAG.Node(f"R{uuid.uuid4().hex}", self.dag.children[-1], self.selector)
                self.item = node
                node.build(nodes)
            elif self.dag.data.startswith("values_"):
                children = [x.value for x in self.dag.children]
                if "hex" in self.dag.data:
                    values = [int(x + y, 16) for x, y in zip(children[::2], children[1::2])]
                elif "dec" in self.dag.data:
                    values = [int(x) for x in children]
                else:
                    raise NotImplemented(self.dag.data)
                if "range" in self.dag.data:
                    L, R = values
                    self.type = "RANGE"
                    self.items = [bytes(bytearray([x])) for x in range(L, R + 1)]
                else:
                    self.type = "STRING"
                    self.value = bytes(bytearray(values))
            else:
                raise NotImplementedError(self.dag.data)

        def getNumber(self, dag: lark.Tree):
            assert dag.children[0].type == "NUMBER"
            return int(dag.children[0].value)

        def getLimit(self):
            children = self.dag.children
            if self.dag.data == "brackets_01":
                min, max = 0, 1
            if self.dag.data == "brackets_0n":
                min, max = 0, REPEAT_MAX
            if self.dag.data == "brackets_xy":
                min, max = self.getNumber(children[0]), self.getNumber(children[1])
            if self.dag.data == "brackets_xn":
                min, max = self.getNumber(children[0]), REPEAT_MAX
            if self.dag.data == "brackets_0x":
                min, max = 0, self.getNumber(children[0])
            if self.dag.data == "brackets_xx":
                min, max = self.getNumber(children[0]), self.getNumber(children[0])
            return DAG.Node.Limit(min, max)

        def generate(self, cache: dict, mcts: bool) -> bytes:
            global path
            if self.name in cache:
                return cache[self.name]
            path += "." + self.name # 全局变量
            # print(path)
            if self.type == "OR":
                res = self.items[self.selector.choice(path, len(self.items), mcts)].generate(cache, mcts)
            elif self.type == "AND":
                res = b"".join([x.generate(cache, mcts) for x in self.items])
            elif self.type == "NODE":
                res = self.value.generate(cache, mcts)
            elif self.type == "STRING":
                res = self.value
            elif self.type == "RANGE":
                res = self.items[self.selector.choice(path, len(self.items), mcts)]
            elif self.type == "FUNC":
                params = []
                # print(self.subject)
                for param in self.items:
                    params.append(param.generate(cache, mcts))
                # print(self.subject, ":", params)
                res = call_function(self.subject, params)
            elif self.type == "IF":
                key = self.subject.generate(cache, mcts)
                res = None
                for param in self.items:
                    if isinstance(param, tuple):
                        if key == param[0]:
                            res = param[1].generate(cache, mcts)
                            break
                    else:
                        # print(key, path, param.name)
                        res = param.generate(cache, mcts)

            elif self.type == "REPEAT":
                # brackets_xx
                if self.limit.min == self.limit.max:
                    return b"".join([self.item.generate({}, mcts) for _ in range(self.limit.min)])
                # brackets_01, brackets_xy, brackets_0x

                # print(self.name, self.limit.min , self.limit.max, REPEAT_MAX)
                if self.limit.max != REPEAT_MAX:
                    total = (
                        self.selector.choice(path, self.limit.max - self.limit.min + 1, mcts)
                        + self.limit.min
                    )
                    return b"".join([self.item.generate({}, mcts) for _ in range(total)])
                # brackets_0n, brackets_xn
                options = ["RAND"] + [self.limit.min + x for x in range(REPEAT_RAND_COUNT)]
                total = options[self.selector.choice(path, len(options), mcts)]
                if isinstance(total, int):
                    return b"".join([self.item.generate({}, mcts) for _ in range(total)])
                total = self.limit.min
                while random.randint(0, 1) and total < self.limit.max:
                    total += 1
                return b"".join([self.item.generate({}, mcts) for _ in range(total)])
            else:
                raise NotImplementedError(self.type)


            # print(self.name, res)
            if self.name == Mutate_Node:
                res = mutate(res)
            cache[self.name] = res
            return res

    nodes = {}
    mutate_pool = []
    cache = {}
    path = ""

    def __init__(self, grammar: str) -> None:
        self.selector = self.Selector()

        dag = parser.parse(grammar)

        # print(dag.pretty())

        for rule in dag.children:
            assert rule.data == "rule"
            name = rule.children[0].value
            clause = rule.children[1].children[0]
            self.nodes[name] = DAG.Node(name, clause, self.selector)

        for name in self.nodes:
            self.nodes[name].build(self.nodes)
            # print(name)



    def generate(self, node_name: str = None, mcts: bool = False):
        global path
        self.selector.records.clear()
        cache = {}
        path = "ROOT"
        data = self.nodes[node_name].generate(cache, mcts)
        return data, copy.copy(self.selector.records)
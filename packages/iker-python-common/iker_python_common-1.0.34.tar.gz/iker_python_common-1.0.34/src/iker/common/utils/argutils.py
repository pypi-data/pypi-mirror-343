import argparse
import inspect
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

from iker.common.utils.typeutils import is_identical_type, type_origin

__all__ = [
    "ParserTreeNode",
    "ParserTree",
    "ArgParseSpec",
    "argparse_spec",
    "make_argparse"
]

import sys


class ParserTreeNode(object):
    def __init__(self, command: str, parser: argparse.ArgumentParser):
        self.command = command
        self.parser = parser
        self.subparsers = None
        self.child_nodes: list[ParserTreeNode] = []


def construct_parser_tree(
    root_node: ParserTreeNode,
    command_chain: list[str],
    command_key_prefix: str,
    **kwargs,
) -> list[ParserTreeNode]:
    node_path = [root_node]
    if len(command_chain) == 0:
        return node_path

    node = root_node
    for depth, command in enumerate(command_chain):
        if node.subparsers is None:
            node.subparsers = node.parser.add_subparsers(dest=f"{command_key_prefix}:{depth}")
        for child_node in node.child_nodes:
            if child_node.command == command:
                node = child_node
                break
        else:
            if depth == len(command_chain) - 1:
                child_parser = node.subparsers.add_parser(command, **kwargs)
            else:
                child_parser = node.subparsers.add_parser(command)
            child_node = ParserTreeNode(command, child_parser)
            node.child_nodes.append(child_node)
            node = child_node
        node_path.append(node)

    return node_path


class ParserTree(object):
    def __init__(self, root_parser: argparse.ArgumentParser, command_key_prefix: str = "command"):
        self.root_node = ParserTreeNode("", root_parser)
        self.command_key_prefix = command_key_prefix

    def add_subcommand_parser(self, command_chain: list[str], **kwargs) -> argparse.ArgumentParser:
        *_, last_node = construct_parser_tree(self.root_node, command_chain, self.command_key_prefix, **kwargs)
        return last_node.parser

    def parse_args(self, args: list[str] | None = None) -> tuple[list[str], argparse.Namespace]:
        # Before Python 3.12 the 'exit_on_error' attribute does not take effect properly
        # if unknown arguments encountered. We have to employ this workaround
        # TODO: remove this workaround when bumping the Python versions to above Python 3.12
        if sys.version_info < (3, 12):
            if self.root_node.parser.exit_on_error:
                known_args_namespace = self.root_node.parser.parse_args(args)
            else:
                known_args_namespace, unknown_args = self.root_node.parser.parse_known_args(args)
                if len(unknown_args or []) > 0:
                    raise argparse.ArgumentError(None, f"unrecognized arguments '{unknown_args}'")
        else:
            known_args_namespace = self.root_node.parser.parse_args(args)

        command_pairs = []
        namespace = argparse.Namespace()
        for key, value in dict(vars(known_args_namespace)).items():
            if key.startswith(self.command_key_prefix) and value is not None:
                command_pairs.append((key, value))
            else:
                setattr(namespace, key, value)

        return list(command for _, command in sorted(command_pairs)), namespace


@dataclass(frozen=True)
class ArgParseSpec(object):
    flag: str | None = None
    name: str | None = None
    action: str | None = None
    default: Any = None
    type: type = None
    choices: list[Any] | None = None
    required: bool | None = None
    help: str | None = None


argparse_spec = ArgParseSpec


def make_argparse(func, parser: argparse.ArgumentParser = None) -> argparse.ArgumentParser:
    if parser is None:
        parser = argparse.ArgumentParser()

    def is_type_of(t: type, *types) -> bool:
        return any(is_identical_type(t, type_) for type_ in types)

    sig = inspect.signature(func)
    for name, param in sig.parameters.items():

        if param.annotation is None:
            param_type = str
        elif is_type_of(param.annotation, str, str | None, list[str], Sequence[str]):
            param_type = str
        elif is_type_of(param.annotation, int, int | None, list[int], Sequence[int]):
            param_type = int
        elif is_type_of(param.annotation, float, float | None, list[float], Sequence[float]):
            param_type = float
        elif is_type_of(param.annotation, bool, bool | None, list[bool], Sequence[bool]):
            param_type = bool
        else:
            param_type = str

        param_action = "append" if type_origin(param.annotation) in {list, Sequence} else None
        param_default = None if param.default is inspect.Parameter.empty else param.default

        if not isinstance(param_default, ArgParseSpec):
            param_name = f"--{name.replace('_', '-')}"

            parser.add_argument(param_name,
                                type=param_type,
                                action=param_action,
                                required=param_default is None,
                                default=param_default)

        else:
            spec = param_default

            param_flag = spec.flag
            param_name = spec.name or f"--{name.replace('_', '-')}"
            param_type = spec.type if spec.type is not None else param_type
            param_action = spec.action if spec.action is not None else param_action

            if param_flag is None:
                parser.add_argument(param_name,
                                    type=param_type,
                                    action=param_action,
                                    required=spec.default is None,
                                    default=spec.default,
                                    help=spec.help)
            else:
                parser.add_argument(param_flag,
                                    param_name,
                                    type=param_type,
                                    action=param_action,
                                    required=spec.default is None,
                                    default=spec.default,
                                    help=spec.help)

    return parser

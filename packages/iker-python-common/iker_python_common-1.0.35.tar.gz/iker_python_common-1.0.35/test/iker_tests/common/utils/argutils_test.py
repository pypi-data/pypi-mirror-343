import argparse
import unittest
from typing import List, Optional, Union

import ddt

from iker.common.utils.argutils import ParserTree
from iker.common.utils.argutils import make_argparse
from iker.common.utils.sequtils import seq


def dummy_parser_tree():
    parser_tree = ParserTree(argparse.ArgumentParser(description="dummy argument parser", exit_on_error=False))

    for command_chain in [
        [],
        ["foo"],
        ["foo", "bar"],
        ["foo", "baz"],
        ["bar"],
        ["bar", "foo"],
        ["bar", "baz"],
        ["baz", "foo"],
        ["baz", "bar"],
        ["baz", "bar", "foo"],
    ]:
        parser = parser_tree.add_subcommand_parser(command_chain, exit_on_error=False)

        option_infix = "-".join(command_chain)
        if len(option_infix) == 0:
            option_infix = "x"

        parser.add_argument(f"--option-{option_infix}-str", type=str, default="")
        parser.add_argument(f"--option-{option_infix}-int", type=int, default=0)
        parser.add_argument(f"--option-{option_infix}-float", type=float, default=0.0)
        parser.add_argument(f"--option-{option_infix}-switch", action="store_true")
        parser.add_argument(f"--option-{option_infix}-nargs", type=str, action="append", default=[])

    return parser_tree


@ddt.ddt
class ArgUtilsTest(unittest.TestCase):

    @ddt.data(
        (
            [],
            [],
            [
                ("option_x_str", ""),
                ("option_x_int", 0),
                ("option_x_float", 0.0),
                ("option_x_switch", False),
                ("option_x_nargs", []),
            ],
        ),
        (
            [
                "--option-x-str", "dummy",
                "--option-x-int", "1",
                "--option-x-float", "1e6",
                "--option-x-switch",
                "--option-x-nargs", "dummy_1",
                "--option-x-nargs", "dummy_2",
            ],
            [],
            [
                ("option_x_str", "dummy"),
                ("option_x_int", 1),
                ("option_x_float", 1e6),
                ("option_x_switch", True),
                ("option_x_nargs", ["dummy_1", "dummy_2"]),
            ],
        ),
        (
            ["foo"],
            ["foo"],
            [
                ("option_foo_str", ""),
                ("option_foo_int", 0),
                ("option_foo_float", 0.0),
                ("option_foo_switch", False),
                ("option_foo_nargs", []),
            ],
        ),
        (
            [
                "foo", "baz",
                "--option-foo-baz-str", "dummy",
                "--option-foo-baz-int", "1",
                "--option-foo-baz-float", "1e6",
                "--option-foo-baz-switch",
                "--option-foo-baz-nargs", "dummy_1",
                "--option-foo-baz-nargs", "dummy_2",
            ],
            ["foo", "baz"],
            [
                ("option_foo_baz_str", "dummy"),
                ("option_foo_baz_int", 1),
                ("option_foo_baz_float", 1e6),
                ("option_foo_baz_switch", True),
                ("option_foo_baz_nargs", ["dummy_1", "dummy_2"]),
            ],
        ),
        (
            [
                "baz", "foo",
                "--option-baz-foo-str", "dummy",
                "--option-baz-foo-int", "1",
                "--option-baz-foo-float", "1e6",
                "--option-baz-foo-switch",
                "--option-baz-foo-nargs", "dummy_1",
                "--option-baz-foo-nargs", "dummy_2",
            ],
            ["baz", "foo"],
            [
                ("option_baz_foo_str", "dummy"),
                ("option_baz_foo_int", 1),
                ("option_baz_foo_float", 1e6),
                ("option_baz_foo_switch", True),
                ("option_baz_foo_nargs", ["dummy_1", "dummy_2"]),
            ],
        ),
        (
            [
                "baz", "bar", "foo",
                "--option-baz-bar-foo-str", "dummy",
                "--option-baz-bar-foo-int", "1",
                "--option-baz-bar-foo-float", "1e6",
                "--option-baz-bar-foo-switch",
                "--option-baz-bar-foo-nargs", "dummy_1",
                "--option-baz-bar-foo-nargs", "dummy_2",
            ],
            ["baz", "bar", "foo"],
            [
                ("option_baz_bar_foo_str", "dummy"),
                ("option_baz_bar_foo_int", 1),
                ("option_baz_bar_foo_float", 1e6),
                ("option_baz_bar_foo_switch", True),
                ("option_baz_bar_foo_nargs", ["dummy_1", "dummy_2"]),
            ],
        ),
    )
    @ddt.unpack
    def test_parser_tree(self, args, expect_commands, expect_options):
        commands, args = dummy_parser_tree().parse_args(args)
        self.assertEqual(commands, expect_commands)
        for key, value in expect_options:
            self.assertEqual(getattr(args, key), value)

    @ddt.data(
        (["foo", "foo"],),
        (["foo", "--option-x-switch"],),
        (["foo", "bar", "--option-bar-foo-switch"],),
        (["baz", "foo", "bar"],),
    )
    @ddt.unpack
    def test_parser_tree__exception(self, args):
        with self.assertRaises(argparse.ArgumentError):
            dummy_parser_tree().parse_args(args)

    def test_make_argparse(self):
        args = [
            ("--param-int", "1", 1),
            ("--param-float", "2.0", 2.0),
            ("--param-str", "dummy", "dummy"),
            ("--param-int-or-none", "11", 11),
            ("--param-float-or-none", "22.0", 22.0),
            ("--param-str-or-none", "dummy-dummy", "dummy-dummy"),
            ("--param-none-or-int", "111", 111),
            ("--param-none-or-float", "222.0", 222.0),
            ("--param-none-or-str", "dummy-dummy-dummy", "dummy-dummy-dummy"),
            ("--param-typing-optional-int", "1111", 1111),
            ("--param-typing-optional-float", "2222.0", 2222.0),
            ("--param-typing-optional-str", "dummy-dummy-dummy-dummy", "dummy-dummy-dummy-dummy"),
            ("--param-typing-union-int-none", "11111", 11111),
            ("--param-typing-union-float-none", "22222.0", 22222.0),
            ("--param-typing-union-str-none", "dummy-dummy-dummy-dummy-dummy", "dummy-dummy-dummy-dummy-dummy"),
            ("--param-typing-union-none-int", "111111", 111111),
            ("--param-typing-union-none-float", "222222.0", 222222.0),
            ("--param-typing-union-none-str",
             "dummy-dummy-dummy-dummy-dummy-dummy",
             "dummy-dummy-dummy-dummy-dummy-dummy"),
            ("--param-list-int", "1111111", [1111111]),
            ("--param-list-float", "2222222.0", [2222222.0]),
            ("--param-list-str",
             "dummy-dummy-dummy-dummy-dummy-dummy-dummy",
             ["dummy-dummy-dummy-dummy-dummy-dummy-dummy"]),
            ("--param-typing-list-int", "11111111", [11111111]),
            ("--param-typing-list-float", "22222222.0", [22222222.0]),
            ("--param-typing-list-str",
             "dummy-dummy-dummy-dummy-dummy-dummy-dummy-dummy",
             ["dummy-dummy-dummy-dummy-dummy-dummy-dummy-dummy"]),
        ]

        def dummy_function(
            param_int: int,
            param_float: float,
            param_str: str,
            param_int_or_none: int | None,
            param_float_or_none: float | None,
            param_str_or_none: str | None,
            param_none_or_int: None | int,
            param_none_or_float: None | float,
            param_none_or_str: None | str,
            param_typing_optional_int: Optional[int],
            param_typing_optional_float: Optional[float],
            param_typing_optional_str: Optional[str],
            param_typing_union_int_none: Union[int, None],
            param_typing_union_float_none: Union[float, None],
            param_typing_union_str_none: Union[str, None],
            param_typing_union_none_int: Union[None, int],
            param_typing_union_none_float: Union[None, float],
            param_typing_union_none_str: Union[None, str],
            param_list_int: list[int],
            param_list_float: list[float],
            param_list_str: list[str],
            param_typing_list_int: List[int],
            param_typing_list_float: List[float],
            param_typing_list_str: List[str],
        ):
            params = (
                param_int,
                param_float,
                param_str,
                param_int_or_none,
                param_float_or_none,
                param_str_or_none,
                param_none_or_int,
                param_none_or_float,
                param_none_or_str,
                param_typing_optional_int,
                param_typing_optional_float,
                param_typing_optional_str,
                param_typing_union_int_none,
                param_typing_union_float_none,
                param_typing_union_str_none,
                param_typing_union_none_int,
                param_typing_union_none_float,
                param_typing_union_none_str,
                param_list_int,
                param_list_float,
                param_list_str,
                param_typing_list_int,
                param_typing_list_float,
                param_typing_list_str,
            )

            for param, (arg_name, arg_str_value, arg_value) in zip(params, args):
                self.assertEqual(param, arg_value, arg_name)

        parser = make_argparse(dummy_function)
        parsed_args = parser.parse_args(
            seq(args).map(lambda x: (lambda name, str_value, _: [name, str_value])(*x)).flatten().map(str),
        )

        dummy_function(**vars(parsed_args))

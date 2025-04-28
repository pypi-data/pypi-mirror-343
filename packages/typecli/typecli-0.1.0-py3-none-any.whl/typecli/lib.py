#!/bin/python

import argparse
import enum
import logging
import sys
from dataclasses import _MISSING_TYPE, MISSING, Field, dataclass
from typing import (
    Any,
    BinaryIO,
    Iterable,
    List,
    Optional,
    Sequence,
    TextIO,
    TypeVar,
    Union,
    cast,
    get_args,
    get_origin,
)

if sys.version_info >= (3, 10):
    from types import NoneType
else:
    NoneType = type(None)

T = TypeVar("T")

logger = logging.getLogger(__name__)


def arg(
    default: Union[T, _MISSING_TYPE] = MISSING,
    short="",
    help="",
    positional=False,
):
    """
    short只填字母不填"-"
    """
    if isinstance(default, list):
        # hack: pass list to factory
        factory: Any = default
        default = MISSING
    else:
        factory = MISSING

    kw_only = {"kw_only": False} if sys.version_info >= (3, 10) else {}

    field = Field(
        default=default,
        default_factory=factory,
        metadata={"positional": positional, "short": short, "help": help},
        init=True,
        repr=True,
        hash=None,
        compare=True,
        **kw_only,
    )
    return cast(T, field)


def build_positional(name: str, positional: bool, short: str):
    args: list[str] = []

    text = name.replace("_", "-")
    if positional:
        args.append(text)
    else:
        if short:
            args.append(f"-{short}")
        args.append(f"--{text}")

    return args


def is_primary(kind: type):
    return kind is bool or kind is int or kind is float or kind is str


def is_union(kind: type):
    """判断是否为Union[T]"""
    origin = get_origin(kind)
    return origin is Union


def extract_union(kind: type) -> tuple[type, ...]:
    assert is_union(kind)
    return get_args(kind)


def extract_union_anyway(kind: type) -> tuple[type, ...]:
    return extract_union(kind) if is_union(kind) else (kind,)


def is_optional(kind: type):
    """判断是否为Optional[T]"""
    if is_union(kind):
        args = extract_union(kind)
        return NoneType in args
    return False


def extract_optional(kind: type) -> list[type]:
    """提取Optional[T]中的T"""
    assert is_optional(kind)
    args = extract_union(kind)
    return list(t for t in args if t is not NoneType)


def is_list(kind: type):
    """判断是否为list[T]或List[T]"""
    origin = get_origin(kind)
    return origin is list or origin is List


def extract_list(kind: type) -> type:
    """提取list[T]中的T"""
    assert is_list(kind)
    args = get_args(kind)
    return args[0] if args else type


def extract_list_anyway(kind: type):
    return extract_list(kind) if is_list(kind) else kind


def build_argument(
    name: str,
    kind: type,
    default,
    short: str,
    is_positional: bool,
    help: str,
):
    positional = build_positional(name, is_positional, short)
    named: dict[str, Any] = {"help": help}

    if default is not None:
        named["default"] = default

    if is_optional(kind):
        just_kind = extract_optional(kind)
        assert just_kind is not bool, (
            f"{name} ({kind}): use bool instead of Optional[bool]"
        )

        named["default"] = None
    else:
        just_kind = extract_union_anyway(kind)

    if len(just_kind) > 1:
        assert not any(is_list(x) for x in just_kind), (
            f"{name} ({kind}): list[T] is exclusive with other types"
        )
    else:
        assert len(just_kind) == 1, f"{name} ({kind}): use a type except Never"

        inner_kind = just_kind[0]
        if is_list(inner_kind):
            inner_kind = extract_list(inner_kind)
            named["nargs"] = "*" if "default" in named else "+"

        variants = extract_union_anyway(inner_kind)
        if len(variants) > 1:
            assert not any(x is NoneType for x in variants), (
                f"{name} ({kind}) ({variants}): can't parse list[None]"
            )
        else:
            assert len(variants) == 1, (
                f"{name} ({kind}) ({variants}): use a type except Never"
            )

            variant = variants[0]

            if variant is bool:
                named["action"] = "store_true"
                named["default"] = False
            else:
                logger.debug(f"{build_argument.__name__}: variant of {kind}: {variant}")
                if issubclass(variant, enum.IntEnum):
                    named["choices"] = [
                        choice for x in variant for choice in (x.name, str(x.value))
                    ]
                    variant = str
                elif issubclass(variant, enum.Enum):
                    named["choices"] = [x.name for x in variant]
                    variant = str
                elif issubclass(variant, TextIO):
                    variant = argparse.FileType("r+")
                elif issubclass(variant, BinaryIO):
                    variant = argparse.FileType("rb+")
                elif not is_primary(variant):
                    logger.warning(f"unknown kind {variant}, name is {name}")

                named["type"] = variant

    """
        constraint of argparse.ArgumentParser: `TypeError: 'required' is an invalid argument for positionals`

        required/nargs:
                  positional
                    x    o
                x   o/   x/
        default o   x/   x/?
    """
    if "default" in named:
        if not positional[0].startswith("-"):
            named["nargs"] = "?"
    elif positional[0].startswith("-") or named.get("nargs") == "+":
        named["required"] = True
    return positional, named


def create_parser(members: Iterable[Field], exit_on_error: bool):
    parser = argparse.ArgumentParser(exit_on_error=exit_on_error)

    for member in members:
        meta = member.metadata

        if member.default is not MISSING:
            default = member.default
        elif member.default_factory is not MISSING:
            # hack: don't call factory, as it's a list actually
            default = member.default_factory
        else:
            default = None

        positional, named = build_argument(
            member.name,
            cast(type, member.type),
            default,
            meta.get("short", ""),
            meta.get("positional", False),
            meta.get("help", ""),
        )
        logger.debug(f"{create_parser.__name__}: {positional}, {named}")
        parser.add_argument(*positional, **named)
    return parser


def parse(cls: type[T], args: Optional[Sequence[str]] = None, strict=True):
    """strict: 若传入未声明的参数则报错"""

    clz = cast(Any, cls)
    if strict:
        raw = clz.parser.parse_args(args)
    else:
        raw, _ = clz.parser.parse_known_args(args)

    arg_map = vars(raw)

    for member in clz.__dataclass_fields__.values():
        name = member.name
        kinds = normalize_kind(member.type)

        value = arg_map[name]
        arg_map[name] = (
            [parse_in_order(kinds, x) for x in value]
            if isinstance(value, list)
            else parse_in_order(kinds, value)
        )

    return cls(**arg_map)


def cli(exit_on_error=True):
    """
    arg名称中的"_"会转成CLI参数的"-"
    bool类型arg默认Falsy
    禁用Optional[bool]类型
    其他Optional类型arg默认值为None
    数组默认值禁用`list_arg: list[int] = []`，正确写法为`list_arg: list[int] = arg(default=[])`
    其他类型arg无默认值则必需
    枚举类型arg根据枚举变体的名称解析CLI参数
    """

    def decorator(cls: type[T]):
        clz = cast(Any, cls)
        clz.parser = create_parser(clz.__dataclass_fields__.values(), exit_on_error)
        clz.parse = classmethod(parse)

        return cls

    return decorator


class AutoCli(type):
    def __new__(cls, name: str, bases: tuple[type, ...], attrs: dict[str, Any]):
        new_class = super().__new__(cls, name, bases, attrs)
        if bases:
            new_class = cli()(dataclass(new_class))
        return new_class


def parse_in_order(kinds: Iterable[Sequence[type]], value):
    ret = value
    for kind in (x for union in kinds for x in union):
        logger.debug(f"{parse_in_order.__name__}: {kind}, {value}")

        if kind is NoneType:
            assert value is None
            break

        if kind is str:
            break

        if issubclass(kind, enum.Enum):
            if isinstance(value, str):
                if value[0].isdecimal():
                    try:
                        ret = int(value)
                    except ValueError:
                        continue
                else:
                    try:
                        ret = kind.__members__[value]
                    except KeyError:
                        continue
            break

        try:
            ret = kind(value)
        except (TypeError, ValueError):
            pass
        else:
            break
    return ret


def normalize_kind(kind: type):
    """resolve enum and union from value"""

    kinds = extract_union_anyway(kind)

    # handles Optional[list[T]]
    unions = (extract_list_anyway(kind) for kind in kinds)

    # handles list[Union[T, U]]
    return [extract_union_anyway(kind) for kind in unions]


class Parser(metaclass=AutoCli):
    __dataclass_fields__: dict[str, Field]
    parser: argparse.ArgumentParser

    def __init__(self, *_, **__): ...

    @classmethod
    def parse(cls: type[T], args: Optional[Sequence[str]] = None, strict=True) -> T: ...


if __name__ == "__main__" and __debug__:

    def test_positional():
        class Args(Parser):
            foo: str = arg(positional=True)

        args = Args.parse(["bar"])

        assert args.foo == "bar"

    def test_required_positional():
        @cli(exit_on_error=False)
        class Args(Parser):
            foo: str = arg(positional=True)

        try:
            Args.parse([])
        except argparse.ArgumentError:
            pass
        else:
            assert False

        args = Args.parse(["bar"])
        assert args.foo == "bar"

    def test_default_positional():
        class Args(Parser):
            foo: str = arg(default="bar", positional=True)

        args = Args.parse([])

        assert args.foo == "bar"

    def test_required():
        @cli(exit_on_error=False)
        class Args(Parser):
            foo: str

        try:
            Args.parse([])
        except argparse.ArgumentError:
            pass
        else:
            assert False

        args = Args.parse(["--foo", "bar"])
        assert args.foo == "bar"

    def test1():
        class Args(Parser):
            vip: bool
            coins: int
            name: str = arg(short="n", help="person name")
            male: bool
            age: Optional[int]
            is_ok: bool
            height: int = 190

        args = Args.parse(["--name", "iw", "--hei", "3", "--co", "3"])

        assert args.name == "iw"
        assert not args.male
        assert args.age is None
        assert not args.vip
        assert args.coins == 3
        assert not args.is_ok
        assert args.height == 3

    def test2():
        class Args(Parser):
            verbose: bool = arg(help="Enable verbose output")
            output_file: Optional[str] = arg(help="Path to the output file")
            targets: list[str] = arg(short="t")
            numbers: list[int] = arg(short="n", help="List of numbers to process")
            input_file: str = arg(default="input.txt", help="Path to the input file")

        args = Args.parse(["-t", "a", "-n", "1", "2"])
        assert isinstance(args, Args)
        assert not args.verbose
        assert args.targets == ["a"]
        assert args.output_file is None
        assert args.input_file == "input.txt"
        assert args.numbers == [1, 2]

    def test_construct():
        class Args(Parser):
            verbose: bool = arg(help="Enable verbose output")
            output_file: Optional[str] = arg(help="Path to the output file")
            targets: list[str] = arg(short="t")
            numbers: list[int] = arg(short="n", help="List of numbers to process")
            input_file: str = arg(default="input.txt", help="Path to the input file")

        args = Args(verbose=False, output_file=None, targets=["a"], numbers=[1, 2])
        assert isinstance(args, Args)
        assert not args.verbose
        assert args.targets == ["a"]
        assert args.output_file is None
        assert args.input_file == "input.txt"
        assert args.numbers == [1, 2]

    def test_default_list():
        class Args(Parser):
            a: list[int] = arg(default=[])
            b: list[str] = arg(default=[])

        args = Args.parse([])
        assert isinstance(args, Args)
        assert args.a == []
        assert args.b == []
        assert id(args.a) != id(args.b)

    def test_optional_list():
        class Args(Parser):
            a: Optional[list[int]]
            b: list[str] = arg(default=[])

        args = Args.parse([])
        assert isinstance(args, Args)
        assert args.a is None
        assert args.b == []

    def test_union():
        class Args(Parser):
            e: Union[int, str, None]

        none = Args.parse([]).e
        assert none is None, f"{none!r}"

        num = Args.parse(["--e", "1"]).e
        assert num == 1, f"{num!r}"

        s = Args.parse(["--e", "1a"]).e
        assert s == "1a", f"{s!r}"

    def test_union_with_default_str():
        class Args(Parser):
            host: Union[int, str] = arg(default="127.0.0.1")

        default = Args.parse([]).host
        assert default == "127.0.0.1", f"{default!r}"

        num = Args.parse(["--host", "42"]).host
        assert num == 42, f"{num!r}"

        localhost = Args.parse(["--host", "localhost"]).host
        assert localhost == "localhost", f"{localhost!r}"

    def test_union_with_default_int():
        class Args(Parser):
            host: Union[int, str] = arg(default=68)

        default = Args.parse([]).host
        assert default == 68, f"{default!r}"

        num = Args.parse(["--host", "42"]).host
        assert num == 42, f"{num!r}"

        localhost = Args.parse(["--host", "localhost"]).host
        assert localhost == "localhost", f"{localhost!r}"

    def test_optional_union():
        class Args(Parser):
            host: Optional[Union[int, str]]

        default = Args.parse([]).host
        assert default is None, f"{default!r}"

        num = Args.parse(["--host", "42"]).host
        assert num == 42, f"{num!r}"

        localhost = Args.parse(["--host", "127.0.0.1"]).host
        assert localhost == "127.0.0.1", f"{localhost!r}"

    def test_enum():
        class E(enum.Enum):
            a = enum.auto()
            b = enum.auto()

        class Args(Parser):
            e: E
            s: str = "s"

        args = Args.parse(["--e", "a"])
        assert isinstance(args, Args)
        assert args.e == E.a, args.e
        assert args.s == "s", args.s

    def test_default_enum():
        class E(enum.Enum):
            a = enum.auto()
            b = enum.auto()

        class Args(Parser):
            e: E = E.b
            s: str = "s"

        args = Args.parse([])
        assert isinstance(args, Args)
        assert args.e == E.b, args.e
        assert args.s == "s", args.s

    def test_optional_enum():
        class E(enum.Enum):
            a = enum.auto()
            b = enum.auto()

        class Args(Parser):
            e: Optional[E]

        none = Args.parse([]).e
        assert none is None, none

        just = Args.parse(["--e", "a"]).e
        assert just == E.a, just

    def test_int_enum():
        class E(enum.IntEnum):
            a = 1
            b = 2

        class Args(Parser):
            e: E

        value_args = Args.parse(["--e", "1"])
        assert isinstance(value_args, Args)
        assert value_args.e == E.a, value_args.e

        name_args = Args.parse(["--e", "b"])
        assert isinstance(name_args, Args)
        assert name_args.e == E.b, name_args.e

    def test_enum_list():
        class SubApp(enum.Enum):
            radio = enum.auto()
            sound = enum.auto()
            wifi = enum.auto()

        class Args(Parser):
            run: list[SubApp] = arg(default=[SubApp.radio, SubApp.sound, SubApp.wifi])

        assert (x := Args.parse([]).run) == [SubApp.radio, SubApp.sound, SubApp.wifi], x
        assert Args.parse(["--run"]).run == []
        assert (x := Args.parse(["--run", "radio"]).run) == [SubApp.radio], x
        assert (x := Args.parse(["--run", "radio", "wifi"]).run) == [
            SubApp.radio,
            SubApp.wifi,
        ], x

    def test_io():
        class Args(Parser):
            input: TextIO = arg(positional=True)
            output: TextIO = arg(default=sys.stdout, short="o")

        args = Args.parse(["-"])
        assert isinstance(args, Args)
        assert args.input == sys.stdin
        assert args.output == sys.stdout

    def test_complicated():
        class Choice(enum.IntEnum):
            foo = 42
            bar = 24

        class Args(Parser):
            a: Optional[list[Union[Choice, int, str]]]

        none = Args.parse([]).a
        assert none is None

        empty = Args.parse(["--a"]).a
        assert empty == []

        # `Choice` is declared before `str` in `Union[Choice, int, str]`, so "bar" will be treated as Choice.bar instead of "bar"
        array = Args.parse(["--a", "42", "68", "1a", "bar"]).a
        assert array == [Choice.foo, 68, "1a", Choice.bar]

    class Args(Parser):
        debug: bool = arg(short="g")

    logging.basicConfig(level=logging.DEBUG if Args.parse().debug else logging.INFO)

    test_positional()
    logger.info("test positional passed")
    test_required_positional()
    logger.info("test required positional passed")
    test_default_positional()
    logger.info("test default positional passed")
    test_required()
    logger.info("test required passed")
    test1()
    logger.info("test 1 passed")
    test_construct()
    logger.info("test construct passed")
    test2()
    logger.info("test 2 passed")
    test_default_list()
    logger.info("test default list passed")
    test_optional_list()
    logger.info("test optional list passed")
    test_union()
    logger.info("test union passed")
    test_union_with_default_str()
    logger.info("test union with default str passed")
    test_union_with_default_int()
    logger.info("test union with default int passed")
    test_optional_union()
    logger.info("test optional union passed")
    test_enum()
    logger.info("test enum passed")
    test_default_enum()
    logger.info("test default enum passed")
    test_optional_enum()
    logger.info("test optional enum passed")
    test_int_enum()
    logger.info("test int enum passed")
    test_enum_list()
    logger.info("test enum list passed")
    test_io()
    logger.info("test io passed")
    test_complicated()
    logger.info("test complicated passed")

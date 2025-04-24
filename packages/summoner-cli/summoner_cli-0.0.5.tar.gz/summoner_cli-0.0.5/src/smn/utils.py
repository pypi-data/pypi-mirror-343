#!/usr/bin/env python3
from __future__ import annotations

from contextlib import contextmanager
from os import PathLike
from shlex import quote
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Generator,
    List,
    Optional,
    Tuple,
    Union,
    overload,
)
from warnings import warn

import click
from invoke.exceptions import UnexpectedExit
from pyre_extensions import none_throws

if TYPE_CHECKING:
    from smn.context import Context


def get_context() -> Context:
    return click.get_current_context().obj


def esc(s: str | PathLike[str]) -> str:
    return quote(str(s))


@contextmanager
def exit_on_failure() -> Generator[None, None, None]:
    """Simple context manager for exiting on failure during command execution.

    This is a context manager which will capture any nonzero exit code raised
    during command execution, raising it via click to avoid a long stack trace
    while still providing accurate command status. This is somewhat similar to
    set -e in a shell script.

    with exit_on_failure():
        ctx.run("exit 1")
    """

    try:
        yield
    except UnexpectedExit as e:
        raise click.exceptions.Exit(e.result.exited)


def build_command(*args: Union[str, List[str]]) -> str:
    """ "Build" a command.

    Given strings and lists of strings, this will "flatten" them into a single
    string, to be used as the input to an invoked command. Empty strings and
    lists are also filtered out.

    Args:
        *args: Union[str, List[str]]. Components to build command with.

    Returns:
        command: str. Built command string.
    """

    command = []

    for arg in args:
        if type(arg) is list and arg:
            # If arg is a non-empty list, build it and add to command.
            command.append(build_command(*arg))
        elif arg != "":
            # Append all non-blank arguments.
            command.append(arg)

    return " ".join(command)


# Taken from: https://github.com/click-contrib/click-default-group
# (Most) type hints added. Also removed the custom HelpFormatter as it isn't
# really necessary.
class DefaultGroup(click.Group):
    """Click command group with default command functionality.

    Invokes a subcommand marked with `default=True` if any subcommand not
    chosen.

    Args:
        default_if_no_args: Resolves to the default command if no arguments passed.

    Public Attributes:
        default_cmd_name: Optional[str]. Name of the command currently set as
            default, if any.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        # To resolve as the default command.
        if not kwargs.get("ignore_unknown_options", True):
            raise ValueError("Default group accepts unknown options")

        self.ignore_unknown_options = True
        self.default_cmd_name: Optional[str] = kwargs.pop("default", None)
        self.default_if_no_args: bool = kwargs.pop("default_if_no_args", False)

        super().__init__(*args, **kwargs)

    def set_default_command(self, command: click.Command) -> None:
        """Sets a command function as the default command."""
        cmd_name = command.name

        self.add_command(command)
        self.default_cmd_name = cmd_name

    def parse_args(self, ctx: click.Context, args: List[str]) -> List[str]:
        if not args and self.default_if_no_args:
            args.insert(0, none_throws(self.default_cmd_name))

        return super().parse_args(ctx, args)

    def get_command(self, ctx: click.Context, cmd_name: str) -> Optional[click.Command]:
        if cmd_name not in self.commands:
            # No command name matched.
            # pyre-fixme[16]: `click.core.Context` has no attribute `arg0`.
            ctx.arg0 = cmd_name
            cmd_name = none_throws(self.default_cmd_name)

        return super().get_command(ctx, cmd_name)

    def resolve_command(
        self, ctx: click.Context, args: List[str]
    ) -> Tuple[Optional[str], Optional[click.Command], List[str]]:
        cmd_name, cmd, args = super().resolve_command(ctx, args)
        if cmd and hasattr(ctx, "arg0"):
            # pyre-fixme[16]: `click.core.Context` has no attribute `arg0`.
            args.insert(0, ctx.arg0)
            cmd_name = cmd.name

        return cmd_name, cmd, args

    @overload
    def command(self, __func: Callable[..., Any]) -> click.Command: ...

    @overload
    # pyre-fixme[3]: Return type must be specified as type that does not contain `Any`.
    def command(
        self, *args: Any, **kwargs: Any
    ) -> Callable[[Callable[..., Any]], click.Command]: ...

    def command(
        self, *args: Any, **kwargs: Any
    ) -> Union[Callable[[Callable[..., Any]], click.Command], click.Command]:
        default = kwargs.pop("default", False)
        # pyre-fixme[33]: Expression `decorator` is used as type `click.core.Command`;
        # given explicit type cannot contain `Any`.
        decorator: Callable[[Callable[..., Any]], click.Command] = super().command(
            *args, **kwargs
        )

        if not default:
            return decorator

        warn(
            "Use default param of DefaultGroup or set_default_command() instead",
            DeprecationWarning,
        )

        # pyre-fixme[2]: Parameter `f` must have a type that does not contain `Any`.
        def _decorator(f: Callable[..., Any]) -> click.Command:
            cmd: click.core.Command = decorator(f)
            self.set_default_command(cmd)
            return cmd

        return _decorator

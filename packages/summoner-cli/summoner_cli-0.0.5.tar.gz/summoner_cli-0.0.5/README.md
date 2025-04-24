# Summoner (smn)

Summoner (`smn`) is a macro-utility for defining lightweight python based
automations using [fabric](https://github.com/fabric/fabric) and [click](https://github.com/pallets/click).

# Getting Started
## TL; DR

The quickest way to start using the CLI is with the 
[uv](https://github.com/astral-sh/uv) package manager:

```bash
# See uv README for other installation options
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install summoner-cli
alias smn='uvx --from summoner-cli smn'

# Clone and run smn against the example tome
git clone https://github.com/adammillerio/smn.git
smn --smn-help
smn hello
```

## Detailed

Summoner can be installed via pip or any other package manager:

```bash
pip install summoner-cli
```

Commands are loaded into Summoner via a "Tome", which is just a Python file that
defines Commands and Groups using the Click CLI framework. This file can import
other files or define commands directly.

A basic hello world example (`hello_world.py`):

```python
#!/usr/bin/env python3
from smn import tome, Context, pass_context


@tome.command("hello")
@pass_context
def hello(ctx: Context) -> None:
    """world!"""

    ctx.run("echo \"hello $(hostname)!\"", echo=True)

```

This command can then be executed both locally by default, or on any remote SSH
host via the `-H` (`--host`) flag:

```bash
aemiller@izalith> smn --tome hello_world.py hello
echo "hello $(hostname)!"
hello izalith!
aemiller@izalith> smn --tome hello_world.py -H ravenholm hello
echo "hello $(hostname)!"
hello ravenholm!
```

In this example, `ravenholm` is a host defined in the local `~/.ssh/config`, which
is loaded similarly to the `ssh` CLI:
```bash
Host ravenholm
    HostName ravenholm.domain.local
    ...
```

An example tome with some basic commands is provided at [tome.py](tome.py). Summoner
will load `./tome.py` by default if `--tome` is not provided. There is also an
environment variable `SMN_TOME` as an alternative.


You can explore available tomes by invoking them with the `--smn-help` option:
```bash
smn --tome hello_world.py --smn-help
Usage: smn [OPTIONS] COMMAND [ARGS]...

  a macro command runner

Options:
  --tome FILE          directly specify path to root tome
  --tree               enable tree display
  --dry-run            enable dry-run mode
  --disable-execution  disable all command execution
  --debug              output additional debug info
  -H, --host TEXT      host to run commands on via ssh, defaults to local
                       execution
  --smn-help           Show this message and exit.

Commands:
  hello  world!
```

Or view a command tree with the `--tree` option:
```bash
smn --tome hello_world.py --tree
smn
+-- hello - world!
```

# Usage
`smn` is best explained via hands on examples. This will demonstrate adding a 
single task to `smn`.

## The Goal
Write a tome with a task which, when given invoked with `--name`, will retrieve 
the current machine hostname and return the message:

```
Hello {name}! This is {machine}.
```

It should also run `uname -a` to print current system info.

## Create the Tome and Task

"Tome" files are really just python files that register new click Commands and 
Groups to a root "tome". There's no enforced naming convention, but typically 
they are named `tome.py`. For this example, we will place it in the hello
directory:

`hello/tome.py`:
```python
#!/usr/bin/env python3
from socket import gethostname

import click

from smn import Context, pass_context, tome


@tome.command("hello", help="Greet a user and show system information.")
@click.option("--name", type=str, help="Name to greet", required=True)
@pass_context
def hello(ctx: Context, name: str) -> None:
    machine = gethostname()

    click.secho(f"Hello, {name}! This is {machine}.", fg="green")

    ctx.run("uname -a")

```

Task composition is just standard Click, with the option of passing in a Fabric
Connection/Context if needed for things like running system commands.

One important general design aspect of `smn` is that tomes and their tasks should 
be largely free of dependencies. Other CLI interfaces are intended to have flexible
interfaces, so they should be invoked as commands rather than in code.

## Register the Tome
To register the tome, create a root `tome.py` and import the `hello` tome that
was just created:

`tome.py`:
```python
from hello.tome import __name__
```

This will import the tome, which will register it to the `smn` root tome. When
`smn` is invoked without the `--tome` option, it will look in the current directory
and all parent directories until it finds a `tome.py` file to load.

## Run the Tome and Command
At this point the Tome is registered and is visible in the root tome `--smn-help`:
```bash
smn --smn-help
...
Commands:
  hello        Greet a user and show system information.
```

And running it will print the expected output:
```bash
smn hello --name 'Foo'
Hello, Foo! This is izalith.
Darwin izalith 23.3.0 Darwin Kernel Version 23.3.0: Wed Dec 20 21:30:59 PST 2023; root:xnu-10002.81.5~7/RELEASE_ARM64_T6030 arm64
```

# Advanced Usage

## Groups

Click Groups can be used to define multiple commands under a single tome, similar 
to how Invoke task files work. This adjusts the above example to turn `hello` 
into a group, and provide subcommands for a day and night greeting:

`hello/tome.py`:
```python
#!/usr/bin/env python3
from socket import gethostname

import click

from smn import Context, pass_context, tome


@tome.group("hello", short_help="Greet a user and show system information.")
@click.option("--name", type=str, help="Name to greet", required=True)
@pass_context
def hello(ctx: Context, name: str) -> None:
    machine = gethostname()

    click.secho(f"Hello, {name}! This is {machine}.", fg="green")

    ctx.run("uname -a")


@hello.command("day", help="Greet a user in the day.")
def hello_day() -> None:
    click.secho("Have a good day.")


@hello.command("night", help="Greet a user in the night.")
def hello_night() -> None:
    click.secho("Have a good night.")

```

Like any Click Group, this allows for clustering of shared code and arguments in 
the group definition:

```bash
smn hello --name 'Foo' day
Hello, Foo! This is izalith.
Darwin izalith 23.3.0 Darwin Kernel Version 23.3.0: Wed Dec 20 21:30:59 PST 2023; root:xnu-10002.81.5~7/RELEASE_ARM64_T6030 arm64
Have a good day.

smn hello --name 'Foo' night
Hello, Foo! This is izalith.
Darwin izalith 23.3.0 Darwin Kernel Version 23.3.0: Wed Dec 20 21:30:59 PST 2023; root:xnu-10002.81.5~7/RELEASE_ARM64_T6030 arm64
Have a good night.
```

## Click Context

If you need to share data within your tome, you can pass in the default Click Context. 

For example, to instead store the first message as an initial greeting so it can 
be included on one line:

`hello/tome.py`:
```python
#!/usr/bin/env python3
from socket import gethostname

import click

from smn import Context, pass_context, tome


@tome.group("hello", short_help="Greet a user and show system information.")
@click.option("--name", type=str, help="Name to greet", required=True)
@pass_context
@click.pass_context
def hello(click_ctx: click.Context, ctx: Context, name: str) -> None:
    machine = gethostname()

    click_ctx.obj["initial_greeting"] = f"Hello, {name}! This is {machine}."

    ctx.run("uname -a")


@hello.command("day", help="Greet a user in the day.")
@click.pass_context
def hello_day(click_ctx: click.Context) -> None:
    initial_greeting = click_ctx.obj["initial_greeting"]

    click.secho(f"{initial_greeting} Have a good day.", fg="green")


@hello.command("night", help="Greet a user in the night.")
@click.pass_context
def hello_night(click_ctx: click.Context) -> None:
    initial_greeting = click_ctx.obj["initial_greeting"]

    click.secho(f"{initial_greeting} Have a good night.", fg="green")

```

```bash
smn hello --name 'Foo' day
Darwin izalith 23.3.0 Darwin Kernel Version 23.3.0: Wed Dec 20 21:30:59 PST 2023; root:xnu-10002.81.5~7/RELEASE_ARM64_T6030 arm64
Hello, Foo! This is izalith. Have a good day.

smn hello --name 'Foo' night
Darwin izalith 23.3.0 Darwin Kernel Version 23.3.0: Wed Dec 20 21:30:59 PST 2023; root:xnu-10002.81.5~7/RELEASE_ARM64_T6030 arm64
Hello, Foo! This is izalith. Have a good night.
```

`obj` is basically just a normal "typeless" key/value dictionary, so use it carefully.

## Aliases

Command aliases can be created by using the `add_command` method on any defined 
Click Command or Group, including the root tome:
```python
#!/usr/bin/env python3
from smn import Context, pass_context, tome


@tome.group("sl", short_help="Run sapling SCM")
def sapling() -> None:
    pass


@sapling.command("pull-rebase", help="Pull repo and rebase current commit to latest")
@pass_context
def pull_rebase(ctx: Context) -> None:
    pass


# If name is not provided, it will just use the command's name (pull-rebase).
tome.add_command(pull_rebase, name="pull")

```

Now the `pull` command is bound to both `smn pull` and `smn sl pull-rebase`:
```bash
smn --smn-help
Commands
  ...
  pull         Pull repo and rebase current commit to latest
  sl           Run sapling SCM

smn sl --smn-help
Commands:
  ...
  pull  Pull repo and rebase current commit to latest
```

## Entrypoints

Many tomes work based on the concept of an "entrypoint". To give an example, here 
is a tome for the sapling SCM, which includes an entrypoint, as well as an 
additional command `smn sl pull-rebase`, which is a macro that performs `sl pull` 
and `sl rebase -d remote/main`:

```python
#!/usr/bin/env python3
from typing import Tuple

import click

from smn import Context, pass_context, tome
from smn.utils import Defaultgroup


@tome.group(
    name="sl", cls=DefaultGroup, default_if_no_args=True, short_help="Run sapling SCM"
)
def sapling() -> None:
    pass


@sapling.command(
    "smn-run",
    default=True,
    help="Run sapling (sl)",
    context_settings={"ignore_unknown_options": True},
)
@click.argument("command", nargs=-1, type=click.UNPROCESSED)
@pass_context
def smn_run(ctx: Context, command: Tuple[str, ...]) -> None:
    ctx.run_entrypoint("sl", command)


@sapling.command(
    "pull-rebase", help="Pull repo and rebase current commit to latest"
)
@pass_context
def pull_rebase(ctx: Context) -> None:
    ctx.run("sl pull", pty=True)
    ctx.run("sl rebase -d remote/main", pty=True, warn=True)


# Also register "pull" to the root tome.
tome.add_command(pull_rebase)

```

This makes invocation of the `smn sl` tome with no matching command behave as a 
transparent entrypoint into the `sl` binary itself. When combined with a shell 
alias, this effectively allows for "patching" other tools to provide additional 
commands:
```bash
alias sl='smn sl'
sl pull       
pulling from https://github.com/adammillerio/smn.git
sl pull-rebase
pulling from https://github.com/adammillerio/smn.git
abort: uncommitted changes
```

Entrypoints and default tome commands are always named `smn-run`, so they are 
clearly identifiable and do not collide with subcommands of the entrypoint.They 
can also be run like any other command. Pass the `--smn-help` option at any time 
to override entrypoint behavior and view tome information:
```bash
smn sl --help
Sapling SCM

sl COMMAND [OPTIONS]

smn sl --smn-help
Commands:
  pull-rebase  Pull repo and rebase current commit to latest
  run          Run sapling (sl)
```

There are a few important Click behavioral changes made here to facilitate this:
* A custom `DefaultGroup` click.Group class is used. This provides default command 
  functionality.
	* If the group is invoked with no arguments, then the default command will 
      be run.
* The run command is created with `default=True`, indicating it is the default 
  command for this group when no commands are matched.
* The context for run is configured with `ignore_unknown_options=True`. This causes 
  click to forward all options it does not recognize from here on as arguments. 
  This is required for the transparent passthrough of arguments in commands like 
  `smn sl --help`.
* The run command is configured with `nargs=-1` and `type=click.UNPROCESSED`. 
  This instructs click to pass through all arguments exactly as received with no 
  string processing.

## Standardizing Commands

Standardizing commands can be done by creating utilities to generate common
click Command and Group definitions. For example, to make a standard command
for controlling lights via the `hass-cli`:

```python
#!/usr/bin/python3
from math import ceil, floor
from typing import Any, Dict
from json import loads

import click

from smn import Context

def get_state_command(ctx: Context, entity_id: str) -> Dict[str, Any]:
    result = loads(
        ctx.run(
            f"hass-cli --output ndjson state get {entity_id}",
            hide=not ctx.smn_debug,
            pty=False,
        ).stdout,
    )

    if result:
        return result[0]
    else:
        raise ValueError(f"No entity with name {entity_id} found")


def get_state(ctx: Context, entity_id: str) -> str:
    return get_state_command(ctx, entity_id)["state"]


def toggle_command(ctx: Context, entity_id: str) -> None:
    ctx.run(
        f"hass-cli service call homeassistant.toggle --arguments entity_id={entity_id}",
        hide=not ctx.smn_debug,
    )


def on_command(ctx: Context, entity_id: str, **kwargs: str) -> None:
    arguments = ",".join([f"{key}={value}" for key, value in kwargs.items()])

    ctx.run(
        f"hass-cli service call homeassistant.turn_on --arguments entity_id={entity_id},{arguments}",
        hide=not ctx.smn_debug,
    )


def off_command(ctx: Context, entity_id: str) -> None:
    ctx.run(
        f"hass-cli service call homeassistant.turn_off --arguments entity_id={entity_id}",
        hide=not ctx.smn_debug,
    )


def set_brightness_command(ctx: Context, entity_id: str, level: int) -> None:
    # Brightness is 0-255 in HA, but 0-100 is more intuitive in a CLI.
    on_command(ctx, entity_id, brightness=str(ceil(level * 2.55)))


def get_level(ctx: Context, entity_id: str) -> int:
    state = get_state_command(ctx, entity_id)

    # Convert from 0-255 -> 0-100.
    brightness = state["attributes"]["brightness"]
    if brightness:
        return floor(brightness / 2.55)
    else:
        # Light is off.
        return 0


def light_control_group(entity_id: str) -> click.Group:
    @click.group(
        "lights", cls=DefaultGroup, default_if_no_args=True, help="light control"
    )
    def control() -> None:
        pass

    @control.command(
        "set",
        default=True,
        help="set brightness level (0-100)",
        epilog=f"sets brightness value of {entity_id}",
    )
    @click.argument("level", nargs=1, type=int, required=False)
    @pass_context
    def control_set(ctx: Context, level: int) -> None:
        if level:
            if level < 0 or level > 100:
                click.secho("level must be between 0-100", fg="red")
                raise click.exceptions.Exit(1)

            set_brightness_command(ctx, entity_id, level)
        else:
            # Just toggle the lights.
            toggle_command(ctx, entity_id)

    @control.command(
        "level",
        help="get brightness level (0-100)",
        epilog=f"get brightness value of {entity_id}",
    )
    @pass_context
    def control_level(ctx: Context) -> None:
        click.secho(get_level(ctx, entity_id))

    @control.command(
        "toggle", help="toggle state", epilog=f"toggles state of {entity_id}"
    )
    @pass_context
    def control_toggle(ctx: Context) -> None:
        toggle_command(ctx, entity_id)

    @control.command("state", help="get state", epilog=f"gets state of {entity_id}")
    @pass_context
    def control_get(ctx: Context) -> None:
        click.secho(get_state(ctx, entity_id))

    @control.command("on", help="turn on", epilog=f"turn on {entity_id}")
    @pass_context
    def control_on(ctx: Context) -> None:
        on_command(ctx, entity_id)

    @control.command("off", help="turn off", epilog=f"turn off {entity_id}")
    @pass_context
    def control_off(ctx: Context) -> None:
        off_command(ctx, entity_id)

    return control

```

Then just define each light related command using the shared functionality:

```python
@tome.group("kitchen", short_help="kitchen")
def kitchen() -> None:
    pass


kitchen.add_command(light_control_group("light.kitchen_lights"))


@tome.group("living", short_help="kitchen")
def living() -> None:
    pass


living.add_command(light_control_group("light.living_room_lights"))
```

Now `smn kitchen lights` and `smn living lights` share the same inputs and 
functionality. It will either toggle the light state if no level is provided, or 
set the light level to a value provided from 0-100: `smn kitchen lights 50`

## Longform Command Help

To provide longform command help, a docstring can be provided:

```python
@sapling.command("pull-rebase", help="Pull repo and rebase current commit to latest")
@pass_context
def pull_rebase(ctx: Context) -> None:
    """Pull repo and rebase current commit to latest

    This will pull the latest remote repository information using the sapling CLI
    and then attempt to rebase the current working copy against remote/main.
    """

```

The first line, `Pull repo and rebase current commit to latest` will become the 
command short help, while the rest will be shown when the command is run with 
`--smn-help`. This can also be set via `help` during `@click.command` decoration, 
but this will override any docstring that is present.

Alternatively, there is also the `epilog` argument to `@click.command`, which will 
print the provided string after all of the click generated help text is provided. 
This can be useful as an alternative for providing a standard set of command help, 
as shown in the standardizing example above.

## Root Tome Module

The `--tome`/`SMN_TOME` option to the CLI can also be a path to a module that is
in the Python classpath already. This is useful for build systems like
[buck](https://github.com/facebook/buck2) which use an isolated classpath:

```
python_binary(
    name = "cli",
    # Equivalent to smn --tome path.to.root.tome
    main_function = "smn.cli.smn",
    runtime_env = {
        "SMN_TOME": "path.to.root.tome"
    },
    ...
)
```

## Command Caching

The results of command runs can optionally be cached with the
[`bkt`](https://github.com/dimo414/bkt) CLI utility. There are three args to
the Summoner Context's `run` methods which control this:

* `cache_ttl` - TTL in seconds to cache the command result.
* `cache_stale` - An optional time in seconds, lower than the ttl. If the same
  command is invoked between `cache_stale` and `cache_ttl`, `bkt` will cache
  the result in the background, avoiding a run in the foreground after the ttl
  expires.
* `cache_force` - If True, this will force a run and re-cache of the command,
    regardless of ttl/stale settings.

Additionally, there are the `--cache-force` and `--cache-disable` options, which
will globally modify caching behavior within `smn`, regardless of any code level
configurations.

# Development

All development on smn can be handled through the `uv` tool:

```bash
uv sync
Resolved 34 packages in 0.38ms
Audited 33 packages in 0.06ms
```

Invocations of `uv` will read configuration from the [pyproject.toml](pyproject.toml)
file and configure a virtual environment with `smn` and it's dependencies under
`.venv` in the repository.

## Type Checking

Ensure no type errors are present with [pyre](https://github.com/facebook/pyre-check):

```bash
uv run pyre check
ƛ No type errors found
```

**Note**: Pyre daemonizes itself on first run for faster subsequent executions. Be
sure to shut it down with `pyre kill` when finished.

## Formatting

Format code with the [ruff](https://github.com/astral-sh/ruff) formatter:

```bash
uv run ruff format
8 files left unchanged
```

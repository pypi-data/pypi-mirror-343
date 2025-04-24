#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.10"
# ///

import subprocess
import sys


def get_release_notes(version):
    with open("CHANGELOG.md", "r") as f:
        content = f.read()

    sections = content.split("\n## ")
    # First section won't start with ## since it's split on that
    sections = ["## " + s if i > 0 else s for i, s in enumerate(sections)]

    for section in sections:
        if section.startswith(f"## {version}"):
            install_instructions = f"""## Installation

You can install krayt using one of these methods:

## pypi

``` bash
pip install krayt
```

### Using i.jpillora.com (recommended)

``` bash
curl https://i.jpillora.com/waylonwalker/krayt | bash
```

### Direct install script

``` bash
curl -fsSL https://github.com/waylonwalker/krayt/releases/download/v{version}/install.sh | bash
```

### Manual download
You can also manually download the archive for your platform from the releases page:
- [x86_64-unknown-linux-gnu](https://github.com/waylonwalker/krayt/releases/download/v{version}/krayt-{version}-x86_64-unknown-linux-gnu)
- [aarch64-unknown-linux-gnu](https://github.com/waylonwalker/krayt/releases/download/v{version}/krayt-{version}-aarch64-unknown-linux-gnu)"""

            # Get help output for main command and all subcommands
            try:
                help_outputs = []

                # Get main help output
                main_help = subprocess.check_output(
                    ["krayt", "--help"],
                    stderr=subprocess.STDOUT,
                    universal_newlines=True,
                )
                help_outputs.append(("Main Command", main_help))

                # Get help for each subcommand
                subcommands = [
                    "create",
                    "exec",
                    "clean",
                    "version",
                    "pod",
                ]
                for cmd in subcommands:
                    cmd_help = subprocess.check_output(
                        ["krayt", cmd, "--help"],
                        stderr=subprocess.STDOUT,
                        universal_newlines=True,
                    )
                    help_outputs.append((f"Subcommand: {cmd}", cmd_help))

                # Format all help outputs
                help_text = "\n\n".join(
                    f"### {title}\n\n``` bash\n{output}```"
                    for title, output in help_outputs
                )

                return f"{section.strip()}\n\n{install_instructions.format(version=version)}\n\n## Command Line Usage\n\n{help_text}"
            except subprocess.CalledProcessError as e:
                return f"{section.strip()}\n\n{install_instructions.format(version=version)}\n\n## Command Line Usage\n\nError getting help: {e.output}"

    return None


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: get_release_notes.py VERSION", file=sys.stderr)
        sys.exit(1)

    version = sys.argv[1]
    notes = get_release_notes(version)
    if notes:
        print(notes)
    else:
        print(f"Error: No release notes found for version {version}", file=sys.stderr)
        sys.exit(1)

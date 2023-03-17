import os
import click
import pandas as pd


def path() -> str:
    parent_dir_path = r"D:\ra_cli"
    dir_name = "ra"
    path = os.path.join(parent_dir_path, dir_name)
    return path


def initialize() -> None:
    os.makedirs(path(), exist_ok=True)


@click.group()
def ra_cli() -> None:
    pass


@ra_cli.command(name="list_all_csv")
def list_all_csv() -> None:
    click.echo("list_all_csv")
    for root, dirs, files in os.walk(path()):
        print(f"root: {root} dirs: {dirs} files: {files} ")


def main_cli():
    initialize()
    ra_cli()

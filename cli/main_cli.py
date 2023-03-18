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
    click.echo("CMD: list_all_csv")
    csv_files = []
    for root, dirs, files in os.walk(path()):
        for index, val in enumerate(files):
            if files[index].rsplit(".", 1)[1] == "csv":
                csv_files.append(files[index])
        print(f"root: {root} dirs: {dirs} files: {files} ")

    csv_files = tuple(csv_files)
    print(csv_files)


def main_cli():
    initialize()
    ra_cli()

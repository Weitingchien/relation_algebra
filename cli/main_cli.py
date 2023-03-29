import os
import click
import pandas as pd
from click_shell import shell

from unary_operators.select import Select
from unary_operators.rename import Rename
from binary_operators.set_union import Union
from binary_operators.set_difference import Difference
from binary_operators.cartesian_product import Cartesian



class catch_Exceptions(click.Group):
    def __call__(self, *args, **kwds):
        try:
            return self.main(*args, **kwds)
        except Exception as exc:
            click.echo(exc)


def path() -> str:
    parent_dir_path = r"D:\ra_cli"
    dir_name = "ra"
    path = os.path.join(parent_dir_path, dir_name)
    return path


def initialize() -> None:
    os.makedirs(path(), exist_ok=True)

@shell(prompt="ra-cli > ",context_settings=dict(help_option_names=["-h", "--help"]), intro="Starting my CLI......")
def ra_cli() -> None:
    pass


@ra_cli.command(name="list_all_csv")
def list_all_csv() -> tuple:
    csv_files = []
    for root, dirs, files in os.walk(path()):
        for index, val in enumerate(files):
            if files[index].rsplit(".", 1)[1] == "csv":
                csv_files.append(files[index])
        print(f"root: {root} dirs: {dirs} files: {files} ")

    csv_files = tuple(csv_files)
    click.echo(csv_files)
    return csv_files


@ra_cli.command(name='select')
@click.argument("columns_and_tablename", nargs=-1, type=str)  # nargs=-1 支援不定參數
@click.pass_context
def select_columns_from_table(ctx, columns_and_tablename) -> None:
    columns_and_tablename = list(columns_and_tablename)
    print(f"columns_and_tablename: {columns_and_tablename}")

    # 關鍵字轉小寫
    for index, val in enumerate(columns_and_tablename):
        if val in ['TABLE', 'COLUMN', 'TO', 'FROM', 'WHERE', 'UNION', 'EXCEPT', 'CROSS', 'JOIN']:
            columns_and_tablename[index] = val.lower()

    select = Select(columns_and_tablename, path, ctx.invoke(list_all_csv))
    
    """
    if len(select.show()) <= 0:
        raise Exception("SQL error")
    """
    if 'union' in columns_and_tablename:
        print('set_union')
        union = Union(columns_and_tablename, path, ctx.invoke(list_all_csv))
        click.echo(union.data())
        return
    elif 'except' in columns_and_tablename:
        print('set_difference')
        difference = Difference(columns_and_tablename, path, ctx.invoke(list_all_csv))
        click.echo(difference.data())
        return  
    elif 'cross' in columns_and_tablename:
        print('cross_join')
        cartesian = Cartesian(columns_and_tablename, path, ctx.invoke(list_all_csv))
        click.echo(cartesian.data())
        return

    result = select.data()
    if(isinstance(result, pd.DataFrame)):
        click.echo(result)

@ra_cli.command(name='alter')
@click.argument('columns_and_tablename', nargs=-1, type=str)
@click.pass_context
def alter_table_rename_columns(ctx, columns_and_tablename) -> None:
    rename = Rename(columns_and_tablename, path, ctx.invoke(list_all_csv))
    rename.alter_table()
    



@ra_cli.command(name="clear")
def clear() -> None:
    click.clear()


@ra_cli.command(name="exit", context_settings=dict(token_normalize_func=lambda x: x.lower()))
def stop() -> None:
    os._exit(0)


def main_cli() -> None:
    initialize()
    ra_cli()

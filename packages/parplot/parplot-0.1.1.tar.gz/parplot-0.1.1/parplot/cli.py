from __future__ import annotations as _annotations

import argparse
import sys
import webbrowser
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Literal

import polars
from altair import Chart, X, Y

from . import __version__


def main():
    try:
        args = parse_args()
        input_file = find_input_file(args.input_path)
        print('Loaded', input_file)
        df = load_df(input_file)
        polars.Config.set_tbl_hide_dataframe_shape(True)
        print('Summary:')
        print(df.describe())
        polars.Config.set_tbl_hide_dataframe_shape(True)
        print('Data:')
        print(df)
        x_series = get_x_series(args, df)
        y_data = get_y_data(args, df, x_series.name)
        mode = infer_mode(args, x_series, y_data)
        print(f'Creating {mode} chart')
        chart = create_chart(args, input_file, df, x_series, y_data, mode)

        if args.output_file:
            output_path = Path(args.output_file)
        else:
            output_path = input_file.with_suffix(f'.{args.output_format}').resolve()

        chart.save(output_path, scale_factor=4.0)  # type: ignore
        try:
            pretty_output_path = f'./{output_path.relative_to(Path.cwd(), walk_up=True)}'
        except ValueError:
            pretty_output_path = str(output_path)
        print(f'Chart written to {pretty_output_path}')

        if args.open:
            webbrowser.open(f'file://{output_path}')

    except RuntimeError as e:
        print(f'Error: {e}', file=sys.stderr)
        exit(1)


class Mode(StrEnum):
    LINE = 'line'
    SCATTER = 'scatter'
    BAR = 'bar'


@dataclass
class Args:
    mode: Mode | None
    x_column: str | None
    y_column: list[str]
    dimension: str | None
    output_format: Literal['html', 'svg', 'png', 'jpeg']
    title: str | None
    x_title: str | None
    y_title: str | None
    width: int
    height: int
    input_path: str | None
    output_file: str | None
    open: bool


def parse_args() -> Args:
    parser = argparse.ArgumentParser(
        prog='parplot',
        description=f"""\
Plot data from a parquet, CSV or JSON file.

Version: {__version__}
""",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    # Options
    parser.add_argument('--mode', '-m', help='Plot mode, default is auto', type=Mode, choices=Mode)
    parser.add_argument('-x', help='X axis column name')
    parser.add_argument('-y', help='Y axis column name(s)', action='append')
    parser.add_argument('--dimension', '-d', help='Dimension column name')
    parser.add_argument(
        '--format', '-f', help='Output format, defaults to html', default='html', choices=['html', 'svg', 'png']
    )
    parser.add_argument('--title', help='Chart title')
    parser.add_argument('--x-title', help='X axis title')
    parser.add_argument('--y-title', help='Y axis title')
    parser.add_argument('--width', type=int, help='Plot width, default is 800', default=800)
    parser.add_argument('--height', type=int, help='Plot height, default is 600', default=600)
    parser.add_argument('--no-open', action='store_true', help='Do not open the file')

    # Positional arguments
    parser.add_argument(
        'input_path',
        nargs='?',
        help='Input path, should be a parquet, CSV or JSON file, or a directory containing such files, defaults to CWD',
    )
    parser.add_argument('output_file', nargs='?', help='Output file path')
    parser.add_argument(
        '--version', '-V', action='version', help='Show version and exit', version=f'%(prog)s v{__version__}'
    )

    args = parser.parse_args()

    return Args(
        x_column=args.x,
        y_column=args.y,
        dimension=args.dimension,
        mode=args.mode,
        output_format=args.format,
        title=args.title,
        x_title=args.x_title,
        y_title=args.y_title,
        width=args.width,
        height=args.height,
        input_path=args.input_path,
        output_file=args.output_file,
        open=not args.no_open,
    )


def find_input_file(input_file_arg: str | None) -> Path:
    if input_file_arg is not None:
        path = Path(input_file_arg)
        if not path.exists():
            raise RuntimeError(f'Input file not found: {path}')
        elif path.is_file():
            return path
    else:
        path = Path.cwd()

    if parquet_file := _get_latest_file(path, '*.parquet'):
        return parquet_file
    elif csv_file := _get_latest_file(path, '*.csv'):
        return csv_file
    elif json_file := _get_latest_file(path, '*.json'):
        return json_file
    else:
        raise RuntimeError('No input file found, looked for parquet, csv, or json files in the current directory')


def _get_latest_file(dir_path: Path, glob: str) -> Path | None:
    match_files = list(dir_path.glob(glob))
    if match_files:
        return max(match_files, key=lambda f: f.stat().st_mtime)
    else:
        return None


def load_df(file_path: Path) -> polars.DataFrame:
    if file_path.suffix == '.parquet':
        return polars.read_parquet(file_path)
    elif file_path.suffix == '.csv':
        return polars.read_csv(file_path, try_parse_dates=True)
    elif file_path.suffix == '.json':
        return polars.read_json(file_path)
    else:
        raise RuntimeError(f'Unsupported file type: {file_path}, must be parquet, csv, or json')


def get_x_series(args: Args, df: polars.DataFrame) -> polars.Series:
    if args.x_column:
        return df[args.x_column]
    elif 'x' in df.columns:
        return df['x']
    else:
        return df[df.columns[0]]


@dataclass
class YColumns:
    columns: list[str]


@dataclass
class YDimensions:
    column: str
    dim: str


YData = YColumns | YDimensions


def get_y_data(args: Args, df: polars.DataFrame, x_col: str) -> YData:
    columns: list[str] = []
    for col in df.columns:
        # don't add x column or dimension column to y data
        if col != x_col and col != args.dimension:
            series = df[col]
            # include if it's not a string column
            if series.dtype not in (polars.datatypes.Categorical, polars.datatypes.String):
                columns.append(col)

    if not columns:
        raise RuntimeError('No y columns found')

    if args.dimension:
        if len(columns) != 1:
            raise RuntimeError('Only one Y column can be used with dimension')
        return YDimensions(columns[0], args.dimension)
    else:
        return YColumns(columns)


def infer_mode(args: Args, x_series: polars.Series, y_data: YData) -> Mode:
    if args.mode:
        return args.mode
    elif x_series.dtype in (
        polars.datatypes.Date,
        polars.datatypes.Datetime,
        polars.datatypes.Float64,
        polars.datatypes.Int64,
    ):
        return Mode.LINE
    elif x_series.dtype in (polars.datatypes.Categorical, polars.datatypes.String):
        return Mode.BAR
    else:
        raise RuntimeError('Unable to infer mode')


def create_chart(
    args: Args, input_file: Path, df: polars.DataFrame, x_series: polars.Series, y_data: YData, mode: Mode
) -> Chart:
    x = X(x_series.name)
    if isinstance(y_data, YColumns):
        color = 'Dimension'
        df = df.unpivot(index=x_series.name, variable_name=color)
        y = Y(shorthand='value')
    else:
        y = Y(shorthand=y_data.column)
        color = y_data.dim

    if y_title := args.y_title:
        y = y.title(y_title)
    if x_title := args.x_title:
        x = x.title(x_title)

    chart = Chart(df)
    if mode == Mode.LINE:
        chart = chart.mark_line(tooltip=True)  # type: ignore
    elif mode == Mode.SCATTER:
        chart = chart.mark_point(tooltip=True)  # type: ignore
    else:
        assert mode == Mode.BAR, f'Invalid mode: {mode}'
        chart = chart.mark_bar(tooltip=True)  # type: ignore

    chart = chart.encode(x=x, y=y, color=color)

    if width := args.width:
        chart = chart.properties(width=width)
    if height := args.height:
        chart = chart.properties(height=height)
    return chart.properties(title=args.title or input_file.name).interactive()

import click
from . import get_publication, get_journal
from .utils import json_str, json_str_pretty

from . import __version__, EMAIL

HEADERS = {
    "User-Agent": "oampy-cli {0} <{1}>".format(__version__, EMAIL)}


def json_output(raw, pretty):
    if pretty:
        return json_str_pretty(raw)
    else:
        return json_str(raw)


def print_json(raw, pretty):
    if raw is not None:
        print(json_output(raw, pretty))


def print_result(result, pretty):
    if result is not None:
        print_json(result.raw, pretty)


@click.group()
def main():
    """
    Fetch metadata from the Open Access Monitor (OAM)
    """
    pass


def main_options(function):
    """
    Reuse decorators for multiple commands
    https://stackoverflow.com/a/50061489
    """
    function = click.option("-p", "--pretty", is_flag=True,
                            help="Pretty print output")(function)
    return function


@main.command()
@main_options
@click.argument('doi')
def publication(doi, pretty):
    """Fetch metadata of publication given by DOI"""
    p = get_publication(doi, headers=HEADERS)
    print_result(p, pretty)


@main.command()
@main_options
@click.argument('issn')
def journal(issn, pretty):
    """Fetch metadata of journal given by ISSN"""
    j = get_journal(issn, headers=HEADERS)
    print_result(j, pretty)


if __name__ == '__main__':
    main()

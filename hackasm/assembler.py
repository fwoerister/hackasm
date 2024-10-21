import sys
import click

from hackasm.parser import Parser


@click.command()
@click.argument('source', type=click.Path(exists=True, readable=True))
def translate_source(source):
    if not sys.argv[1].endswith(".asm"):
        raise Exception("Source file must end with .asm")

    translate_source(sys.argv[1])

    hack_parser = Parser(f'{source[:-4]}.asm')

    with open(f'{source[:-4]}.hack', 'w') as out:
        for instruction in hack_parser.get_parsed_instructions():
            out.write(f'{instruction.to_machine_code()}\n')


if __name__ == '__main__':
    translate_source()

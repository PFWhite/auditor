docstr = """
Auditor

Usage: auditor (<program_path>)
auditor migrate ( <old_config> <new_program> )

Options:
  -h --help                                     show this message and exit


Auditor is used to run auditor program files to alter csv files
"""
from docopt import docopt

from auditor.compiler import AuditorCompiler
from auditor.interpreter import Interpreter
from auditor.old_config_parser import ConfigParser

def main(args=docopt(docstr)):
    if not args.get('migrate'):
        program_path = args['<program_path>']
        compiler = AuditorCompiler()
        instructions = compiler(program_path)
        interpreter = Interpreter(instructions)
        interpreter()
    else:
        parser = ConfigParser(args.get('<old_config>'))
        parser.write(args.get('<new_program>'))


if __name__ == '__main__':
    args = docopt(docstr)
    main(args)
    exit()

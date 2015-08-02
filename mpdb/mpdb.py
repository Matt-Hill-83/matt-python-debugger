PRODUCTION = False

'''

To Install:
easy_install prettytable

To use:
    from .mpdb.mpdb import *
    from .mpdb.zpdb import *
then:
    Mpdb.run(locals())
        OR
    set_trace(locals())

then: set this in all 3 files:
PRODUCTION = True



Questions:
- How do I create an alias for Mpdb.run(locals()) that includes the parameter?
- How do I trigger ipdb to execute with the correct scope?
- How to I get locals() from pdb so that I can use the next function and run mpdb on the new locals?



To Do:
- Add numbers to column object
- create a dict of column codes
- create a column object for every column
- slice each row element based on its column slicing data during row population
- create a dictionary that relates the column object to it's id number
- create a command interpreter that updates column slice data


- Look at isinstance()

- use s[1000 2330] to just show certain rows

- show data for list objects
- group local variables
- only show local variables that aren't already shown

- add ability to hide columns

- figure out how to make PRODUCTION a global

- color ID's
- add double vertical bar for first col
- figure out a universal way to determine if something is an object instance

- how to import into a django project?
- monkey patch pdb?



- figure out out how to make a pip package

- add more color
- add col slicer
- figure out how to make row width work

- center headers on rows automatically
- Pretty Table colors


'''

import ipdb
import os
import re

if PRODUCTION:
    from .print_managers import *
    # from .zpdb import *
else:
    from print_managers import *
    # from zpdb import *

class Mpdb():
    @classmethod
    def initialize(cls, local_vars):
        cls.keyboard_input = '0'
        ### ??? What is a better way to share this data across instances of
        # the child classes?
        PrintManager.codes_dict = CodesDict()
        PrintManager.local_vars = local_vars

    @classmethod
    def convert_to_int(cls, num):
        if num:
            return int(num)

    @classmethod
    def convert_input_to_dict(cls, keyboard_input):
        ki_str = keyboard_input
        search_str2 = \
            r'(?P<code>\d+)(?P<space>\s*)(?P<start>\d*)(?P<colon>:*)(?P<end>\d*)'
        match = re.search(search_str2, ki_str)
        m ={}
        m['inputs_received'] = False
        if match:
            [print(x) for x in match.groups()]
            m = match.groupdict()

            space = m['space']
            colon = m['colon']

            m['code'] = cls.convert_to_int((m['code']))
            m['start'] = cls.convert_to_int((m['start']))
            m['end'] = cls.convert_to_int((m['end']))
            m['inputs_received'] = True

        return m

    @classmethod
    def create_printers(cls):
        cls.printers = [PrintManagerForLocalVars(),
                    PrintManagerForObjects(),
                    PrintManagerForListsOfObjects()
                    ]

        [p.create_table_data() for p in cls.printers]

    @classmethod
    def display_output(cls):
        os.system('clear')
        for printer in cls.printers:
            printer.print_section_header()
            printer.print_tables()
        print('')
        print('')

    @classmethod
    def get_user_input(cls):
        u_input = cls.keyboard_input
        codes_dict = PrintManager.codes_dict

        while u_input != 'q':
            inputs = cls.convert_input_to_dict(u_input)
            if inputs['inputs_received']:
                code = inputs['code']
                if code in codes_dict.codes:
                    target_object = codes_dict.codes[code][0]
                    target_object.visible = not target_object.visible

            cls.display_output()

            u_input = input('mpdb(q to quit)>>')

    @classmethod
    def run(cls, local_vars):
        cls.initialize(local_vars)
        cls.create_printers()
        cls.get_user_input()



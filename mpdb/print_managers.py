PRODUCTION = False

if PRODUCTION:
    from .colors import *
else:
    from colors import *
import re
import os
import prettytable as pt
import ipdb

# General PrintManager class that performs the common printing
# tasks required by each section.

class PrintManager():
    # Variables shared between instances of inherited classes:
    codes_dict = None
    local_vars = None

    def __init__(self):
        self.visible = True
        self.section = Section()
        self.filtered_var_names = []
        self.excluded_parameters = ['date_updated',
                               'modified_by_id',
                               'tail',
                               'owned_by_organization_id',
                               'created_by_id',
                               'date_created',
                               'owned_by_user_id',
                               '_owned_by_organization_cache',
                               '_modified_by_cache',
                               '_owned_by_user_cache',
                               '_created_by_cache',
                               ]

    ########## Create data architecture

    def add_section_code_to_codes_dict(self, objekt):
        self.codes_dict.codes[objekt.section.id] = [objekt.section, True]

    def create_table_objects(self):
        for item in self.filtered_var_names:
            self.create_object_for_item_of_the_correct_type(item)

    def create_table_data(self):
        self.add_section_code_to_codes_dict(self)
        self.filter_var_names()
        self.table_count = 1
        self.create_table_objects()

    def is_instance(self, item):
        if PRODUCTION:
            search_str = "<class 'webapp.apps."
            start_pos = 0
        else:
            search_str = '__main__.'
            start_pos = 8

        # return isinstance(item)

        return (str(type(item))[start_pos:start_pos + len(search_str)]) == search_str

    def is_list_of_instances(self, item):
        return isinstance(item, list) and len(item) > 0 and self.is_instance(item[0])

    def cprint(self, str, color='YELLOW'):
        if color == 'YELLOW':
            print(bcolors.YELLOW + (str) + bcolors.ENDC)
        if color == 'FAIL':
            print(bcolors.FAIL + (str) + bcolors.ENDC)

    def filter_var_names(self):
        excluded_var_names = ['self']
        var_names = self.local_vars.keys()
        self.filtered_var_names = [item for item in var_names if item not in excluded_var_names]

    def create_row_object(self, table, item_name, item, row_count):
        row = Row()
        row.id = table.id + row_count
        row.item = item
        row.item_name = item_name
        table.rows.append(row)
        self.codes_dict.codes[row.id] = [row, True]

    def create_table_object(self, objekt_name, objekt, count):
        table = Table()
        table.objekt = objekt
        table.objekt_name = objekt_name
        table.class_name = table.objekt.__class__.__name__
        table.id = count * table.table_count_increment + int(self.section.id)

        self.codes_dict.codes[table.id] = [table, True]
        return table

    def filter_column_headers(self, keys):
        filtered_col_headers = [item for item in keys if item not in self.excluded_parameters]
        filtered_col_headers.sort()
        return filtered_col_headers

    def create_column_headers(self, table):
        col_headers = []
        [col_headers.append(col_hdr) for col_hdr in table.rows[0].item.__dict__.keys()]
        table.column_headers = col_headers

    def add_slicer_to_col_headers(self, table):
        col_headers = table.printable_column_headers
        headers = []

        for i in range(len(col_headers)):
            col = table.columns[i]
            start = col.slicer_start
            stop = col.get_slicer_stop()
            column_code = str(table.columns[i].id)
            column_header = col_headers[i]

            headers.append('[%s] %s  [%s:%s]' %(column_code, column_header, str(start), str(stop)))
        return headers

    def add_id_column_to_header_if_multiple_rows_present(self, table):
        if table.print_id_column:
            table.printable_column_headers = ['ID'] + table.column_headers
        else:
            table.printable_column_headers = table.column_headers

    def create_column_object_for_each_column_in_table(self, table):
        col_num = 0
        num_col = len(table.printable_column_headers)
        for col in range(num_col):
            new_col = Column()
            new_col.id = col_num
            table.columns.append(new_col)
            PrintManager.codes_dict.column_codes[col_num] = new_col

    ########## Create PrettyTable objects

    def init_pretty_table(self, table, col_width=20):

        col_headers = self.add_slicer_to_col_headers(table)
        pretty_table = pt.PrettyTable(col_headers)
        pretty_table.matable_width = col_width
        # pretty_table.max_width = col_width # not yet tested
        pretty_table.padding_width = 1 # this is the default
        # pretty_table.hrules=pt.ALL
        # pretty_table.align["City name"] = "l" # Left align city names

        return pretty_table

    def add_row_to_pretty_table(self, pretty_table, row_object, table):
        if row_object.visible:

            row_elements = []
            col_headers = table.column_headers

            for i in range(len(col_headers)):
                attribute = col_headers[i]
                col = table.columns[i]
                start = col.slicer_start
                stop = col.get_slicer_stop()

                attr_value = getattr(row_object.item, attribute)
                attr_value = str(attr_value)[start:stop]

                row_elements.append(attr_value)

            # Only add ID column if table has more than one row.
            if table.print_id_column:
                row_elements = [row_object.id] + row_elements

            pretty_table.add_row(row_elements)

    ########## Print Output

    def print_section_header(self):
        print("")
        self.cprint('[' + str(self.section.id) + ']' + self.section_header, 'YELLOW')

    def print_table_header(self, table):
        table_header = (table.header) %(str(table.id), table.objekt_name, table.class_name)
        self.cprint(table_header, 'FAIL')

    def print_tables(self):
        if self.section.visible:
            for table in self.section.tables:
                table.print_id_column = len(table.rows) > 1
                self.print_table_header(table)
                self.create_column_headers(table)
                self.add_id_column_to_header_if_multiple_rows_present(table)
                self.create_column_object_for_each_column_in_table(table)
                pretty_table = self.init_pretty_table(table)

                for row in table.rows:
                    self.add_row_to_pretty_table(pretty_table, row, table)

                if table.visible:
                    print(pretty_table)

# Specialized PrintManager subclasses that can be modified to suit the
# particular printing needs of each section

class PrintManagerForLocalVars(PrintManager):
    def __init__(self):
        self.__class__.__bases__[0].__init__(self)
        self.section.id = 1000
        self.section_header = \
                '-------------------- Local Variables: ---------------------------'

    def add_row_to_pretty_table(self, pretty_table, row_object, table):
        row_elements = []
        r = row_object
        value = str(r.item)[:30]
        row_elements = [r.item_name, str(value), str(type(r.item))]

        # Only add ID column if table has more than one row.
        if table.print_id_column:
            augmented_row_elements = [row_object.id] + row_elements
        else:
            augmented_row_elements = row_elements

        pretty_table.add_row(augmented_row_elements)

    def print_table_header(self, table):
        # No header required for this table.
        pass

    def create_column_headers(self, table):
        filtered_col_headers = ['name', 'value', 'type']
        table.column_headers = filtered_col_headers

    def create_table_objects(self):
        table = self.create_table_object('', None, self.table_count)
        for item in self.filtered_var_names:
            #Create objects for all items that are not objects and lists of objects
            item_name = item
            item = self.local_vars[item]

            if not self.is_instance(item) and not self.is_list_of_instances(item):
                row_count = table.row_count_increment
                self.create_row_object(table, item_name, item, row_count)
                self.table_count += 1

        self.section.tables.append(table)

class PrintManagerForObjects(PrintManager):
    def __init__(self):
        self.__class__.__bases__[0].__init__(self)
        self.section.id = 2000
        self.section_header = \
            '-------------------- Objects: -----------------------------------'

    def create_object_for_item_of_the_correct_type(self, item):
        #Create table object for all items that are objects
        item_name = item
        item = self.local_vars[item]

        if self.is_instance(item):
            table = self.create_table_object(item_name, item, self.table_count)
            row_count = table.row_count_increment
            self.create_row_object(table, item_name, item, row_count)
            self.section.tables.append(table)

            self.table_count += 1

class PrintManagerForListsOfObjects(PrintManager):
    def __init__(self):
        self.__class__.__bases__[0].__init__(self)
        self.section.id = 3000
        self.visible = True
        self.section_header = \
            '-------------------- Lists of Objects: --------------------------'

    def create_object_for_item_of_the_correct_type(self, item):
        item_name = item
        item = self.local_vars[item]

        #Create table object for all items that are lists of objects
        if self.is_list_of_instances(item):
            table = self.create_table_object(item_name, item, self.table_count)

            row_count = table.row_count_increment
            for objekt in item:
                self.create_row_object(table, objekt.name, objekt, row_count)
                row_count += table.row_count_increment
            self.section.tables.append(table)

            self.table_count += 1

# Classes to encode the architecture of the objects to be printed

class Section():
    def __init__(self):
        self.id = 0
        self.visible = True
        self.tables = []

class Table():
    def __init__(self):
        self.id = 0
        self.visible = True
        self.rows = []
        self.columns = []
        self.header = '[%s] %s [%s]'
        self.objekt = None
        self.objekt_name = ''
        self.class_name = ''
        self.table_count_increment = 100
        self.row_count_increment = 10
        self.column_headers = []
        self.printable_column_headers = [] # These include the object variables plus the 'ID' column.
        self.print_id_column = False
        self.table_count = 0

class Row():
    def __init__(self):
        self.id = None
        self.visible = True
        self.objekt = None

class Column():
    def __init__(self):
        self.id = None
        self.slicer_start = 0
        self.slicer_stop = 5

    def get_slicer_stop(self):
        if self.slicer_stop == None:
            self.slicer_stop = 0
        return self.slicer_stop

# Dictionary to associate each data object with a particular code that the
# user can use to reference the data object through the UI

class CodesDict():
    def __init__(self):
        self.codes = {}
        self.column_codes = {}

    def get_highest_column_id(self):
        return max(self.column_codes.keys())
import json
import re
import yaml
import dateutil.parser as date_parser

class Mappings(object):

    def __init__(self, config, **kwargs):
        self.bad_data = config['error_strings']['bad_data']
        self.empty_cell = config['error_strings']['empty_cell']
        self.blacklisted = config['error_strings']['blacklisted']
        self.not_whitelisted = config['error_strings']['not_whitelisted']
        self.no_regex_match = config['error_strings']['no_regex_match']
        self.empty_okay_string = config['control_strings']['empty_okay']

        self.verbose = kwargs.get('verbose')

        self.whitelists = {}
        for item in config['whitelist']:
            with open(item['vals_file_path']) as values_file:
                self.whitelists[item['header_name']] = self.parse(values_file)

        self.blacklists = {}
        for item in config['blacklist']:
            with open(item['vals_file_path']) as values_file:
                self.blacklists[item['header_name']] = self.parse(values_file)

        self.regexs = {}
        for item in config['regexs']:
            with open(item['vals_file_path']) as values_file:
                self.regexs[item['header_name']] = self.parse(values_file)

    def handler(self, **kwargs):
        the_map = kwargs['map']
        if type(the_map) != type('string'):
            the_map = the_map['func']
        return getattr(self, the_map)(**kwargs)

    def format_date(self, **kwargs):
        item = kwargs.get('item')
        try:
            if item == '':
                return self.empty_cell
            else:
                return date_parser.parse(item).strftime('%Y-%m-%d')
        except Exception as ex:
            if self.verbose:
                print('format_date exception')
                print(ex)
            return self.bad_data

    def is_whitelist(self, **kwargs):
        item = kwargs.get('item')
        header = kwargs.get('header')
        try:
            if item == '':
                return self.empty_cell
            else:
                return item if item in self.whitelists.get(header) else self.not_whitelisted
        except Exception as ex:
            if self.verbose:
                print('is_whitelist exception')
                print(ex)
            return self.bad_data

    def is_blacklist(self, **kwargs):
        item = kwargs.get('item')
        header = kwargs.get('header')
        try:
            if item == '':
                return self.empty_cell
            else:
                return self.blacklisted if item in self.blacklists.get(header) else item
        except Exception as ex:
            if self.verbose:
                print('is_blacklist exception')
                print(ex)
            return self.bad_data

    def regex(self, **kwargs):
        item = kwargs.get('item')
        header = kwargs.get('header')
        try:
            if item == '':
                return self.empty_cell
            else:
                regexs = self.regexs.get(header)
                for regex in regexs:
                    pattern = re.compile(regex['pattern'])
                    match = pattern.match(item)
                    if match:
                        try:
                            return match.group(1)
                        except Exception as ex:
                            if self.verbose:
                                print('deep regex exception')
                                print(ex)
                                return regex.get('value')
                # no match found
                return self.no_regex_match
        except Exception as ex:
            if self.verbose:
                print('regex exception')
                print(ex)
            return self.bad_data

    def empty_okay(self, **kwargs):
        item = kwargs.get('item')
        if item == '' or item == None:
            return self.empty_okay_string
        else:
            return item

    def __arg_map_base(self, callable_item, **kwargs):
        """
        Applies the args in the mapping object as *args into
        the callable_item
        """
        headers = kwargs.get('headers')
        row = kwargs.get('row')
        arg_list = kwargs.get('args')
        args = [val, header for val, header in zip(row, headers) if (header in arg_list)]
        args = [val for val, header in sorted(args, key=lambda x: arg_list.index(x[1]))]
        return callable_item(*args)

    def greater_equal(self, **kwargs):
        """
        Tests if the first item is greater equal the second and
        returns it if it is. Else returns self.bad_data
        """
        try:
            func = lambda x, y: x if x >= y else self.bad_data
            return self.__arg_map_base(func, **kwargs)
        except Exception as ex:
            if self.verbose:
                print('greater_equal exception')
                print(ex)
                print('Occurred with kwargs:')
                print(kwargs)
            return self.bad_data

    def space_join(self, **kwargs):
        """
        Joins all the args values with a space character
        """
        try:
            func = lambda *x: ' '.join(x)
            return self.__arg_map_base(func, **kwargs)
        except Exception as ex:
            if self.verbose:
                print('space_join exception')
                print(ex)
                print('Occurred with kwargs:')
                print(kwargs)
            return self.bad_data

    def parse(self, infile):
        text = infile.read()
        try:
            values = yaml.load(text)
        except Exception as ex:
            if self.verbose:
                print(ex)
                print('Value files must be written in yaml.')
        return values if values else []




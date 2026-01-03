####################################################################
#  query.py                                                        #
####################################################################
#                                                                  #
#                      This file is part of:                       #
#                        MOONVEIL PROJECT                          #
#                                                                  #
####################################################################

from pyparsing import (
    alphanums,
    infixNotation,
    oneOf,
    opAssoc,
    ParseException,
    Word
)

class QueryParser:
    def __init__(self):
        self.attribute = Word(alphanums + '_')
        self.value = Word(alphanums + '_.-/')
        self.operator = oneOf(':')
        self.boolean_operator = oneOf('and or', caseless=True)
        self.query_expr = self.define_query_expr()

    def define_query_expr(self):
        return infixNotation(
            self.attribute + self.operator + self.value,
            [
                ('and', 2, opAssoc.LEFT),
                ('or', 2, opAssoc.LEFT),
            ],
        )

    def parse_query(self, query_string):
        try:
            parsed_query = self.query_expr.parseString(
                query_string, parseAll=True)
            if len(parsed_query) == 1:
                return parsed_query[0].asList()
            else:
                return parsed_query.asList()
        except ParseException as error:
            print(f'Error parsing query: {error}')
            return None

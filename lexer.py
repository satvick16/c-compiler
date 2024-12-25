import re
from enum import Enum

class TokenType(Enum):
    identifier = 1
    constant = 2
    int_keyword = 3
    void_keyword = 4
    return_keyword = 5
    open_parenthesis = 6
    close_parenthesis = 7
    open_brace = 8
    close_brace = 9
    semicolon = 10

    tilde = 11
    hyphen = 12
    two_hyphens = 13

class Token:
    def __init__(self, string, token_type):
        self.string = string
        self.token_type = token_type

def tokenize(program_input):
    tokens = []

    while len(program_input) != 0:
        if program_input[0].isspace():
            program_input = program_input.lstrip()
        else:
            matches = {
                TokenType.identifier: re.search(r"[a-zA-Z_]\w*\b", program_input),
                TokenType.constant: re.search(r"[0-9]+\b", program_input),
                TokenType.int_keyword: re.search(r"int\b", program_input),
                TokenType.void_keyword: re.search(r"void\b", program_input),
                TokenType.return_keyword: re.search(r"return\b", program_input),
                TokenType.open_parenthesis: re.search(r"\(", program_input),
                TokenType.close_parenthesis: re.search(r"\)", program_input),
                TokenType.open_brace: re.search(r"{", program_input),
                TokenType.close_brace: re.search(r"}", program_input),
                TokenType.semicolon: re.search(r";", program_input),

                TokenType.tilde: re.search(r"~", program_input),
                TokenType.hyphen: re.search(r"-", program_input),
                TokenType.two_hyphens: re.search(r"--", program_input)
            }

            spans = {}

            for key, value in matches.items():
                # only keep potential matches
                if value is not None:
                    spans[key] = value.span()
            
            if not spans:
                raise Exception('No token match found!')

            lengths = {}

            for key, value in spans.items():
                # only keep matches from the beginning of the input
                if value[0] == 0:
                    lengths[key] = value[1] - value[0]

            if not lengths:
                raise Exception('No token match found!')

            temp = max(lengths.values())
            ttypes = [key for key in lengths if lengths[key] == temp]

            if temp == 0:
                raise Exception('No token match found!')

            if len(ttypes) == 2:
                if TokenType.identifier in ttypes:
                    ttypes.remove(TokenType.identifier)
                else:
                    raise Exception('More than one token match found!')

            ttype = ttypes[0]

            token = Token(matches[ttype].group(), ttype)
            tokens.append(token)

            program_input = program_input[spans[ttype][1]:]
 
    return tokens

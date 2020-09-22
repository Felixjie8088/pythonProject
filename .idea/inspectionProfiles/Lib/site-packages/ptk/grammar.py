# -*- coding: UTF-8 -*-

# (c) Jérôme Laheurte 2015-2019
# See LICENSE.txt

"""
Context-free grammars objects. To define a grammar, inherit the
Grammar class and define a method decorated with 'production' for each
production.
"""

import copy
import functools
import inspect
import logging

from ptk.lexer import EOF, _LexerMeta
from ptk.utils import memoize, Singleton


class Epsilon(metaclass=Singleton):
    """
    Empty production
    """
    __reprval__ = '\u03B5'


class GrammarError(Exception):
    """
    Generic grammar error, like duplicate production.
    """


class GrammarParseError(GrammarError):
    """
    Syntax error in a production specification.
    """


@functools.total_ordering
class Production(object):
    """
    Production object
    """
    def __init__(self, name, callback, priority=None, attributes=None):
        self.name = name
        self.posarg = None
        self.callback = callback
        self.right = list()
        self.attributes = attributes or {}
        self.__priority = priority
        self.__ids = dict() # position => id

    def addSymbol(self, identifier, name=None):
        """
        Append a symbol to the production's right side.
        """
        if name is not None:
            if name in self.__ids.values():
                raise GrammarParseError('Duplicate identifier name "%s"' % name)
            self.__ids[len(self.right)] = name
        self.right.append(identifier)

    def cloned(self):
        prod = Production(self.name, self.callback, self.__priority)
        prod.right = list(self.right)
        prod.__ids = dict(self.__ids) # pylint: disable=W0212
        return prod

    def apply(self, args, position):
        kwargs = dict([(name, args[index]) for index, name in self.__ids.items()])
        if self.posarg is not None:
            kwargs[self.posarg] = position
        return self.callback, kwargs

    def rightmostTerminal(self, grammar):
        """
        Returns the rightmost terminal, or None if there is none
        """
        for symbol in reversed(self.right):
            if symbol in grammar.tokenTypes():
                return symbol

    def precedence(self, grammar):
        """
        Returns the production's priority (specified through the
        'priority' keyword argument to the 'production' decorator), or
        if there is none, the priority for the rightmost terminal.
        """
        if self.__priority is not None:
            return grammar.terminalPrecedence(self.__priority)
        symbol = self.rightmostTerminal(grammar)
        if symbol is not None:
            return grammar.terminalPrecedence(symbol)

    def __eq__(self, other):
        return (self.name, self.right) == (other.name, other.right)

    def __lt__(self, other):
        return (self.name, self.right) < (other.name, other.right)

    def __repr__(self): # pragma: no cover
        return '%s -> %s' % (self.name, ' '.join([repr(p) for p in self.right]) if self.right else repr(Epsilon))

    def __hash__(self):
        return hash((self.name, tuple(self.right)))


# Same remark as in lexer.py.
_PRODREGISTER = list()


class _GrammarMeta(_LexerMeta):
    def __new__(metacls, name, bases, attrs):
        global _PRODREGISTER # pylint: disable=W0603
        try:
            attrs['__productions__'] = list()
            attrs['__precedence__'] = list()
            attrs['__prepared__'] = False
            attrs['__lrstates__'] = list()
            klass = super().__new__(metacls, name, bases, attrs)
            for func, string, priority, attrs in _PRODREGISTER:
                parser = klass._createProductionParser(func.__name__, priority, attrs) # pylint: disable=W0212
                parser.parse(string)
            return klass
        finally:
            _PRODREGISTER = list()


def production(prod, priority=None, **kwargs):
    def _wrap(func):
        if any([func.__name__ == aFunc.__name__ and func != aFunc for aFunc, _, _, _ in _PRODREGISTER]):
            raise TypeError('Duplicate production method name "%s"' % func.__name__)
        _PRODREGISTER.append((func, prod, priority, kwargs))
        return func
    return _wrap


class Grammar(metaclass=_GrammarMeta):
    """
    Base class for a context-free grammar
    """

    __productions__ = list() # Make pylint happy
    __precedence__ = list()
    __prepared__ = False

    startSymbol = None

    def __init__(self):
        # pylint: disable=R0912
        super().__init__()
        if not self.__prepared__:
            self.prepare()

    @classmethod
    def prepare(cls):
        cls.startSymbol = cls._defaultStartSymbol() if cls.startSymbol is None else cls.startSymbol

        productions = set()
        for prod in cls.productions():
            if prod in productions:
                raise GrammarError('Duplicate production "%s"' % prod)
            productions.add(prod)

        cls.__allFirsts__ = cls.__computeFirsts()

        logger = logging.getLogger('Grammar')
        productions = cls.productions()
        maxWidth = max([len(prod.name) for prod in productions])
        for prod in productions:
            logger.debug('%%- %ds -> %%s' % maxWidth, prod.name, ' '.join([repr(name) for name in prod.right]) if prod.right else Epsilon) # pylint: disable=W1201

        cls.__prepared__ = True

    @classmethod
    def __computeFirsts(cls):
        allFirsts = dict([(symbol, set([symbol])) for symbol in cls.tokenTypes() | set([EOF])])
        while True:
            prev = copy.deepcopy(allFirsts)
            for nonterminal in cls.nonterminals():
                for prod in cls.productions():
                    if prod.name == nonterminal:
                        if prod.right:
                            for symbol in prod.right:
                                first = allFirsts.get(symbol, set())
                                allFirsts.setdefault(nonterminal, set()).update(first)
                                if Epsilon not in first:
                                    break
                            else:
                                allFirsts.setdefault(nonterminal, set()).add(Epsilon)
                        else:
                            allFirsts.setdefault(nonterminal, set()).add(Epsilon)
            if prev == allFirsts:
                break
        return allFirsts

    @classmethod
    def _defaultStartSymbol(cls):
        return cls.productions()[0].name

    @classmethod
    def productions(cls):
        """
        Returns all productions
        """
        productions = list()
        for base in inspect.getmro(cls):
            if issubclass(base, Grammar):
                productions.extend(base.__productions__)
        return productions

    @classmethod
    def nonterminals(cls):
        """
        Return all non-terminal symbols
        """
        result = set()
        for prod in cls.productions():
            result.add(prod.name)
            for symbol in prod.right:
                if symbol not in cls.tokenTypes():
                    result.add(symbol)
        return result

    @classmethod
    def precedences(cls):
        precedences = list()
        for base in inspect.getmro(cls):
            if issubclass(base, Grammar):
                precedences.extend(base.__precedence__)
        return precedences

    @classmethod
    def terminalPrecedence(cls, symbol):
        for index, (associativity, terminals) in enumerate(cls.precedences()):
            if symbol in terminals:
                return associativity, index

    @classmethod
    @memoize
    def first(cls, *symbols):
        """
        Returns the first set for a group of symbols
        """
        first = set()
        for symbol in symbols:
            rfirst = cls.__allFirsts__[symbol]
            first |= set([a for a in rfirst if a is not Epsilon])
            if Epsilon not in rfirst:
                break
        else:
            first.add(Epsilon)
        return first

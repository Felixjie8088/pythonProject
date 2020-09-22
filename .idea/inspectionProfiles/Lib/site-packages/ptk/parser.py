# -*- coding: UTF-8 -*-

# (c) Jérôme Laheurte 2015-2019
# See LICENSE.txt

import functools
import collections
import logging
import re

from ptk.lexer import ProgressiveLexer, EOF, token, LexerPosition
from ptk.grammar import Grammar, Production, GrammarError
# production is only imported so that client code doesn't have to import it from grammar
from ptk.grammar import production # pylint: disable=W0611
from ptk.utils import Singleton, callbackByName, memoize


class ParseError(Exception):
    """
    Syntax error when parsing.

    :ivar token: The unexpected token.
    """
    def __init__(self, grammar, tok, state, tokens):
        self.token = tok
        super().__init__('Unexpected token "%s" (%s) in state "%s"' % (tok.value, tok.type, sorted(state)))

        self._state = state
        self._expecting = set()
        for terminal in grammar.tokenTypes():
            if grammar.__actions__.get((state, terminal), None) is not None:
                self._expecting.add(terminal)
        self._tokens = tokens

    def expecting(self):
        """
        Returns a set of tokens types that would have been valid in input.
        """
        return self._expecting

    def state(self):
        """
        Returns the parser state when the error was encountered.
        """
        return self._state

    def lastToken(self):
        """
        Returns the last valid token seen before this error
        """
        return self._tokens[-1]

    def tokens(self):
        """
        Returns all tokens seen
        """
        return self._tokens


def leftAssoc(*operators):
    """
    Class decorator for left associative operators. Use this to
    decorate your :py:class:`Parser` class. Operators passed as
    argument are assumed to have the same priority. The later you
    declare associativity, the higher the priority; so the following
    code

    .. code-block:: python

       @leftAssoc('+', '-')
       @leftAssoc('*', '/')
       class MyParser(LRParser):
           # ...

    declares '+' and '-' to be left associative, with the same
    priority. '*' and '/' are also left associative, with a higher
    priority than '+' and '-'.

    See also the *priority* argument to :py:func:`production`.
    """
    def _wrapper(cls):
        cls.__precedence__.insert(0, ('left', set(operators)))
        return cls
    return _wrapper


def rightAssoc(*operators):
    """
    Class decorator for right associative operators. Same remarks as :py:func:`leftAssoc`.
    """
    def _wrapper(cls):
        cls.__precedence__.insert(0, ('right', set(operators)))
        return cls
    return _wrapper


def nonAssoc(*operators):
    """
    Class decorator for non associative operators. Same remarks as :py:func:`leftAssoc`.
    """
    def _wrapper(cls):
        cls.__precedence__.insert(0, ('non', set(operators)))
        return cls
    return _wrapper


class _StartState(metaclass=Singleton):
    __reprval__ = '\u03A3'


class _ResolveError(Exception):
    pass


@functools.total_ordering
class _Item(object):
    __slots__ = ('production', 'dot', 'terminal', 'index', 'shouldReduce', 'expecting')

    def __init__(self, prod, dot, terminal):
        self.production = prod
        self.dot = dot
        self.terminal = terminal
        self.index = None
        self.shouldReduce = self.dot == len(self.production.right)
        self.expecting = None if self.shouldReduce else self.production.right[self.dot]

    def next(self):
        """
        Returns an item with the dot advanced one position
        """
        return _Item(self.production, self.dot + 1, self.terminal)

    def hasPrefix(self, *tokens):
        """
        Return True if the passed sequence of token types appears right before the dot
        """
        if len(tokens) > self.dot:
            return False
        for tok1, tok2 in zip(self.production.right[self.dot - len(tokens):self.dot], tokens):
            if tok1 != tok2:
                return False
        return True

    def __repr__(self):
        symbols = list(self.production.right)
        symbols.insert(self.dot, '\u2022')
        return '%s -> %s (%s)' % (self.production.name, ' '.join([repr(sym) for sym in symbols]), self.terminal)

    def __eq__(self, other):
        return (self.production, self.dot, self.terminal) == (other.production, other.dot, other.terminal)

    def __lt__(self, other):
        return (self.production, self.dot, self.terminal) < (other.production, other.dot, other.terminal)

    def __hash__(self):
        return hash((self.production, self.dot, self.terminal))


class _Accept(BaseException):
    def __init__(self, result):
        self.result = result
        super().__init__()


_StackItem = collections.namedtuple('_StackItem', ['state', 'value', 'position'])


class _Shift(object):
    def __init__(self, newState):
        self.newState = newState

    def doAction(self, grammar, stack, tok): # pylint: disable=W0613
        stack.append(_StackItem(self.newState, tok.value, tok.position))
        return True


class _Reduce(object):
    def __init__(self, item):
        self.item = item
        self.nargs = len(item.production.right)

    def doAction(self, grammar, stack, tok): # pylint: disable=W0613
        pos, (callback, kwargs) = self._getCallback(stack)
        self._applied(grammar, stack, callback(grammar, **kwargs), pos)
        return False

    def _applied(self, grammar, stack, prodVal, position):
        stack.append(_StackItem(grammar.goto(stack[-1].state, self.item.production.name), prodVal, position))

    def _getCallback(self, stack):
        if self.nargs:
            args = [stackItem.value for stackItem in stack[-self.nargs:]]
            pos = stack[-self.nargs].position
            stack[-self.nargs:] = []
        else:
            args = []
            pos = stack[-1].position # Hum.
        return pos, self.item.production.apply(args, pos)


class LRParser(Grammar):
    """
    LR(1) parser. This class is intended to be used with a lexer class
    derived from :py:class:`LexerBase`, using inheritance; it
    overrides :py:func:`LexerBase.newToken` so you must inherit from
    the parser first, then the lexer:

    .. code-block:: python

       class MyParser(LRParser, ReLexer):
           # ...

    """
    def __init__(self): # pylint: disable=R0914,R0912
        super().__init__()
        self._restartParser()

    def rstack(self):
        return reversed(self.__stack)

    def newToken(self, tok):
        try:
            for action, stack in self._processToken(tok):
                if action.doAction(self, stack, tok):
                    break
            self.__tokens.append(tok)
        except _Accept as exc:
            self._restartParser()
            return self.newSentence(exc.result)

    def currentLRState(self):
        for item in self.__stack[-1].state:
            return item.index

    def _processToken(self, tok):
        while True:
            action = self.__actions__.get((self.__stack[-1].state, tok.type), None)
            if action is None:
                raise ParseError(self, tok, self.__stack[-1].state, self.__tokens)
            yield action, self.__stack

    def newSentence(self, sentence): # pragma: no cover
        """
        This is called when the start symbol has been reduced.

        :param sentence: The value associated with the start symbol.
        """
        raise NotImplementedError

    @classmethod
    def _createProductionParser(cls, name, priority, attrs):
        return ProductionParser(callbackByName(name), priority, cls, attrs)

    @classmethod
    def _createReduceAction(cls, item):
        return _Reduce(item)

    @classmethod
    def _createShiftAction(cls, state):
        return _Shift(state)

    @classmethod
    def prepare(cls):
        for prod in cls.productions():
            if prod.name is _StartState:
                break
        else:
            def acceptor(_, result):
                raise _Accept(result)
            prod = Production(_StartState, acceptor)
            prod.addSymbol(cls._defaultStartSymbol() if cls.startSymbol is None else cls.startSymbol, name='result')
            cls.__productions__.insert(0, prod)

        cls.startSymbol = _StartState
        super().prepare()

        states, goto = cls.__computeStates(prod)
        reachable = cls.__computeActions(states, goto)

        logger = logging.getLogger('LRParser')
        cls.__resolveConflicts(logger)

        usedTokens = set([symbol for state, symbol in cls.__actions__.keys() if symbol is not EOF])
        if usedTokens != cls.tokenTypes(): # pragma: no cover
            logger.warning('The following tokens are not used: %s', ','.join([repr(sym) for sym in sorted(cls.tokenTypes() - usedTokens)]))

        if reachable != cls.nonterminals(): # pragma: no cover
            logger.warning('The following nonterminals are not reachable: %s', ','.join([repr(sym) for sym in sorted(cls.nonterminals() - reachable)]))

        # Reductions only need goto entries for nonterminals
        cls._goto = dict([((state, symbol), newState) for (state, symbol), newState in goto.items() if symbol not in cls.tokenTypes()])

        parts = list()
        if cls.nSR:
            parts.append('%d shift/reduce conflicts' % cls.nSR)
        if cls.nRR:
            parts.append('%d reduce/reduce conflicts' % cls.nRR)
        if parts:
            logger.warning(', '.join(parts))

        # Cast to tuple because sets are not totally ordered
        for index, state in enumerate([tuple(cls._startState)] + sorted([tuple(state) for state in states if state != cls._startState])):
            logger.debug('State %d', index)
            for item in sorted(state):
                logger.debug('    %s', item)
                item.index = index
            cls.__lrstates__.append(sorted(state))
        logger.info('%d states.', len(states))

    @classmethod
    def __computeStates(cls, start):
        allSyms = list(cls.tokenTypes() | cls.nonterminals())
        goto = list()
        cls._startState = frozenset([_Item(start, 0, EOF)])
        states = set([cls._startState])
        stack = [cls._startState]
        while stack:
            state = stack.pop()
            stateClosure = cls.__itemSetClosure(state)
            for symbol in allSyms:
                # Compute goto(symbol, state)
                nextState = frozenset([item.next() for item in stateClosure if item.expecting == symbol])
                if nextState:
                    goto.append(((state, symbol), nextState))
                    if nextState not in states:
                        states.add(nextState)
                        stack.append(nextState)
        return states, dict(goto)

    @classmethod
    def __computeActions(cls, states, goto):
        cls.__actions__ = dict()
        reachable = set()
        tokenTypes = cls.tokenTypes()
        for state in states:
            for item in cls.__itemSetClosure(state):
                if item.shouldReduce:
                    action = cls._createReduceAction(item)
                    reachable.add(item.production.name)
                    cls.__addReduceAction(state, item.terminal, action)
                else:
                    symbol = item.production.right[item.dot]
                    if symbol in tokenTypes:
                        cls.__addShiftAction(state, symbol, cls._createShiftAction(goto[(state, symbol)]))
        return reachable

    @classmethod
    def __shouldPreferShift(cls, logger, reduceAction, symbol):
        logger.info('Shift/reduce conflict for "%s" on "%s"', reduceAction.item, symbol)

        prodPrecedence = reduceAction.item.production.precedence(cls)
        tokenPrecedence = cls.terminalPrecedence(symbol)

        # If both precedences are specified, use priority/associativity
        if prodPrecedence is not None and tokenPrecedence is not None:
            prodAssoc, prodPrio = prodPrecedence
            tokenAssoc, tokenPrio = tokenPrecedence
            if prodPrio > tokenPrio:
                logger.info('Resolving in favor of reduction because of priority')
                return False
            if prodPrio < tokenPrio:
                logger.info('Resolving in favor of shift because of priority')
                return True
            if prodAssoc == tokenAssoc:
                if prodAssoc == 'non':
                    logger.info('Resolving in favor of error because of associativity')
                    raise _ResolveError()
                if prodAssoc == 'left':
                    logger.info('Resolving in favor of reduction because of associativity')
                    return False
                logger.info('Resolving in favor of shift because of associativity')
                return True

        # At least one of those is not specified; use shift
        logger.warning('Could not disambiguate shift/reduce conflict for "%s" on "%s"; using shift' % (reduceAction.item, symbol))
        cls.nSR += 1
        return True

    @classmethod
    def __resolveConflicts(cls, logger):
        cls.nSR = 0
        cls.nRR = 0

        for (state, symbol), actions in sorted(cls.__actions__.items()):
            action = actions.pop()
            while actions:
                conflicting = actions.pop()
                try:
                    action = cls.__resolveConflict(logger, action, conflicting, symbol)
                except _ResolveError:
                    del cls.__actions__[(state, symbol)]
                    break
            else:
                cls.__actions__[(state, symbol)] = action

    @classmethod
    def __resolveConflict(cls, logger, action1, action2, symbol):
        if isinstance(action2, _Shift):
            action1, action2 = action2, action1

        if isinstance(action1, _Shift):
            # Shift/reduce
            return action1 if cls.__shouldPreferShift(logger, action2, symbol) else action2

        # Reduce/reduce
        logger.warning('Reduce/reduce conflict between "%s" and "%s"', action1.item, action2.item)
        cls.nRR += 1

        # Use the first one to be declared
        for prod in cls.productions():
            if prod == action1.item.production:
                logger.warning('Using "%s', prod)
                return action1
            if prod == action2.item.production:
                logger.warning('Using "%s', prod)
                return action2

    @classmethod
    def __addReduceAction(cls, state, symbol, action):
        cls.__actions__.setdefault((state, symbol), list()).append(action)

    @classmethod
    def __addShiftAction(cls, state, symbol, action):
        for existing in cls.__actions__.get((state, symbol), list()):
            if isinstance(existing, _Shift):
                return
        cls.__actions__.setdefault((state, symbol), list()).append(action)

    @classmethod
    def goto(cls, state, symbol):
        return cls._goto[(state, symbol)]

    def _restartParser(self):
        self.__stack = [_StackItem(self._startState, None, LexerPosition(1, 1))]
        self.__tokens = []
        self.restartLexer()

    @classmethod
    @memoize
    def __itemSetClosure(cls, items):
        result = set(items)
        while True:
            prev = set(result)
            for item in [item for item in result if not item.shouldReduce]:
                symbol = item.production.right[item.dot]
                if symbol not in cls.tokenTypes():
                    terminals = cls.first(*tuple(item.production.right[item.dot + 1:] + [item.terminal]))
                    for prod in (prod for prod in cls.productions() if prod.name == symbol):
                        for terminal in terminals:
                            result.add(_Item(prod, 0, terminal))
            if prev == result:
                break
        return result


class ProductionParser(LRParser, ProgressiveLexer): # pylint: disable=R0904
    # pylint: disable=C0111,C0103,R0201
    def __init__(self, callback, priority, grammarClass, attributes): # pylint: disable=R0915
        self.callback = callback
        self.priority = priority
        self.grammarClass = grammarClass
        self.attributes = attributes

        super().__init__()

    @classmethod
    def prepare(cls, **kwargs): # pylint: disable=R0915
        # Obviously cannot use @production here

        # When mixing async and sync parsers in the same program this may be called twice,
        # because AsyncProductionParser inherits from ProductionParser
        if cls.productions():
            return

        # DECL -> identifier "->" PRODS
        prod = Production('DECL', cls.DECL)
        prod.addSymbol('LEFT', 'left')
        prod.addSymbol('arrow')
        prod.addSymbol('PRODS', 'prods')
        cls.__productions__.append(prod)

        # LEFT -> identifier
        prod = Production('LEFT', cls.LEFT)
        prod.addSymbol('identifier', 'name')
        cls.__productions__.append(prod)

        # LEFT -> identifier "<" posarg ">"
        prod = Production('LEFT', cls.LEFT)
        prod.addSymbol('identifier', 'name')
        prod.addSymbol('lchev')
        prod.addSymbol('identifier', 'posarg')
        prod.addSymbol('rchev')
        cls.__productions__.append(prod)

        # PRODS -> P
        prod = Production('PRODS', cls.PRODS1)
        prod.addSymbol('P', 'prodlist')
        cls.__productions__.append(prod)

        # PRODS -> PRODS "|" P
        prod = Production('PRODS', cls.PRODS2)
        prod.addSymbol('PRODS', 'prods')
        prod.addSymbol('union')
        prod.addSymbol('P', 'prodlist')
        cls.__productions__.append(prod)

        # P -> P SYM
        prod = Production('P', cls.P1)
        prod.addSymbol('P', 'prodlist')
        prod.addSymbol('SYM', 'sym')
        cls.__productions__.append(prod)

        # P -> ɛ
        prod = Production('P', cls.P2)
        cls.__productions__.append(prod)

        # SYM -> SYMNAME PROPERTIES
        prod = Production('SYM', cls.SYM)
        prod.addSymbol('SYMNAME', 'symname')
        prod.addSymbol('PROPERTIES', 'properties')
        cls.__productions__.append(prod)

        # SYM -> SYMNAME repeat PROPERTIES
        prod = Production('SYM', cls.SYMREP)
        prod.addSymbol('SYMNAME', 'symname')
        prod.addSymbol('repeat', 'repeat')
        prod.addSymbol('PROPERTIES', 'properties')
        cls.__productions__.append(prod)

        # SYM -> SYMNAME repeat lparen identifier rparen PROPERTIES
        prod = Production('SYM', cls.SYMREP)
        prod.addSymbol('SYMNAME', 'symname')
        prod.addSymbol('repeat', 'repeat')
        prod.addSymbol('lparen')
        prod.addSymbol('identifier', 'separator')
        prod.addSymbol('rparen')
        prod.addSymbol('PROPERTIES', 'properties')
        cls.__productions__.append(prod)

        # SYM -> SYMNAME repeat lparen litteral rparen PROPERTIES
        prod = Production('SYM', cls.SYMREP_LIT)
        prod.addSymbol('SYMNAME', 'symname')
        prod.addSymbol('repeat', 'repeat')
        prod.addSymbol('lparen')
        prod.addSymbol('litteral', 'separator')
        prod.addSymbol('rparen')
        prod.addSymbol('PROPERTIES', 'properties')
        cls.__productions__.append(prod)

        # SYMNAME -> identifier
        prod = Production('SYMNAME', cls.SYMNAME1)
        prod.addSymbol('identifier', 'identifier')
        cls.__productions__.append(prod)

        # SYMNAME -> litteral
        prod = Production('SYMNAME', cls.SYMNAME2)
        prod.addSymbol('litteral', 'litteral')
        cls.__productions__.append(prod)

        # PROPERTIES -> ɛ
        prod = Production('PROPERTIES', cls.PROPERTIES1)
        cls.__productions__.append(prod)

        # PROPERTIES -> lchev identifier rchev
        prod = Production('PROPERTIES', cls.PROPERTIES2)
        prod.addSymbol('lchev')
        prod.addSymbol('identifier', 'name')
        prod.addSymbol('rchev')
        cls.__productions__.append(prod)

        super().prepare(**kwargs)

    def newSentence(self, startSymbol):
        (name, posarg), prods = startSymbol
        for prod in prods:
            if prod.name is None:
                prod.name = name
                prod.posarg = posarg
        self.grammarClass.__productions__.extend(prods)

    # Lexer

    @staticmethod
    def ignore(char):
        return char in ' \t\n'

    @token('->')
    def arrow(self, tok):
        pass

    @token('<')
    def lchev(self, tok):
        pass

    @token('>')
    def rchev(self, tok):
        pass

    @token(r'\|')
    def union(self, tok):
        pass

    @token(r'\*|\+|\?')
    def repeat(self, tok):
        pass

    @token(r'\(')
    def lparen(self, tok):
        pass

    @token(r'\)')
    def rparen(self, tok):
        pass

    @token('[a-zA-Z_][a-zA-Z0-9_]*')
    def identifier(self, tok):
        pass

    @token(r'"|\'')
    def litteral(self, tok):
        class StringBuilder(object):
            def __init__(self, quotetype):
                self.quotetype = quotetype
                self.chars = list()
                self.state = 0
            def feed(self, char):
                if self.state == 0:
                    if char == '\\':
                        self.state = 1
                    elif char == self.quotetype:
                        return 'litteral', ''.join(self.chars)
                    else:
                        self.chars.append(char)
                elif self.state == 1:
                    self.chars.append(char)
                    self.state = 0
        self.setConsumer(StringBuilder(tok.value))

    # Parser

    def DECL(self, left, prods):
        name, posarg = left
        if name in self.grammarClass.tokenTypes():
            raise GrammarError('"%s" is a token name and cannot be used as non-terminal' % name)
        return (left, prods)

    def LEFT(self, name, posarg=None):
        return (name, posarg)

    def PRODS1(self, prodlist):
        return prodlist

    def PRODS2(self, prods, prodlist):
        prods.extend(prodlist)
        return prods

    def P1(self, sym, prodlist):
        result = list()
        symbol, properties, repeat, sep = sym

        for prod in prodlist:
            if prod.name is None:
                if repeat is None:
                    prod.addSymbol(symbol, name=properties.get('name', None))
                    result.append(prod)
                elif repeat == '?':
                    if sep is not None:
                        raise GrammarError('A separator makes no sense for "?"')
                    self.__addAtMostOne(result, prod, symbol, properties.get('name', None))
                elif repeat in ['*', '+']:
                    self.__addList(result, prod, symbol, properties.get('name', None), repeat == '*', sep)
            else:
                result.append(prod)

        return result

    def __addAtMostOne(self, productions, prod, symbol, name):
        clone = prod.cloned()
        if name is not None:
            self._wrapCallbackNone(name, clone)
        productions.append(clone)

        prod.addSymbol(symbol, name=name)
        productions.append(prod)

    def _wrapCallbackNone(self, name, prod):
        previous = prod.callback
        def callback(*args, **kwargs):
            kwargs[name] = None
            return previous(*args, **kwargs)
        prod.callback = callback

    def __addList(self, productions, prod, symbol, name, allowEmpty, sep):
        class ListSymbol(metaclass=Singleton):
            __reprval__ = 'List(%s, "%s")' % (symbol, '*' if allowEmpty else '+')

        if allowEmpty:
            clone = prod.cloned()
            self._wrapCallbackEmpty(name, clone)
            productions.append(clone)

        prod.addSymbol(ListSymbol, name=name)
        productions.append(prod)

        listProd = Production(ListSymbol, self._wrapCallbackOne())
        listProd.addSymbol(symbol, name='item')
        productions.append(listProd)

        listProd = Production(ListSymbol, self._wrapCallbackNext())
        listProd.addSymbol(ListSymbol, name='items')
        if sep is not None:
            listProd.addSymbol(sep)
        listProd.addSymbol(symbol, name='item')
        productions.append(listProd)

    def _wrapCallbackEmpty(self, name, prod):
        previous = prod.callback
        def cbEmpty(*args, **kwargs):
            if name is not None:
                kwargs[name] = []
            return previous(*args, **kwargs)
        prod.callback = cbEmpty

    def _wrapCallbackOne(self):
        def cbOne(_, item):
            return [item]
        return cbOne

    def _wrapCallbackNext(self):
        def cbNext(_, items, item):
            items.append(item)
            return items
        return cbNext

    def P2(self):
        # 'name' is replaced in newSentence()
        return [Production(None, self.callback, priority=self.priority, attributes=self.attributes)]

    def SYMNAME1(self, identifier):
        return identifier

    def SYMNAME2(self, litteral):
        name = litteral
        if name not in self.grammarClass.tokenTypes():
            self.grammarClass.addTokenType(name, lambda s, tok: None, re.escape(name), None)
        return name

    def SYM(self, symname, properties):
        return (symname, properties, None, None)

    def SYMREP(self, symname, repeat, properties, separator=None):
        return (symname, properties, repeat, separator)

    def SYMREP_LIT(self, symname, repeat, properties, separator):
        if separator not in self.grammarClass.tokenTypes():
            self.grammarClass.addTokenType(separator, lambda s, tok: None, re.escape(separator), None)
        return self.SYMREP(symname, repeat, properties, separator)

    def PROPERTIES1(self):
        return dict()

    def PROPERTIES2(self, name):
        return dict(name=name)

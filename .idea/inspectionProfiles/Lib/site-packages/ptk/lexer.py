# -*- coding: UTF-8 -*-

# (c) Jérôme Laheurte 2015-2019
# See LICENSE.txt

import inspect
import re

from ptk.regex import buildRegex, DeadState, RegexTokenizer, LexerPosition
from ptk.utils import Singleton, callbackByName, chars


# In Python 3 we'd use __prepare__ and an ordered dict...
_TOKREGISTER = list()


class _LexerMeta(type):
    def __new__(metacls, name, bases, attrs):
        global _TOKREGISTER # pylint: disable=W0603
        try:
            attrs['__tokens__'] = (set(), list()) # Set of token names, list of (rx, callback, defaultType)
            klass = super().__new__(metacls, name, bases, attrs)
            for func, rx, toktypes in _TOKREGISTER:
                klass.addTokenType(func.__name__, callbackByName(func.__name__), rx, toktypes)
            return klass
        finally:
            _TOKREGISTER = list()


def token(rx, types=None):
    def _wrap(func):
        if any([func.__name__ == aFunc.__name__ and func != aFunc for aFunc, _, _ in _TOKREGISTER]):
            raise TypeError('Duplicate token method name "%s"' % func.__name__)
        _TOKREGISTER.append((func, rx, types))
        return func
    return _wrap


class SkipToken(Exception):
    """
    Raise this from your consumer to ignore the token.
    """


class LexerError(Exception):
    """
    Unrecognized token in input

    :ivar lineno: Line in input
    :ivar colno: Column in input
    """
    def __init__(self, char, colno, lineno):
        super().__init__('Unrecognized token "%s" at line %d, column %d' % (char, lineno, colno))
        self.lineno = lineno
        self.colno = colno


class EOF(metaclass=Singleton):
    """
    End symbol
    """

    __reprval__ = '$'

    @property
    def type(self):
        """Read-only attribute for Token duck-typing"""
        return self
    @property
    def value(self):
        """Read-only attribute for Token duck-typing"""
        return self


class LexerBase(metaclass=_LexerMeta):
    """
    This defines the interface for lexer classes. For concrete
    implementations, see :py:class:`ProgressiveLexer` and
    :py:class:`ReLexer`.
    """

    Token = RegexTokenizer.Token

    # Shut up pychecker. Those are actually set by the metaclass.
    __tokens__ = ()

    class _MutableToken(object):
        def __init__(self, type_, value, position):
            self.type = type_
            self.value = value
            self.position = position

        def token(self):
            """Returns the unmutable equivalent"""
            return EOF if EOF in [self.type, self.value] else RegexTokenizer.Token(self.type, self.value, self.position)

    def __init__(self):
        super().__init__()
        self.restartLexer()

    def restartLexer(self, resetPos=True):
        if resetPos:
            self._pos = LexerPosition(column=1, line=1)
            self._input = list()
        self._consumer = None

    def position(self):
        """
        :return: The current position in stream as a 2-tuple (column, line).
        """
        return self._pos

    def advanceColumn(self, count=1):
        """
        Advances the current position by *count* columns.
        """
        self._pos = self._pos._replace(column=self._pos.column + count)

    def advanceLine(self, count=1):
        """
        Advances the current position by *count* lines.
        """
        self._pos = self._pos._replace(column=1, line=self._pos.line + count)

    @staticmethod
    def ignore(char):
        """
        Override this to ignore characters in input stream. The
        default is to ignore spaces and tabs.

        :param char: The character to test
        :return: True if *char* should be ignored
        """
        return char in chars(' ') + chars('\t')

    def setConsumer(self, consumer):
        """
        Sets the current consumer. A consumer is an object with a
        *feed* method; all characters seen on the input stream after
        the consumer is set are passed directly to it. When the *feed*
        method returns a 2-tuple (type, value), the corresponding
        token is generated and the consumer reset to None. This may be
        handy to parse tokens that are not easily recognized by a
        regular expression but easily by code; for instance the
        following lexer recognizes C strings without having to use
        negative lookahead:

        .. code-block:: python

           class MyLexer(ReLexer):
               @token('"')
               def cstring(self, tok):
                   class CString(object):
                       def __init__(self):
                           self.state = 0
                           self.value = StringIO.StringIO()
                       def feed(self, char):
                           if self.state == 0:
                               if char == '"':
                                   return 'cstring', self.value.getvalue()
                               if char == '\\\\':
                                   self.state = 1
                               else:
                                   self.value.write(char)
                           elif self.state == 1:
                               self.value.write(char)
                               self.state = 0
                   self.setConsumer(CString())

        You can also raise SkipToken instead of returning a token if it
        is to be ignored (comments).
        """
        self._consumer = consumer

    def consumer(self):
        return self._consumer

    def parse(self, string): # pragma: no cover
        """
        Parses the whole *string*
        """
        raise NotImplementedError

    def newToken(self, tok): # pragma: no cover
        """
        This method will be invoked as soon as a token is recognized on input.

        :param tok: The token. This is a named tuple with *type* and *value* attributes.
        """
        raise NotImplementedError

    @classmethod
    def addTokenType(cls, name, callback, regex, types=None):
        for typeName in [name] if types is None else types:
            if typeName is not EOF:
                cls.__tokens__[0].add(typeName)
        cls.__tokens__[1].append((regex, callback, name if types is None else None))

    @classmethod
    def _allTokens(cls):
        tokens = (set(), list())
        for base in inspect.getmro(cls):
            if issubclass(base, LexerBase):
                tokens[0].update(base.__tokens__[0])
                tokens[1].extend(base.__tokens__[1])
        return tokens

    @classmethod
    def tokenTypes(cls):
        """
        :return: the set of all token names, as strings.
        """
        return cls._allTokens()[0]


class ReLexer(LexerBase): # pylint: disable=W0223
    """
    Concrete lexer based on Python regular expressions. this is
    **way** faster than :py:class:`ProgressiveLexer` but it can only
    tokenize whole strings.
    """
    def __init__(self):
        self._regexes = list()
        for rx, callback, defaultType in self._allTokens()[1]:
            crx = re.compile((b'^' if isinstance(rx, bytes) else '^') + rx)
            self._regexes.append((crx, callback, defaultType))
        super().__init__()

    def _parse(self, string, pos):
        while pos < len(string):
            char = string[pos]
            try:
                if self.consumer() is None:
                    if self.ignore(char):
                        pos += 1
                        continue
                    pos = self._findMatch(string, pos)
                else:
                    try:
                        tok = self.consumer().feed(char)
                    except SkipToken:
                        self.setConsumer(None)
                    else:
                        if tok is not None:
                            self.setConsumer(None)
                            if tok[0] is not None:
                                self.newToken(self.Token(*tok, self.position()))
                    pos += 1
            finally:
                if char in chars('\n'):
                    self.advanceLine()
                else:
                    self.advanceColumn()
        return pos

    def parse(self, string):
        self._parse(string, 0)
        return self.newToken(EOF)

    def _findMatch(self, string, pos):
        match = None
        matchlen = 0
        pos2d = self.position()

        for rx, callback, defaultType in self._regexes:
            mtc = rx.match(string[pos:])
            if mtc:
                value = mtc.group(0)
                if len(value) > matchlen:
                    match = value, callback, defaultType
                    matchlen = len(value)

        if match:
            value, callback, defaultType = match
            tok = self._MutableToken(defaultType, value, pos2d)
            callback(self, tok)
            pos += matchlen
            if self.consumer() is None and tok.type is not None:
                self.newToken(tok.token())
            self.advanceColumn(matchlen - 1)
            return pos
        else:
            raise LexerError(string[pos:pos+10], *pos2d)


class ProgressiveLexer(LexerBase): # pylint: disable=W0223
    """
    Concrete lexer based on a simple pure-Python regular expression
    engine. This lexer is able to tokenize an input stream in a
    progressive fashion; just call the
    :py:func:`ProgressiveLexer.feed` method with whatever bytes are
    available when they're available. Useful for asynchronous
    contexts. Starting with Python 3.5 there is also an asynchronous
    version, see :py:class:`AsyncLexer`.

    This is **slow as hell**.
    """
    def restartLexer(self, resetPos=True):
        self._currentState = [(buildRegex(rx).start(), callback, defaultType, [0]) for rx, callback, defaultType in self._allTokens()[1]]
        self._currentMatch = list()
        self._matches = list()
        self._maxPos = 0
        self._state = 0
        self._input = list()
        super().restartLexer(resetPos=resetPos)

    def parse(self, string):
        for char in string:
            self.feed(char)
        self.feed(EOF)

    def feed(self, char):
        """
        Handle a single input character. When you're finished, call
        this with EOF as argument.
        """

        self._input.append((char, self.position()))
        if char in chars('\n'):
            self.advanceLine()
        else:
            self.advanceColumn()

        while self._input:
            char, charPos = self._input.pop(0)
            for tok in self._feed(char, charPos):
                self.newToken(tok)

    def _feed(self, char, charPos): # pylint: disable=R0912,R0915
        if self.consumer() is not None:
            try:
                tok = self.consumer().feed(char)
            except SkipToken:
                self.setConsumer(None)
            else:
                if tok is not None:
                    self.setConsumer(None)
                    if tok[0] is not None:
                        yield self.Token(*tok, charPos)
            return

        try:
            if char is EOF:
                if self._state == 0:
                    self.restartLexer()
                    yield EOF
                    return
                self._maxPos = max(self._maxPos, max(pos[0] for regex, callback, defaultType, pos in self._currentState))
                if self._maxPos == 0 and self._currentMatch:
                    raise LexerError(self._currentMatch[0][0], *self._currentMatch[0][1])
                self._matches.extend([(pos[0], callback) for regex, callback, defaultType, pos in self._currentState if pos[0] == self._maxPos])
                self._matches = [(pos, callback) for pos, callback in self._matches if pos == self._maxPos]
            else:
                if self._state == 0 and self.ignore(char):
                    return
                self._state = 1

                newState = list()
                for regex, callback, defaultType, pos in self._currentState:
                    try:
                        if regex.feed(char):
                            pos[0] = len(self._currentMatch) + 1
                    except DeadState:
                        if pos[0]:
                            self._matches.append((pos[0], callback))
                            self._maxPos = max(self._maxPos, pos[0])
                    else:
                        newState.append((regex, callback, defaultType, pos))

                if all([regex.isDeadEnd() for regex, callback, defaultType, pos in newState]):
                    for regex, callback, defaultType, pos in newState:
                        self._matches.append((len(self._currentMatch) + 1, callback))
                        self._maxPos = max(self._maxPos, len(self._currentMatch) + 1)
                    newState = list()

                self._matches = [(pos, callback) for pos, callback in self._matches if pos == self._maxPos]
                self._currentState = newState

                self._currentMatch.append((char, charPos))
                if self._currentState:
                    return

                if self._maxPos == 0:
                    raise LexerError(char, *charPos)
        except LexerError:
            self.restartLexer()
            raise

        tok = self._finalizeMatch()
        if tok is not None:
            yield tok

        if char is EOF:
            self.restartLexer()
            yield EOF

    def _finalizeMatch(self):
        # First declared token method
        matches = set([callback for _, callback in self._matches])
        sep = '' if isinstance(self._currentMatch[0][0], str) else b''
        match = sep.join([(bytes([char]) if isinstance(char, int) else char) \
                          for char, pos in self._currentMatch[:self._maxPos]]) # byte or unicode
        remain = self._currentMatch[self._maxPos:]
        pos = self._currentMatch[0][1]
        self.restartLexer(False)
        self._input.extend(remain)
        for _, callback, defaultType in self._allTokens()[1]:
            if callback in matches:
                tok = self._MutableToken(defaultType, match, pos)
                callback(self, tok)
                if tok.type is None or self.consumer() is not None:
                    break
                return tok.token()

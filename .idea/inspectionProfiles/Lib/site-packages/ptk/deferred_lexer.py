# -*- coding: UTF-8 -*-

# (c) Jérôme Laheurte 2015-2019
# See LICENSE.txt

from ptk.lexer import ProgressiveLexer, token, EOF, LexerError # pylint: disable=W0611

from twisted.internet.defer import Deferred


class DeferredLexer(ProgressiveLexer):
    """

    This class works like :py:class:`ProgressiveLexer` but can be feed
    the input asynchronously via :py:func:`deferFeed`. It works with
    :py:class:`DeferredLRParser`.

    """

    def deferFeed(self, char, charPos=None):
        """
        Asynchronous version of :py:func:`ProgressiveLexer.feed`. This
        will wait for the deferred returned by
        :py:func:`deferNewToken` instead of calling 'newToken'
        synchronously.
        """
        self._input.append((char, charPos))
        d = Deferred()

        def nextInput(result): # pylint: disable=W0613
            if self._input:
                char, charPos = self._input.pop(0)
                tokens = self._feed(char, charPos)
                def gotToken(result): # pylint: disable=W0613
                    try:
                        tok = tokens.__next__()
                    except StopIteration:
                        nextInput(None)
                    else:
                        self.deferNewToken(tok).addCallbacks(gotToken, d.errback)
                gotToken(None)
            else:
                d.callback(None)
        nextInput(None)

        return d

    def deferNewToken(self, tok):
        """
        Asynchronous version of py:func:`LexerBase.newToken`. Must
        return a Deferred.
        """
        raise NotImplementedError

# -*- coding: UTF-8 -*-

# (c) Jérôme Laheurte 2015-2019
# See LICENSE.txt

from ptk.parser import production, LRParser, ProductionParser, leftAssoc, rightAssoc, nonAssoc, ParseError, _Accept, _Reduce, _Shift # pylint: disable=W0611
from ptk.utils import callbackByName

from twisted.internet.defer import succeed, Deferred, maybeDeferred
from twisted.python.failure import Failure


class _DeferShift(_Shift):
    def deferDoAction(self, grammar, stack, tok):
        return succeed(self.doAction(grammar, stack, tok))


class _DeferReduce(_Reduce):
    def deferDoAction(self, grammar, stack, tok): # pylint: disable=W0613
        callback, kwargs = self._getCallback(stack)
        d = Deferred()
        def applied(prodVal):
            try:
                self._applied(grammar, stack, prodVal)
                d.callback(False)
            except Exception: # pylint: disable=W0703
                d.errback(Failure())
        maybeDeferred(callback, grammar, **kwargs).addCallbacks(applied, d.errback)
        return d


class DeferredProductionParser(ProductionParser):
    def _wrapCallbackOne(self):
        def cbOne(_, item):
            return succeed([item])
        return cbOne

    def _wrapCallbackNext(self):
        def cbNext(_, items, item):
            items.append(item)
            return succeed(items)
        return cbNext


class DeferredLRParser(LRParser):
    """
    This class works like :py:class:`LRParser` but supports
    returning a Deferred from semantic actions. You must use
    :py:class:`DeferredLexer` in conjuction with it:

    .. code-block:: python

    class Parser(DeferredLRParser, DeferredLexer):
        # ...

    And only use :py:func:`DeferredLexer.deferFeed` to feed it the input
    stream. Semantic actions must return Deferred instances.  When the
    start symbol is reduced, the :py:func:`deferNewSentence` method is
    called and must return a Deferred."""

    def deferNewToken(self, tok):
        d = Deferred()
        actions = self._processToken(tok)

        def error(reason):
            if reason.check(_Accept):
                self._restartParser()
                self.deferNewSentence(reason.value.result).chainDeferred(d)
            else:
                d.errback(reason)

        def nextAction(result):
            if result:
                d.callback(None)
                return result

            try:
                action, stack = actions.__next__()
            except StopIteration:
                d.callback(None)
            else:
                try:
                    df = action.deferDoAction(self, stack, tok)
                except Exception: # pylint: disable=W0703
                    d.errback(Failure())
                else:
                    df.addCallback(nextAction)
                    df.addErrback(error)

        nextAction(False)
        return d

    def deferNewSentence(self, result):
        """
        Called when the start symbol is reached. Must return a Deferred.
        """
        raise NotImplementedError

    @classmethod
    def _createProductionParser(cls, name, priority, attributes):
        return DeferredProductionParser(callbackByName(name), priority, cls, attributes)

    @classmethod
    def _createShiftAction(cls, state):
        return _DeferShift(state)

    @classmethod
    def _createReduceAction(cls, item):
        return _DeferReduce(item)

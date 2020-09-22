# -*- coding: UTF-8 -*-

# (c) Jérôme Laheurte 2015-2019
# See LICENSE.txt

# XXXTODO: when pylint supports async, remove this...
# pylint: skip-file

from ptk.parser import production, LRParser, ProductionParser, leftAssoc, rightAssoc, nonAssoc, ParseError, _Accept, _Reduce, _Shift


class _AsyncShift(_Shift):
    async def asyncDoAction(self, grammar, stack, tok):
        return self.doAction(grammar, stack, tok)


class _AsyncReduce(_Reduce):
    async def asyncDoAction(self, grammar, stack, tok):
        callback, kwargs = self._getCallback(stack)
        prodVal = await callback(grammar, **kwargs)
        self._applied(grammar, stack, prodVal)
        return False


class AsyncProductionParser(ProductionParser):
    def _wrapCallbackNone(self, name, prod):
        previous = prod.callback
        async def callback(*args, **kwargs):
            kwargs[name] = None
            return await previous(*args, **kwargs)
        prod.callback = callback

    def _wrapCallbackEmpty(self, name, prod):
        previous = prod.callback
        async def cbEmpty(*args, **kwargs):
            if name is not None:
                kwargs[name] = []
            return await previous(*args, **kwargs)
        prod.callback = cbEmpty

    def _wrapCallbackOne(self):
        async def cbOne(_, item):
            return [item]
        return cbOne

    def _wrapCallbackNext(self):
        async def cbNext(_, items, item):
            items.append(item)
            return items
        return cbNext


def asyncCallbackByName(name):
    async def _wrapper(instance, *args, **kwargs):
        return await getattr(instance, name)(*args, **kwargs)
    return _wrapper


class AsyncLRParser(LRParser):
    """
    This class works like :py:class:`LRParser` but supports
    asynchronous methods (new in Python 3.5). You must use
    :py:class:`AsyncLexer` in conjuction with it:

    .. code-block:: python

    class Parser(AsyncLRParser, AsyncLexer):
        # ...

    And only use :py:func:`AsyncLexer.asyncFeed` to feed it the input
    stream. Semantic actions must be asynchronous methods as
    well. When the start symbol is reduced, the
    :py:func:`asyncNewSentence` method is awaited.
    """

    async def asyncNewToken(self, tok):
        try:
            for action, stack in self._processToken(tok):
                if await action.asyncDoAction(self, stack, tok):
                    break
        except _Accept as exc:
            self._restartParser()
            await self.asyncNewSentence(exc.result)
            return exc.result

    async def asyncNewSentence(self, result):
       """
       Awaited when the start symbol is reached.
       """
       raise NotImplementedError

    @classmethod
    def _createProductionParser(cls, name, priority, attrs):
        return AsyncProductionParser(asyncCallbackByName(name), priority, cls, attrs)

    @classmethod
    def _createShiftAction(cls, state):
        return _AsyncShift(state)

    @classmethod
    def _createReduceAction(cls, item):
        return _AsyncReduce(item)

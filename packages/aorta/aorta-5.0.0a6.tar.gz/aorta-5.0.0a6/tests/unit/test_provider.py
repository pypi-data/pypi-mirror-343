import pytest

import aorta



@pytest.fixture
def provider():
    p = aorta.Provider()
    p.register(FilteredCommandHandlerAlpha)
    p.register(FilteredCommandHandlerBeta)
    p.register(FilteredEventListenerAlpha)
    p.register(FilteredEvenListenerBeta)


def test_filter_command(provider: aorta.Provider):
    envelope = FilteredCommand(message='Hello world!').envelope()
    assert len(aorta.get(envelope, False)) == 2
    assert len(aorta.get(envelope, include={FilteredCommandHandlerAlpha.qualname})) == 1
    assert aorta.get(envelope, include={FilteredCommandHandlerAlpha.qualname}) == {FilteredCommandHandlerAlpha}


def test_filter_event(provider: aorta.Provider):
    envelope = FilteredEvent(message='Hello world!').envelope()
    assert len(aorta.get(envelope, False)) == 2
    assert len(aorta.get(envelope, include={FilteredEventListenerAlpha.qualname})) == 1
    assert aorta.get(envelope, include={FilteredEventListenerAlpha.qualname}) == {FilteredEventListenerAlpha}



class FilteredCommand(aorta.Command):
    message: str


class FilteredCommandHandlerAlpha(aorta.CommandHandler[FilteredCommand]):
    pass


class FilteredCommandHandlerBeta(aorta.CommandHandler[FilteredCommand]):
    pass



class FilteredEvent(aorta.Event):
    message: str


class FilteredEventListenerAlpha(aorta.EventListener[FilteredEvent]):
    pass


class FilteredEvenListenerBeta(aorta.EventListener[FilteredEvent]):
    pass
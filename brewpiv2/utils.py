from abc import ABC, abstractmethod


class Event(ABC):
    """
    Base class for a typed event
    """
    def __init__(self, name, description="No description"):
        self.name = name
        self.description = description


class Observer(ABC):
    """
    Abstract Observer Class for the Observer Pattern
    """


class Observable(ABC):
    """
    Abstract Observable Class for the Observer Pattern
    """
    def __init__(self):
        self._observers = []

    def subscribe(self, anObserver):
        """
        Subscribes to the manager events
        """
        if anObserver not in self._observers:
            self._observers.append(anObserver)

        return True

    def notify(self, anEvent, *args, **kwargs):
        """
        Dispatch an event to the `Observers`
        """
        for observer in self._observers:
            callback_name = "_on_{0}".format(anEvent.name)
            callback = getattr(observer, callback_name)
            callback(*args, **kwargs)


class Visitor(ABC):
    """
    Minismalist Visitor pattern
    """
    @abstractmethod
    def visit(self, aMessageHandler):
        raise NotImplementedError

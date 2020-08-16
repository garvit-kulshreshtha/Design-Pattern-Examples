from abc import ABC, abstractmethod
from enum import Enum, auto


class NotifyStrategy(ABC):
    def notify(self, message):
        pass


class EmailNotifyStrategy(NotifyStrategy):
    def notify(self, message):
        print(f"Sending email:{message}")


class SlackMsgNotifyStrategy(NotifyStrategy):
    def notify(self, message):
        print(f"Sending slack message:{message}")


class EventHandler(ABC):
    notify_strategy: NotifyStrategy

    @abstractmethod
    def handle(self, notify_strategy):
        pass

    def notify(self, event):
        pass


class WriteEventHandler(EventHandler):
    def __init__(self, notify_strategy=EmailNotifyStrategy()):
        self.notify_strategy = notify_strategy

    def handle(self, event):
        #
        # handle the event
        #
        self.notify(event)

    def notify(self, event):
        self.notify_strategy.notify(event)

    def set_notify_method(self, method):
        self.notify_strategy = method


class FailureEventHandler(EventHandler):
    def __init__(self, notify_strategy=SlackMsgNotifyStrategy()):
        self.notify_strategy = notify_strategy

    def handle(self, event):
        #
        # handle the event
        #
        self.notify(event)

    def notify(self, event):
        self.notify_strategy.notify(event)

    def set_notify_method(self, method):
        self.notify_strategy = method


# this class doesnot implement notify method because we
# don't want notification for read events
class ReadEventHandler(EventHandler):
    def __init__(self, notify_strategy=SlackMsgNotifyStrategy()):
        self.notify_strategy = notify_strategy

    def handle(self, event):
        #
        # handle the event
        #
        self.notify(event)

    def set_notify_method(self, method):
        self.notify_strategy = method


if __name__ == "__main__":
    event_handler = WriteEventHandler()
    event = "Write event occured"
    event_handler.handle(event)
    # change notify strategy at runtime
    event_handler.set_notify_method(SlackMsgNotifyStrategy())
    event_handler.handle(event)

    event_handler = FailureEventHandler()
    event = "Failure event occured"
    event_handler.handle(event)

    event_handler = ReadEventHandler()
    event = "read event occured"
    event_handler.handle(event)

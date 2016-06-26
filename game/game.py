from abc import ABCMeta, abstractmethod
import time
from exceptions import KeyError
import inspect

from pygame.locals import *
import pygame

from .custom_exceptions import NoEventHandlerError


def function_tag(tag):
    def decorator(func):
        func.key = tag
        return func
    return decorator


class PygameApp:
    '''
    A simple class to create games in pygame.
    '''
    __metaclass__ = ABCMeta

    class EventHandlerMethods:
        '''
        Contains all the event-handlers of the app.
        NOTE: This meta class must inherit from the outer class' parent's meta class to use the parent's event handlers.
        '''

        @function_tag(QUIT)
        def on_quit(self, *args, **kwargs):
            self.running = False

    def __init__(self, title='Game', window_dimensions=(900, 900), delay_time=1, background=None, images=None):
        self.running = True
        self.title = title

        self.window_dimensions = window_dimensions
        self.delay_time = delay_time
        self.images = images if images is not None else {}
        if background is not None:
            self.images.update({'BACKGROUND': background})

        self._set_event_handlers()

    def _set_event_handlers(self):
        '''Fetches the event handlers from the EventHandlerMethods meta class'''
        handlers = inspect.getmembers(self.EventHandlerMethods, predicate=inspect.ismethod)
        self.event_handlers = {handler.key:handler for handler_name, handler in handlers}

    def on_init(self):
        '''When the execution starts'''
        pygame.init()
        pygame.display.set_caption(self.title)

    def on_event(self, event, *args, **kwargs):
        try:
            self.event_handlers[event.type](*args, **kwargs)
        except KeyError, e:
            raise NoEventHandlerError(event.type)

    @abstractmethod
    def on_loop(self, *args, **kwargs):
        '''Logic to be executed in every iteration of the game loop'''
        pass

    @abstractmethod
    def render(self, *args, **kwargs):
        '''Renders the changes reflected in the logic'''
        pass

    def delay(self):
        '''Delays the start of the next loop'''
        time.sleep(self.delay_time)

    def cleanup(self):
        '''When the game loop breaks'''
        pygame.quit()

    def execute(self):
        if not self.on_init():
            self.running = False

        while self.running:
            pygame.event.pump()
            self.on_loop()
            self.render()
            self.delay()

        self.cleanup()

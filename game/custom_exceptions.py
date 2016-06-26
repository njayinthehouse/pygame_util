from exceptions import Exception

class NoEventHandlerError(Exception):

    def __init__(self, event_type):
        super(NoEventHandlerError, self).__init__('Event of type {0} has no handler.'.format(event_type))

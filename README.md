# pygame_util
A few modules for pygame-based apps.

1. game.py defines an abstract class PygameApp, which can act as the parent class of such apps to form a basic structure for a pygame app. To add event handlers to a subclass, just code the handlers in metaclass `EventHandlerMethods`, with decorator event_tag used to map an event to a handler. To use the superclass' event handlers while defining your own, inherit your metaclass EventHandlerMethods from the parent class' metaclass, and call the parent class' constructor in your subclass' constructor.

        class MyPygameApp(PygameApp):
    
            # inherits from outer class' parent class' metaclass to use the parent's event handlers
            class EventHandlerMethods(PygameApp.EventHandlerMethods):
                
                @event_tag(<some event>)
                def on_some_event(self, *args, **kwargs):
                    # handle <some event>
                    
            def __init__(self, *args, **kwargs):
                super(MyPygameApp, self).__init__(*args, **kwargs)
                # init code
                
        
        

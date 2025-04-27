from jjsystem.common import subsystem
from jjsystem.subsystem.timeline_event \
    import resource, controller, manager


subsystem = subsystem.Subsystem(resource=resource.TimelineEvent,
                                controller=controller.Controller,
                                manager=manager.Manager)

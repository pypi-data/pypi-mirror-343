from jjsystem.common import subsystem
from jjsystem.subsystem.route import resource, manager


subsystem = subsystem.Subsystem(resource=resource.Route,
                                manager=manager.Manager)

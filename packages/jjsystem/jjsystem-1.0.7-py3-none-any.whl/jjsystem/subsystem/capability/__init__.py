from jjsystem.common import subsystem
from jjsystem.subsystem.capability import resource, manager


subsystem = subsystem.Subsystem(resource=resource.Capability,
                                manager=manager.Manager)

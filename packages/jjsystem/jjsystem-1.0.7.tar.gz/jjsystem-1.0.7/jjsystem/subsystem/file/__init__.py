from jjsystem.common import subsystem
from jjsystem.subsystem.file import resource
from jjsystem.subsystem.file import manager
from jjsystem.subsystem.file import controller

subsystem = subsystem.Subsystem(resource=resource.File,
                                manager=manager.Manager,
                                controller=controller.Controller)

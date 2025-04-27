from jjsystem.common import subsystem
from jjsystem.subsystem.application import resource, manager, controller, \
    router

subsystem = subsystem.Subsystem(resource=resource.Application,
                                manager=manager.Manager,
                                controller=controller.Controller,
                                router=router.Router)

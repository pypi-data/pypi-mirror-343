from jjsystem.common import subsystem
from jjsystem.subsystem.functionality \
    import manager, resource, controller, router

subsystem = subsystem.Subsystem(resource=resource.Functionality,
                                controller=controller.Controller,
                                manager=manager.Manager,
                                router=router.Router)

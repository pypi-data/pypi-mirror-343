from jjsystem.common import subsystem
from jjsystem.subsystem.token import manager
from jjsystem.subsystem.token import resource
from jjsystem.subsystem.token import router
from jjsystem.subsystem.token import controller

subsystem = subsystem.Subsystem(resource=resource.Token,
                                manager=manager.Manager,
                                router=router.Router,
                                controller=controller.Controller)

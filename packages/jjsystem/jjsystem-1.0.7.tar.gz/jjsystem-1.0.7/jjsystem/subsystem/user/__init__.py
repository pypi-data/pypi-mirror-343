from jjsystem.common import subsystem
from jjsystem.subsystem.user import resource

from jjsystem.subsystem.user import controller
from jjsystem.subsystem.user import manager
from jjsystem.subsystem.user import router


subsystem = subsystem.Subsystem(resource=resource.User,
                                router=router.Router,
                                controller=controller.Controller,
                                manager=manager.Manager)

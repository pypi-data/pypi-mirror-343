from jjsystem.common import subsystem
from jjsystem.common.subsystem import controller
from jjsystem.subsystem.project_cost \
    import resource, manager

subsystem = subsystem.Subsystem(resource=resource.ProjectCost,
                                manager=manager.Manager,
                                controller=controller.Controller)

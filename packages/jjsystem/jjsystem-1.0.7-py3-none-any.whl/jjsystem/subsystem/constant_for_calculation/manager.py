from jjsystem.common.subsystem import operation, manager
from jjsystem.subsystem.constant_for_calculation.resource \
    import ConstantForCalculation
from jjsystem.subsystem.application.resource import Application


class List(operation.List):

    def do(self, session, **kwargs):
        query = session.query(ConstantForCalculation). \
            join(Application, Application.id == # noqa
                 ConstantForCalculation.application_id)
        query = query.distinct()
        dict_compare = {"application.": Application}
        kwargs['query'] = query
        kwargs['dict_compare'] = dict_compare
        return super().do(session=session, **kwargs)


class Manager(manager.Manager):

    def __init__(self, driver):
        super(Manager, self).__init__(driver)
        self.list = List(self)

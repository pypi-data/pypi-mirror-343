from jjsystem.common import exception
from jjsystem.common.subsystem import operation, manager
from jjsystem.common.subsystem.pagination import Pagination
from jjsystem.subsystem.functionality.resource \
    import Functionality, FunctionalityRoute
from jjsystem.subsystem.route.resource \
    import Route
from sqlalchemy import func, or_


class Create(operation.Create):

    def _get_domain_default(self):
        domains = self.manager.api.domains().list(name='default')
        if len(domains) > 0:
            return domains[0]
        else:
            raise exception.NotFound('Default domain not found.')

    def _validar_name(self, name):
        if self.manager.verify_if_exists(name=name):
            raise exception.BadRequest(
                'There is already a functionality with this name.')

    def pre(self, session, **kwargs):
        name = kwargs.get('name', None)
        self._validar_name(name)
        domain = self._get_domain_default()
        domain_id = domain.id
        kwargs['code'] = self.manager.api.domain_sequences().\
            get_nextval(id=domain_id, name=Functionality.CODE_SEQUENCE)
        return super().pre(session, **kwargs)


class AddRoutes(operation.Update):

    def do(self, session, **kwargs):
        routes = kwargs.pop("routes", [])
        route_ids = [r.get('route_id', None) for r in routes]
        entity = self.entity.add_routes(route_ids)
        super().do(session=session)
        return entity


class RmRoutes(operation.Update):

    def do(self, session, **kwargs):
        routes = kwargs.pop("routes", [])
        route_ids = [r.get('route_id', None) for r in routes]
        entity = self.entity.rm_routes(route_ids)
        super().do(session=session)
        return entity


class GetAvailableRoutes(operation.List):

    def do(self, session, **kwargs):
        # remove from kwargs to not be passed in the apply filters function
        id = kwargs.pop("id", None)
        query = session.query(Route). \
            join(FunctionalityRoute,
                 FunctionalityRoute.route_id == Route.id,
                 isouter=True). \
            join(Functionality,
                 FunctionalityRoute.functionality_id == Functionality.id,
                 isouter=True)\
            .filter(or_(Functionality.id != id,
                        Functionality.id == None))\
            .filter(Route.sysadmin == False)  # noqa
        query = self.manager.apply_filters(query, Route, **kwargs)
        query = query.distinct()

        dict_compare = {}
        query = self.manager.apply_filters_includes(
            query, dict_compare, **kwargs)
        query = query.distinct()

        total_rows = None
        if self.manager.with_pagination(**kwargs):
            total_rows = query.count()

        pagination = Pagination.get_pagination(Route, **kwargs)
        if pagination.order_by is not None:
            pagination.adjust_order_by(Route)
        query = self.driver.apply_pagination(query, pagination)
        result = query.all()

        return (result, total_rows)


class GetSelectedRoutes(operation.Get):

    def do(self, session, **kwargs):
        # remove from kwargs to not be passed in the apply filters function
        id = kwargs.pop("id", None)
        query = session.query(Route). \
            join(FunctionalityRoute,
                 FunctionalityRoute.route_id == Route.id). \
            join(Functionality,
                 FunctionalityRoute.functionality_id == Functionality.id)\
            .filter(Functionality.id == id)\
            .filter(Route.sysadmin == False)  # noqa
        query = self.manager.apply_filters(query, Route, **kwargs)
        query = query.distinct()

        dict_compare = {}
        query = self.manager.apply_filters_includes(
            query, dict_compare, **kwargs)
        query = query.distinct()

        total_rows = None
        if self.manager.with_pagination(**kwargs):
            total_rows = query.count()

        pagination = Pagination.get_pagination(Route, **kwargs)
        if pagination.order_by is not None:
            pagination.adjust_order_by(Route)
        query = self.driver.apply_pagination(query, pagination)
        result = query.all()

        return (result, total_rows)


class VerifyIfExists(operation.List):

    def do(self, session, **kwargs):
        normalize = func.jjsystem_normalize
        name = kwargs.pop('name', None)
        if name is None:
            raise exception.BadRequest('Name is required.')
        query = session.query(Functionality). \
            filter(normalize(getattr(Functionality, 'name'))
                   .ilike(normalize(name))).\
            distinct()
        result = query.all()

        if len(result) > 0:
            return True
        else:
            return False


class Manager(manager.Manager):

    def __init__(self, driver):
        super(Manager, self).__init__(driver)
        self.create = Create(self)
        self.add_routes = AddRoutes(self)
        self.rm_routes = RmRoutes(self)
        self.get_available_routes = GetAvailableRoutes(self)
        self.get_selected_routes = GetSelectedRoutes(self)
        self.verify_if_exists = VerifyIfExists(self)

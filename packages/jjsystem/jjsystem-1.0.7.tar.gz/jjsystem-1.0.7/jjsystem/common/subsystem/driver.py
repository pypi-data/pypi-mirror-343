import uuid
from jjsystem.common.subsystem.pagination import Pagination
from jjsystem.common.subsystem.entity import DATE_FMT
from datetime import datetime as datetime1
import datetime as datetime2
from typing import Any, Type

from jjsystem.common import exception
from sqlalchemy import func, or_, and_
from sqlalchemy.orm import exc
from sqlalchemy.sql import text

from jjsystem.common.subsystem.transaction_manager import TransactionManager


class Driver(object):

    def __init__(self, resource: Type[Any],
                 transaction_manager: TransactionManager) -> None:
        self.resource = resource
        self.transaction_manager = transaction_manager

    def removeId(self, entity_aux):
        new_id = uuid.uuid4().hex

        if entity_aux.get('id') is not None:
            new_id = entity_aux.pop('id')

        return new_id

    def instantiate(self, **kwargs):
        try:
            embedded = {}
            for attr in self.resource.embedded():
                if attr not in kwargs:
                    raise Exception(
                        f'O campo embedded {attr} é obrigatório em ' +
                        f'{self.resource.__name__}.')
                embedded.update({attr: kwargs.pop(attr)})

            instance = self.resource(**kwargs)

            for attr in embedded:
                value = embedded[attr]
                var = getattr(self.resource, attr)
                # TODO(samueldmq): is this good enough? should we discover it?
                mapped_attr = {self.resource.individual() + '_id': instance.id}
                if isinstance(value, list):
                    setattr(instance, attr, [var.property.mapper.class_(
                        id=self.removeId(ref), **dict(ref, **mapped_attr))
                        for ref in value])
                else:
                    # TODO(samueldmq): id is inserted here. it is in the
                    # manager for the entities. do it all in the resource
                    # contructor
                    setattr(instance, attr, var.property.mapper.class_(
                        id=uuid.uuid4().hex, **dict(value, **mapped_attr)))
        except Exception as exec:
            # TODO(samueldmq): replace with specific exception
            message = ''.join(exec.args)
            raise exception.BadRequest(message)

        return instance

    def create(self, entity, session):
        if not entity.is_stable():
            raise exception.PreconditionFailed()
        session.add(entity)
        session.flush()

    def update(self, entity, data, session):
        # try:
        #     entity = self.get(id, session)
        # except exc.NoResultFound:
        #     raise exception.NotFound()

        for attr in self.resource.embedded():
            if attr in data:
                value = data.pop(attr)
                var = getattr(self.resource, attr)
                # TODO(samueldmq): is this good enough? should we discover it?
                mapped_attr = {self.resource.individual() + '_id': id}
                if isinstance(value, list):
                    setattr(entity, attr, [var.property.mapper.class_(
                        id=self.removeId(ref), **dict(ref, **mapped_attr))
                        for ref in value])
                else:
                    # TODO(samueldmq): id is inserted here. it is in the
                    # manager for the entities. do it all in the resource
                    # contructor
                    setattr(entity, attr, var.property.mapper.class_(
                        id=uuid.uuid4().hex, **dict(value, **mapped_attr)))

        for key, value in data.items():
            if hasattr(entity, key):
                try:
                    setattr(entity, key, value)
                except AttributeError:
                    raise exception.BadRequest(
                        f'Error! The attribute {key} is read only')
            else:
                raise exception.BadRequest(
                    f'Error! The attribute {key} not exists')

        if not entity.is_stable():
            raise exception.PreconditionFailed()
        session.flush()
        return entity

    def delete(self, entity, session):
        session.delete(entity)
        session.flush()

    def get(self, id, session):
        try:
            query = session.query(self.resource).filter_by(id=id)
            result = query.one()
        except exc.NoResultFound:
            raise exception.NotFound()

        return result

    def list(self, session, **kwargs):
        only_first_column = kwargs.pop('only_first_column', False)
        dict_compare = kwargs.pop('dict_compare', None)
        # pega a query ou monta uma
        query = kwargs.pop('query', session.query(self.resource))

        # aplica filtros na classe principal
        query = self.apply_filters(query, self.resource, **kwargs)
        # aplica filtros nas classes dos joins
        query = self.apply_filters_includes(query, dict_compare, **kwargs)
        # aplica filtros de intervalo de tempo em colunas date ou datetime
        query = self.apply_filter_multiple_de_ate_with_timezone(
            query=query, resource=self.resource, **kwargs)
        # aplica order_by se "order_by" tiver sido passado
        query = self.apply_order_by(query, **kwargs)
        # aplica paginação se "page" e "page_size" tiver sido passado
        query = self.apply_pagination(query, **kwargs)

        result = query.all()

        if only_first_column:
            result = list(map(lambda x: x[0], result))

        return result

    def count(self, session, **kwargs):
        try:
            # TODO(JogeSilva): improve filtering so as not to ignore parameters
            # that are attributes of an entity to include
            # pega a query ou monta uma
            query = kwargs.pop('query', session.query(self.resource.id))
            rows = self.apply_filters(query, self.resource, **kwargs).count()
            result = rows
        except exc.NoResultFound:
            raise exception.NotFound()

        return result

    def activate_or_deactivate_multiple_entities(self, session, **kwargs):
        active = kwargs.pop('active', None)

        entities = self.list_multiple_selection(session, **kwargs)
        key = 'active'

        for entity in entities:
            if hasattr(entity, key):
                setattr(entity, key, active)
            else:
                raise exception.BadRequest(
                    f'Error! The attribute {key} not exists.')

            if not entity.is_stable():
                raise exception.PreconditionFailed()
        session.flush()
        return entities

    def list_multiple_selection(self, session, **kwargs):
        '''
            fields that can be passed in kwargs:

            dict_compare
            resource
            query

            the possibility of passing these fields as parameters makes
            the function generic.
        '''

        dict_compare = kwargs.pop('dict_compare', {})
        query_in_kwargs = False
        multiple_selection = kwargs.get('multiple_selection', None)
        if multiple_selection is None:
            raise exception.BadRequest('multiple_selection is required.')

        resource_filtro = self.resource
        resource = kwargs.pop('resource', None)
        if resource is not None:
            resource_filtro = resource

        if 'query' in kwargs.keys():
            query = kwargs.pop('query', None)
            query_in_kwargs = True
        else:
            query = session.query(resource_filtro)

        selected_list = multiple_selection.get('selected_list', [])
        unselected_list = multiple_selection.get('unselected_list', [])

        if len(selected_list) > 0:
            query = query.filter(resource_filtro.id.in_(selected_list))
        else:
            if len(unselected_list) > 0:
                query = query.filter(resource_filtro.id.not_in(
                    unselected_list))
            query = self.apply_filters(query, resource_filtro, **kwargs)
            query = self.apply_filters_includes(query, dict_compare, **kwargs)
            query = self.apply_filter_multiple_de_ate_with_timezone(
                query=query, resource=self.resource, **kwargs)

        query = query.distinct()
        result = query.all()

        if query_in_kwargs is True:
            result = list(map(lambda x: x[0], result))

        return result

    def apply_filters(self, query, resource, **kwargs):
        for k, v in kwargs.items():
            if hasattr(resource, k):
                if k == 'tag':
                    values = v
                    if len(v) > 0 and v[0] == '#':
                        values = v[1:]
                    values = values.split(',')
                    filter_tags = []
                    for value in values:
                        filter_tags.append(
                            getattr(resource, k)
                            .like('%#' + str(value) + ' %'))
                    query = query.filter(or_(*filter_tags))
                elif isinstance(v, str) and '%' in v:
                    normalize = func.jjsystem_normalize
                    query = query.filter(normalize(getattr(resource, k))
                                         .ilike(normalize(v)))
                else:
                    query = query.filter(getattr(resource, k) == v)

        return query

    def apply_order_by(self, query, **kwargs):
        tablename = f'"{self.resource.__tablename__}"'
        order_by_default = f'{tablename}.id'
        order_by = kwargs.get('order_by', None)
        # se não tiver sido passado um order_by,
        # irá usar o order_by default
        if order_by is None:
            query = query.order_by(text(order_by_default))
        else:
            # se foi passado um order_by ai iremos normalizar ele
            order_by_splited = order_by.split(',')
            order_by_final = ''
            for item in order_by_splited:
                if '.' not in item:
                    order_by_final += f'{tablename}.{item},'
                else:
                    order_by_final += f'{item},'

            query = query.order_by(text(order_by_final[:-1]))
        return query

    def apply_pagination(self, query, **kwargs):
        page_size = int(kwargs.get('page_size', 9999999))
        page = int(kwargs.get('page', 0))

        query = query.limit(page_size)
        query = query.offset(page * page_size)

        return query

    def apply_filters_includes(self, query, dict_compare, **kwargs):
        if type(dict_compare) is not dict:
            return query
        for id, resource in dict_compare.items():
            for k, v in kwargs.items():
                if id in k and hasattr(resource, k.split('.')[-1]):
                    k = k.split('.')[-1]
                    isinstance_aux = isinstance(v, str)

                    if k == 'tag':
                        # TODO(JorgeSilva): definir o caractere para split
                        values = v
                        if len(v) > 0 and v[0] == '#':
                            values = v[1:]
                        values = values.split(',')
                        filter_tags = []
                        for value in values:
                            filter_tags.append(
                                getattr(resource, k)
                                .like('%#' + str(value) + ' %'))
                        query = query.filter(or_(*filter_tags))
                    elif isinstance_aux and self.__isdate(v):
                        day, next_day = self.__get_day_and_next_day(v)
                        query = query.filter(
                            and_(
                                or_(getattr(resource, k) < next_day,
                                    getattr(resource, k) == None),  # noqa
                                or_(getattr(resource, k) >= day,
                                    getattr(resource, k) == None)))  # noqa
                    elif isinstance_aux and '%' in v:
                        normalize = func.jjsystem_normalize
                        query = query.filter(normalize
                                             (getattr(resource, k))
                                             .ilike(normalize(v)))
                    else:
                        query = query.filter(getattr(resource, k) == v)

        return query

    def with_pagination(self, **kwargs):
        require_pagination = kwargs.get('require_pagination', False)
        page = kwargs.get('page', None)
        page_size = kwargs.get('page_size', None)

        if (page and page_size is not None) and require_pagination is True:
            return True
        return False

    def __isdate(self, data, format="%Y-%m-%d"):
        res = True
        try:
            res = bool(datetime1.strptime(data, format))
        except ValueError:
            res = False
        return res

    def __get_day_and_next_day(self, data, format="%Y-%m-%d"):
        day = datetime1.strptime(data, format)
        next_day = day + datetime2.timedelta(days=1)
        return (day, next_day)

    def _convert_de_ate(self, **kwargs):
        de = kwargs.get('de', None)
        ate = kwargs.get('ate', None)
        inicio = None
        fim = None

        if de and ate:
            try:
                inicio = datetime1.strptime(de.replace(' ', '+'), '%Y-%m-%d%z')
                fim = datetime1.strptime(ate.replace(' ', '+'), '%Y-%m-%d%z') \
                    + datetime2.timedelta(days=1)

            except Exception:
                inicio = datetime1.strptime(de, DATE_FMT)
                fim = datetime1.strptime(ate, DATE_FMT) +\
                    datetime2.timedelta(days=1)

        return (inicio, fim)

    # função criada para filtrar na listagem de uma entidade mais
    # de um campo do tipo Date ou DateTime
    def apply_filter_multiple_de_ate_with_timezone(
            self, query, resource, **kwargs):
        attributes_filter = kwargs.get('attributes_filter', '')
        attributes_filter = attributes_filter.split(',')
        de_filter = kwargs.get('de_filter', '')
        de_filter = de_filter.split(',')
        ate_filter = kwargs.get('ate_filter', '')
        ate_filter = ate_filter.split(',')

        tamanho = len(attributes_filter)

        if not (tamanho == len(de_filter) and tamanho == len(ate_filter)):
            return query

        for i in range(tamanho):
            attribute = attributes_filter[i]
            data = {
                'de': de_filter[i],
                'ate': ate_filter[i]
            }
            (de, ate) = self._convert_de_ate(**data)
            if de and ate:
                if hasattr(resource, attribute):
                    query = query.filter(
                        and_(getattr(resource, attribute) >= de,
                             getattr(resource, attribute) < ate))
        return query

    def adjust_dinamic_order_by(self, resource: Type[Any]):
        if self.order_by is not None:
            order_by_ajusted = ''
            table_name = resource.__tablename__
            order_by_post_split = self.order_by.split(',')
            for item in order_by_post_split:
                if '.' in item:
                    order_by_ajusted += f'{item},'
                else:
                    order_by_ajusted += f'{table_name}.{item},'

            self.order_by = order_by_ajusted[:-1]

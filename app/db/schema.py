from enum import Enum, unique

from sqlalchemy import (
    Column, Enum as MariaEnum, Integer, Float,
    TIMESTAMP, Boolean, MetaData, String, Table,
)


convention = {
    'all_column_names': lambda constraint, table: '_'.join([
        column.name for column in constraint.columns.values()
    ]),
    'ix': 'ix__%(table_name)s__%(all_column_names)s',
    'uq': 'uq__%(table_name)s__%(all_column_names)s',
    'ck': 'ck__%(table_name)s__%(column_0_name)s',
    'fk': 'fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s',
    'pk': 'pk__%(table_name)s'
}

metadata = MetaData(naming_convention=convention)


@unique
class CourierType(Enum):
    foot = 'foot'
    bike = 'bike'
    car = 'car'

    def __repr__(self):
        return "%s" % self._value_

    def __str__(self):
        return "%s" % self._value_


couriers_table = Table(
    'couriers',
    metadata,
    Column('courier_id', Integer, primary_key=True),
    Column('courier_type', MariaEnum(CourierType, name='courier_type'), nullable=False),
)

orders_table = Table(
    'orders',
    metadata,
    Column('order_id', Integer, primary_key=True),
    Column('weight', Float, nullable=False),
    Column('region_id', Integer, nullable=False),
    Column('is_ready', Boolean, nullable=False, default=0),
    Column('complete_time', TIMESTAMP, nullable=True),
    Column('assign_id', Integer, nullable=True, default=-1),
)

regions_table = Table(
    'regions',
    metadata,
    Column('region_id', Integer, primary_key=True),
    Column('region_name', String(50), nullable=True),
)

courier_to_region_table = Table(
    'courier_to_region',
    metadata,
    Column('courier_id', Integer, primary_key=True),
    Column('region_id', Integer, primary_key=True),
)

orders_assign_table = Table(
    'orders_assign',
    metadata,
    Column('assign_id', Integer, primary_key=True, autoincrement=True),
    Column('courier_id', Integer, nullable=False),
    Column('assign_time', TIMESTAMP, nullable=True),
)

working_bands_table = Table(
    'working_bands',
    metadata,
    Column('band_id', Integer, primary_key=True, autoincrement=True),
    Column('courier_id', Integer, nullable=False),
    Column('start', String(20), nullable=False),
    Column('end', String(20), nullable=False),
)

delivery_bands_table = Table(
    'delivery_bands',
    metadata,
    Column('band_id', Integer, primary_key=True, autoincrement=True),
    Column('order_id', Integer, nullable=False),
    Column('start', String(20), nullable=False),
    Column('end', String(20), nullable=False),
)

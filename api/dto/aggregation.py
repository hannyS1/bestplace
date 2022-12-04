from fastapi.utils import Enum
from typing import List

from pydantic import BaseModel, validator, PositiveInt, PositiveFloat


class FieldEnum(str, Enum):
    apartments = "apartments"
    price = "price"
    year = "year"


class AggregationEnum(str, Enum):
    sum = "sum"
    avg = "avg"
    min = "min"
    max = "max"


class GeometryTypeEnum(str, Enum):
    point = "Point"
    polygon = "Polygon"


class GeometryPointDto(BaseModel):
    type: GeometryTypeEnum = GeometryTypeEnum.point
    coordinates: List[PositiveFloat]

    class ErrorMessages:
        INVALID_COORDINATES_TUPLE_LENGTH = "Length of coordinates tuple must be equal 2"
        INVALID_GEOMETRY_TYPE = "Geometry type must be Point"

    @validator("coordinates")
    def validate_coordinates(cls, value: List[float]):
        if len(value) != 2:
            raise ValueError(cls.ErrorMessages.INVALID_COORDINATES_TUPLE_LENGTH)
        return value

    @validator("type")
    def validate_type(cls, value: GeometryTypeEnum):
        if value != GeometryTypeEnum.point:
            raise ValueError(cls.ErrorMessages.INVALID_GEOMETRY_TYPE)
        return value


class GeometryPolygonDto(BaseModel):
    type: GeometryTypeEnum = GeometryTypeEnum.polygon
    coordinates: List[List[List[PositiveFloat]]]

    class ErrorMessages:
        INVALID_COORDINATES_TUPLE_LENGTH = "Length of coordinates tuple must be equal 2"
        INVALID_COORDINATES_LENGTH = "List of coordinates must be grater than 0"
        INVALID_GEOMETRY_TYPE = "Geometry type must be Polygon"

    @validator("coordinates")
    def validate_coordinates(cls, value: List[List[List[PositiveFloat]]]):
        if len(value) < 1:
            raise ValueError(cls.ErrorMessages.INVALID_COORDINATES_LENGTH)

        for nested in value:
            for coordinates in nested:
                if len(coordinates) != 2:
                    raise ValueError(cls.ErrorMessages.INVALID_COORDINATES_TUPLE_LENGTH)

        return value

    @validator("type")
    def validate_type(cls, value: GeometryTypeEnum):
        if value != GeometryTypeEnum.polygon:
            raise ValueError(cls.ErrorMessages.INVALID_GEOMETRY_TYPE)
        return value


class AggregationBaseDto(BaseModel):
    field: FieldEnum
    aggr: AggregationEnum


class AggregationRadiusDto(AggregationBaseDto):
    geometry: GeometryPointDto
    r: PositiveInt


class AggregationPolygonDto(AggregationBaseDto):
    geometry: GeometryPolygonDto


class AggregationResponseDto(BaseModel):
    value: float

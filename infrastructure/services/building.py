import h3
from fastapi import HTTPException
from pythondi import inject
from sqlalchemy.sql import func
from starlette import status

from core.entities import ApartmentBuilding
from core.interfaces.repository.building import IBuildingRepository
from core.interfaces.services.building import IBuildingService
from core.utils.h3 import H3Constants
from infrastructure.specifications.building import DefaultBuildingSpecification


class BuildingService(IBuildingService):

    field_mapping = {
        "apartments": ApartmentBuilding.apartments_count,
        "price": ApartmentBuilding.price,
        "year": ApartmentBuilding.year,
    }

    aggr_mapping = {
        "min": func.min,
        "max": func.max,
        "avg": func.avg,
        "sum": func.sum
    }

    class ErrorMessages:
        FIELD_NOT_SUPPORTED = "Аггрегация по полю {} не поддерживается"
        AGGREGATION_NOT_SUPPORTED = "Аггрегация {} не поддерживается"

    @inject()
    def __init__(self, repository: IBuildingRepository):
        self.repository = repository

    def __get_field_obj(self, field: str):
        field_obj = self.field_mapping.get(field)
        if not field_obj:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=self.ErrorMessages.FIELD_NOT_SUPPORTED.format(field)
            )
        return field_obj

    def __get_aggregation_function(self, aggr_type: str):
        aggr_function = self.aggr_mapping.get(aggr_type)
        if not aggr_function:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=self.ErrorMessages.AGGREGATION_NOT_SUPPORTED.format(aggr_type)
            )
        return aggr_function

    def aggregate_radius(
            self, field: str, aggr_type: str,
            radius: int, longitude: float, latitude: float
    ) -> float:
        field_obj = self.__get_field_obj(field)
        aggr_function = self.__get_aggregation_function(aggr_type)

        h3_value = h3.geo_to_h3(latitude, longitude, resolution=H3Constants.RESOLUTION)
        search_h3_values = list(h3.k_ring(h3_value, radius))

        specification = DefaultBuildingSpecification(
            ApartmentBuilding.h3_value.in_(search_h3_values)
        )

        return self.repository.aggregate(aggr_function, field_obj, specification)

    def aggregate_polygon(
        self, field: str, aggr_type: str, geometry: dict,
    ) -> float:
        field_obj = self.__get_field_obj(field)
        aggr_function = self.__get_aggregation_function(aggr_type)

        search_h3_values = list(h3.polyfill(
            geometry, res=H3Constants.RESOLUTION, geo_json_conformant=True,
        ))

        specification = DefaultBuildingSpecification(
            ApartmentBuilding.h3_value.in_(search_h3_values)
        )

        return self.repository.aggregate(aggr_function, field_obj, specification)


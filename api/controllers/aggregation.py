from fastapi import APIRouter
from pythondi import inject

from api.dto.aggregation import AggregationRadiusDto, AggregationPolygonDto, AggregationResponseDto
from core.interfaces.services.building import IBuildingService

aggregation_controller = APIRouter(prefix='/api/aggregation')


class UseCase:
    @inject()
    def __init__(self, building_service: IBuildingService):
        self.building_service = building_service


@aggregation_controller.post("/radius", response_model=AggregationResponseDto)
async def aggregate_radius(dto: AggregationRadiusDto) -> AggregationResponseDto:
    use_case = UseCase()
    result = use_case.building_service.aggregate_radius(
        field=dto.field,
        aggr_type=dto.aggr,
        radius=dto.r,
        longitude=dto.geometry.coordinates[0],
        latitude=dto.geometry.coordinates[1],
    )
    return AggregationResponseDto(value=result)


@aggregation_controller.post("/polygon", response_model=AggregationResponseDto)
async def aggregate_polygon(dto: AggregationPolygonDto) -> AggregationResponseDto:
    use_case = UseCase()
    result = use_case.building_service.aggregate_polygon(
        field=dto.field,
        aggr_type=dto.aggr,
        geometry=dict(dto.geometry),
    )
    return AggregationResponseDto(value=result)

from abc import ABC


class IBuildingService(ABC):
    def aggregate_radius(
            self, field: str, aggr_type: str,
            radius: int, longitude: float, latitude: float
    ) -> float:
        raise NotImplementedError()

    def aggregate_polygon(
        self, field: str, aggr_type: str,
        geometry: dict
    ) -> float:
        raise NotImplementedError()

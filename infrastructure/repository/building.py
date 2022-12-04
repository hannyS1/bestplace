from typing import Callable, Optional, Any

from core.entities import ApartmentBuilding
from core.interfaces.repository.building import IBuildingRepository
from core.interfaces.specifications.ispecification import ISpecification
from infrastructure.repository.base import BaseRepository


class BuildingRepository(BaseRepository[ApartmentBuilding], IBuildingRepository):
    def aggregate(
            self, aggregate_func: Callable,
            aggregate_field: Any,
            specification: Optional[ISpecification] = None,
    ) -> float:
        query = self.db.query(aggregate_func(aggregate_field))
        if specification:
            query = query.filter(specification.get_criteria())
        result = query.all()
        return float(result[0][0]) if result[0][0] is not None else 0

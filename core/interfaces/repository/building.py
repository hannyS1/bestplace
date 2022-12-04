from abc import ABC

from typing import Optional, Callable, Any

from core.entities.building import ApartmentBuilding
from core.interfaces.repository.base import IBaseRepository
from core.interfaces.specifications.ispecification import ISpecification


class IBuildingRepository(ABC, IBaseRepository[ApartmentBuilding]):
    def aggregate(
            self, aggregate_func: Callable,
            aggregate_field: Any,
            specification: Optional[ISpecification] = None,
    ) -> float:
        raise NotImplementedError()

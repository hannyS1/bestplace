from pythondi import Provider, configure

from core.interfaces.repository.building import IBuildingRepository
from core.interfaces.services.building import IBuildingService
from infrastructure.repository.building import BuildingRepository
from infrastructure.services.building import BuildingService


def configure_dependencies():

    provider = Provider()

    configure(provider)

    provider.bind(IBuildingRepository, BuildingRepository)
    provider.bind(IBuildingService, BuildingService)

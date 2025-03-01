from api.services.interface.marketServiceInterface import MarketServiceInterface
from api.repositories.interface.marketRepositoryInterface import MarketRepositoryInterface
from api.models.market import Market
from api.dto.market_dto import MarketDTO
from typing import List, Optional

class MarketService(MarketServiceInterface):
  def __init__(self, market_repository: MarketRepositoryInterface):
    self.market_repository = market_repository

  def get_by_id(self, market_id: int) -> Optional[MarketDTO]:
    market = self.market_repository.get_by_id(market_id)
    return MarketDTO.from_model(market) if market else None

  def all(self) -> List[MarketDTO]:
    markets = self.market_repository.all()
    return [MarketDTO.from_model(market) for market in markets]

  def add(self, market_dto: MarketDTO) -> MarketDTO:
    market = Market(name=market_dto.name)
    added_market = self.market_repository.add(market)
    return MarketDTO.from_model(added_market)

  def update(self, market_dto: MarketDTO) -> MarketDTO:
    market = Market(id=market_dto.id, name=market_dto.name)
    updated_market = self.market_repository.update(market)
    return MarketDTO.from_model(updated_market)

  def delete(self, market_dto: MarketDTO) -> bool:
    try:
      market = Market.objects.get(id=market_dto.id)
    except Market.DoesNotExist:
      return False
    return self.market_repository.delete(market)


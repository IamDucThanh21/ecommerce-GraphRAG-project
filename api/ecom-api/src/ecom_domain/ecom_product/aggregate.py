from fluvius.domain.aggregate import Aggregate, action

class ECOMProductAggregate(Aggregate):
    ## this is firt aggregate
    async def create_product(self, name: str, price: float):
        self._state.name = name
        self._state.price = price
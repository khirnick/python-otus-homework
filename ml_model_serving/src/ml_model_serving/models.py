from copy import deepcopy
import random

from pydantic import Field
from pydantic.dataclasses import dataclass


@dataclass(frozen=True)
class Model:

    name: str = Field(min_length=3, max_length=20)
    features: list[float] = Field(default_factory=list)

    def predict(self, new: list[float]) -> float:
        self.features.extend(new)
        return random.choice(self.features)

models: dict[str, Model] = {}


def initialize_models() -> None:
    model_x = Model(name='model_x', features=[1.3, 5.3, 3.3])
    model_y = Model(name='model_y', features=[4.2, 7.2, 6.9])
    model_z = Model(name='model_z', features=[1.4, 3.1, 10.3])
    models[model_x.name] = model_x
    models[model_y.name] = model_y
    models[model_z.name] = model_z

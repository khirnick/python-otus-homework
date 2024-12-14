from typing import Annotated
from fastapi.exceptions import HTTPException
from fastapi.params import Depends, Path
from pydantic.dataclasses import dataclass

from ml_model_serving.handlers.login import get_current_active_user, User
from ml_model_serving.models import models


@dataclass(frozen=True)
class Features:

    features: list[float]


def model_inference(
    model_name: Annotated[str, Path(title='ML Model Name', min_length=3, max_length=20)],
    features: Features,
    current_user: Annotated[User, Depends(get_current_active_user)]
) -> dict[str, float]:
    if model_name not in models:
        raise HTTPException(status_code=404, detail=f'Model {model_name} not found')
    prediction = models[model_name].predict(features.features)
    return {'prediction': prediction}

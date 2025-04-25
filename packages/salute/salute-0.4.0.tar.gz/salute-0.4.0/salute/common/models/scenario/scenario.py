from pydantic import BaseModel
from common.models.scenario.scenario_app import ScenarioApp, SessionStore
from common.models.scenario.utils import ScenarioInfo


class Scenario(BaseModel):
    app: ScenarioApp
    info: ScenarioInfo
    session_store: SessionStore

    class Config:
        arbitrary_types_allowed = True

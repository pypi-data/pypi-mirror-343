from pathlib import Path

from decouple import config
from sanic import Sanic
from scenarios.vovka.scenario import VovkaScenario


async def scenario_connector(path: Path) -> None:
    app = Sanic.get_app(config("NAME"))
    vovka_scenario = VovkaScenario(path=path)
    await vovka_scenario.set_storage()

    app.update_config({"SCENARIOS": {vovka_scenario.info.key: vovka_scenario}})

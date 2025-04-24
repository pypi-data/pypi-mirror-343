import random
from string import Template

from sanic.logging.loggers import logger

from common.utils.load_data import load_data
from common.models.request_message import RequestMessage
from common.models.scenario.scenario_app import ScenarioApp
from scenarios.vovka.session import (
    VovkaQuestion,
    VovkaPhrase,
    VovkaScenarioPayload,
)
from scenarios.vovka.walking import Walking


class VovkaScenario(ScenarioApp):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        logger.info("Initializing Vovka Scenario")
        self.phrases: dict[str, VovkaPhrase] = dict()
        logger.info(f"Loading phrases from {self.static_dir}")
        self.set_phrases_list()
        logger.info(f"Install {len(self.phrases)} phrases")
        self.questions: list[VovkaQuestion] = []
        logger.info(f"Loading questions from {self.static_dir}")
        self.set_question_list()
        logger.info(f"Install {len(self.questions)} questions")

        self.info.payload = VovkaScenarioPayload(**self.info.payload)

        self.app = self

    def __repr__(self) -> str:
        return str(self.app.info)

    def set_phrases_list(self) -> None:
        phrases = load_data(self.static_dir / "phrases.json")

        for phrase_key in phrases:
            self.phrases.update(
                {
                    phrase_key: VovkaPhrase(
                        message=Template(phrases[phrase_key])
                    )
                }
            )

    def set_question_list(self) -> None:
        questions = load_data(self.static_dir / "questions.json")

        for question in questions:
            self.questions.append(VovkaQuestion(**question))

    def get_all_questions(
        self, with_shuffle: bool = True
    ) -> dict[int, VovkaQuestion]:
        question_map = {}
        if with_shuffle:
            random.shuffle(self.questions)
        for question in self.questions:
            question_map[question.id] = question
        return question_map

    async def process(self, scenario_request: RequestMessage):
        logger.info("Processing Vovka Scenario")
        walk = Walking(
            scenario_request,
            self.phrases,
            self.get_all_questions(),
            self.session_store,
            self.info.payload,
        )
        response = await walk.process()
        logger.info(
            f"Processed Vovka Scenario Response: {response.model_dump(mode='json')}"
        )
        return response

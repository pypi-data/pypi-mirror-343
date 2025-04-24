from enum import Enum
from string import Template

from pydantic import BaseModel
from pydantic.alias_generators import to_camel

from common.models.scenario.utils import ScenarioInfo


class VovkaSessionPayload(BaseModel):
    is_new_game: bool = True
    question: str = None
    score: int = 0
    answer: str = None


class VovkaState(str, Enum):
    RUN_APP = "RUN_APP"
    QUESTION = "QUESTION"


class VovkaStage(str, Enum):
    WELCOME = "WELCOME"
    WAITING = "WAITING"
    CHECK_ANSWER = "CHECK_ANSWER"
    ANSWER_SUCCESS = "ANSWER_SUCCESS"
    ANSWER_FAILURE = "ANSWER_FAILURE"
    REPEAT = "REPEAT"
    HELP = "HELP"
    LOSE = "LOSE"
    WIN = "WIN"
    PROMOTE = "PROMOTE"


class VovkaQuestion(BaseModel):
    id: int
    answers: list
    question: str
    card: str
    card_tts: str = None
    choices: list = []
    is_simple: bool = False
    image_url: str
    image_hash: str

    class Config:
        alias_generator = to_camel

    def get_question_message(self) -> str:
        return self.question

    def get_answer_message(self) -> str:
        message = self.card_tts or self.card
        return message.lower() if message else ""


class VovkaSession(BaseModel):
    is_saved: bool = False
    intent: str = ""
    question_id: int = 0
    questions: list[int] = []
    score: int = 0


class VovkaPhrase(BaseModel):
    message: Template = None

    class Config:
        arbitrary_types_allowed = True

    def get_message(self, **kwargs):
        return self.message.substitute(**kwargs)


class VovkaPhrases:
    items: dict[str, VovkaPhrase]


class VovkaScenarioBackground(BaseModel):
    url: str
    hash: str


class VovkaScenarioVideo(BaseModel):
    title: str
    link: str


class VovkaScenarioConfig(BaseModel):
    wrong: int
    correct: int
    win: int
    lose: int
    video: VovkaScenarioVideo


class VovkaScenarioPayload(BaseModel):
    init_background: VovkaScenarioBackground
    win_background: VovkaScenarioBackground
    config: VovkaScenarioConfig


class VovkaScenarioInfo(ScenarioInfo):
    payload: VovkaScenarioPayload

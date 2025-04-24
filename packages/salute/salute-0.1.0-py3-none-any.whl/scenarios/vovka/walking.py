from common.assets.items import get_bubble, get_card_list, get_suggestion
from common.models.message.name import Name
from common.models.request_message import RequestMessage
from common.models.response_message import ResponseMessage
from sanic.logging.loggers import logger

from common.models.scenario.scenario_app import SessionStore
from scenarios.vovka.session import (
    VovkaPhrase,
    VovkaQuestion,
    VovkaSession,
    VovkaScenarioPayload,
)
from scenarios.vovka.utils.okko_card import get_okko_card

RUN_APP = "run_app"
WELCOME_APP = "welcome_app"
REQUESTED_QUESTION = "requested_question"
PROCESSING_ANSWER = "processing_answer"


class Walking:

    def __init__(
        self,
        request: RequestMessage,
        phrases: dict[str, VovkaPhrase],
        questions: dict[int, VovkaQuestion],
        session_store: SessionStore,
        payload: VovkaScenarioPayload,
    ) -> None:
        self.request: RequestMessage = request
        self.response: ResponseMessage = self._create_base_response()
        self.session: VovkaSession = VovkaSession()
        self.payload: VovkaScenarioPayload = payload
        self.phrases: dict[str, VovkaPhrase] = phrases
        self.questions: dict[int, VovkaQuestion] = questions
        self.question_keys: list[int] = list(questions.keys())

        self.session_store: SessionStore = session_store

    def _create_base_response(self) -> ResponseMessage:
        response = ResponseMessage(**self.request.model_dump(mode="json"))
        response.messageName = Name.ANSWER_TO_USER
        return response

    async def _setup_session(self):
        logger.info("Setting up session")
        raw_session = await self.session_store.get(self.request.get_user_id())
        session: VovkaSession = VovkaSession(
            **raw_session if raw_session else {}
        )
        self.session: VovkaSession = session
        logger.info(f"Session -> {session}")

    def is_win(self) -> bool:
        return self.session.score <= self.payload.config.win

    def is_lose(self) -> bool:
        if self.session.score >= self.payload.config.lose:
            return True
        if not len(self.session.questions):
            return True
        return False

    async def _save_session(self):
        user_id = self.request.get_user_id()
        self.session.is_saved = True
        session_data = self.session.model_dump(mode="json")
        await self.session_store.set(user_id, session_data)

    def add_video_card(self):
        self.response.payload.items.append(
            get_okko_card(
                self.payload.config.video.title, self.payload.config.video.link
            )
        )

    async def lose_stage(self):
        logger.info("Lose stage init")

        lose_message = self.phrases["lose"].get_message()

        self.response.payload.pronounceText += lose_message
        self.response.payload.items.append(get_bubble(lose_message))
        self.add_video_card()

        await self.session_store.drop(self.request.get_user_id())
        return self.response

    async def win_stage(self):
        logger.info("Win stage init")

        win_message = self.phrases["win"].get_message()

        self.response.payload.pronounceText += win_message
        self.response.payload.items.append(get_bubble(win_message))
        self.response.payload.items.append(
            get_card_list(
                self.payload.win_background.url,
                self.payload.win_background.hash,
            )
        )
        self.add_video_card()

        await self.session_store.drop(self.request.get_user_id())
        return self.response

    async def repeat_question(self):
        logger.info("Repeat question stage init")
        question: VovkaQuestion = self.questions[self.session.question_id]

        self.response.payload.pronounceText += question.question
        self.response.payload.suggestions.buttons += get_suggestion(
            question.choices
        )

        self.response.payload.intent = REQUESTED_QUESTION
        logger.info("Repeat question stage complete")
        return self.response

    async def make_question(self):
        logger.info("Make question stage init")
        question_key = self.session.questions.pop()
        question: VovkaQuestion = self.questions[question_key]

        self.response.payload.pronounceText += question.question
        self.response.payload.items.append(get_bubble(question.question))
        self.response.payload.suggestions.buttons += get_suggestion(
            question.choices
        )

        self.response.payload.intent = REQUESTED_QUESTION

        self.session.intent = REQUESTED_QUESTION
        self.session.question_id = question_key
        self.session.questions = self.session.questions

        await self.session_store.set(
            self.request.get_user_id(), self.session.model_dump(mode="json")
        )
        logger.info("Make question stage complete")

    async def welcome_stage(self) -> ResponseMessage:
        logger.info("RUN_APP stage init")
        self.response.payload.intent = REQUESTED_QUESTION
        welcome_message = self.phrases["main"].get_message()
        self.response.payload.pronounceText = welcome_message
        self.response.payload.items.append(get_bubble(welcome_message))
        self.response.payload.items.append(
            get_card_list(
                self.payload.init_background.url,
                self.payload.init_background.hash,
            )
        )

        self.session.questions = self.question_keys
        await self.make_question()
        await self._save_session()

        return self.response

    async def correct_answer_stage(self):
        logger.info("Correct answer stage")
        message = self.phrases["correct"].get_message(
            degree=self.session.score
        )

        self.response.payload.pronounceText = message
        self.response.payload.items.append(get_bubble(message))
        self.session.score += self.payload.config.correct

    async def wrong_answer_stage(self):
        logger.info("Wrong answer stage")
        self.session.score += self.payload.config.wrong
        message = self.phrases["incorrect"].get_message(
            degree=self.session.score
        )
        self.response.payload.pronounceText = message
        self.response.payload.items.append(get_bubble(message))

    async def check_answer_stage(self):
        logger.info("REQUESTED_QUESTION stage init")
        self.response.payload.intent = PROCESSING_ANSWER
        self.response.payload.pronounceText = self.phrases[
            "main"
        ].get_message()

        question: VovkaQuestion = self.questions[self.session.question_id]
        answer_message = question.get_answer_message()

        self.response.payload.pronounceText = ""
        logger.info(f"QUESTION! {self.request.payload.message}")

        user_answer = self.request.payload.message.asr_normalized_message
        logger.info(f"USER ANSWER! {user_answer}")

        if user_answer in question.answers:
            logger.info("Answer is correct")
            await self.correct_answer_stage()
        else:
            logger.info("Answer is incorrect")
            await self.wrong_answer_stage()

        self.response.payload.pronounceText += answer_message
        self.response.payload.items.append(get_bubble(answer_message))
        self.response.payload.items.append(
            get_card_list(question.image_url, question.image_hash)
        )

    async def process(self):
        logger.info("Processing walking Vovka Scenario")
        logger.info(f"Intent -> {self.request.payload.intent}")

        await self._setup_session()

        if self.request.get_intent() == RUN_APP:
            if self.session.is_saved:
                return await self.repeat_question()
            return await self.welcome_stage()

        if self.request.get_intent() == REQUESTED_QUESTION:
            await self.check_answer_stage()
            if self.is_lose():
                return await self.lose_stage()
            if self.is_win():
                return await self.win_stage()
            await self.make_question()

        return self.response

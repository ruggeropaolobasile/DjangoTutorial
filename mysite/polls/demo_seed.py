from dataclasses import dataclass
from typing import Literal

SeedProfile = Literal["core", "mvp", "full"]


@dataclass(frozen=True)
class DemoPoll:
    question_text: str
    age_days: int
    age_hours: int
    choices: list[tuple[str, int]]


# This dataset is designed to cover active features:
# - search by text ("planning", "integration")
# - popular sorting (high vote variance)
# - MVP pipeline stages (<3, >=3, >=5, >=8 votes)
DEMO_POLLS: list[DemoPoll] = [
    DemoPoll(
        question_text="Which feature should we ship next quarter?",
        age_days=0,
        age_hours=2,
        choices=[
            ("Decision Loop timeline", 16),
            ("Slack automation", 24),
            ("Public dashboard", 9),
        ],
    ),
    DemoPoll(
        question_text="Preferred release cadence for product updates?",
        age_days=1,
        age_hours=1,
        choices=[("Weekly", 1), ("Bi-weekly", 1), ("Monthly", 0)],
    ),
    DemoPoll(
        question_text="Which team needs decision insights the most?",
        age_days=2,
        age_hours=3,
        choices=[("Product", 11), ("Sales", 14), ("Customer Success", 21)],
    ),
    DemoPoll(
        question_text="How should we notify owners about pending actions?",
        age_days=3,
        age_hours=2,
        choices=[("Email digest", 5), ("Teams bot", 19), ("Slack DM", 23)],
    ),
    DemoPoll(
        question_text="What is the best KPI for decision health?",
        age_days=4,
        age_hours=5,
        choices=[("Activation rate", 22), ("Votes per poll", 15), ("Time to close", 27)],
    ),
    DemoPoll(
        question_text="Which integration should be prioritized first?",
        age_days=5,
        age_hours=4,
        choices=[("Jira", 20), ("Notion", 17), ("HubSpot", 8)],
    ),
    DemoPoll(
        question_text="Which planning workflow should we test in sprint 15?",
        age_days=6,
        age_hours=1,
        choices=[("Product-led", 3), ("Sales-led", 4), ("Hybrid", 6)],
    ),
    DemoPoll(
        question_text="How mature is our decision loop right now?",
        age_days=7,
        age_hours=6,
        choices=[("Early", 0), ("Scaling", 1), ("Mature", 1)],
    ),
    DemoPoll(
        question_text="What pricing model feels fair for SMB teams?",
        age_days=8,
        age_hours=2,
        choices=[("Per workspace", 13), ("Per active user", 18), ("Usage-based", 6)],
    ),
    DemoPoll(
        question_text="Where should we run customer interviews this month?",
        age_days=9,
        age_hours=3,
        choices=[("In-app widget", 9), ("Video call", 25), ("Email async", 11)],
    ),
]


PROFILE_LIMITS: dict[SeedProfile, int] = {
    "core": 5,
    "mvp": 8,
    "full": len(DEMO_POLLS),
}


def seeded_question_texts() -> list[str]:
    return [item.question_text for item in DEMO_POLLS]


def polls_for_profile(profile: SeedProfile) -> list[DemoPoll]:
    return DEMO_POLLS[: PROFILE_LIMITS[profile]]

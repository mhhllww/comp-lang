# ЗАПУСК: py -3.10 task_4_few_shot.py

from typing import Tuple
from deeppavlov import build_model
from deeppavlov.core.commands.utils import parse_config


SUPPORT_SET = [
    ("Какая погода сегодня?", "get_weather"),
    ("Скажи погоду в Москве", "get_weather"),
    ("Будет ли дождь завтра?", "get_weather"),

    ("Расскажи анекдот", "tell_joke"),
    ("Пошути", "tell_joke"),
    ("Скажи смешную шутку", "tell_joke"),

    ("Нарисуй кота", "draw_picture"),
    ("Сгенерируй картинку", "draw_picture"),
    ("Создай изображение леса", "draw_picture"),
]

INTENT_TO_RU = {
    "get_weather": "get_weather (узнать погоду)",
    "tell_joke": "tell_joke (рассказать шутку)",
    "draw_picture": "draw_picture (сгенерировать картинку)",
    "oos": "oos (Не понимаю запрос)",
}


def decide_intent(intent: str, confidence: float, threshold: float) -> Tuple[str, float]:
    if confidence < threshold:
        return "oos", confidence
    return intent, confidence


def unwrap_first(x):
    """Разматывает вложенные списки/кортежи до первого скаляра."""
    while isinstance(x, (list, tuple)) and len(x) > 0:
        x = x[0]
    return x


def main(threshold: float = 0.55):
    print("\nLoading model...")
    config = parse_config("few_shot_roberta")
    model = build_model(config, download=True, install=True)
    print("Model loaded!\n")

    test_messages = [
        "Какая погода завтра?",
        "Сколько градусов сегодня?",
        "Расскажи анекдот",
        "Пошути пожалуйста",
        "Нарисуй дракона",
        "Сделай изображение космоса",
        # вне интентов
        "Сколько будет два плюс два?",
        "Где находится Салехард?",
    ]

    print(f"Текущий порог уверенности: {threshold}\n")

    # dataset: список пар [текст, интент]
    dataset = [[text, label] for text, label in SUPPORT_SET]

    for msg in test_messages:
        print(f"Вопрос: {msg}")

        res = model([msg], dataset)

        if isinstance(res, (list, tuple)) and len(res) == 2:
            labels_raw, conf_raw = res
            intent = unwrap_first(labels_raw)
            confidence = float(unwrap_first(conf_raw))
        else:
            intent = unwrap_first(res)
            confidence = 1.0

        if not isinstance(intent, str):
            intent = str(intent)

        final_intent, used_conf = decide_intent(intent, confidence, threshold)

        print(f"Уверенность модели: {used_conf}")
        print(f"Итоговый ответ: {INTENT_TO_RU.get(final_intent, INTENT_TO_RU['oos'])}")
        print("-" * 40)


if __name__ == "__main__":
    main()

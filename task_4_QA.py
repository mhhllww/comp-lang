from typing import Tuple
from deeppavlov import build_model


# Контексты прямо в коде
CONTEXTS = [
    "Байкал является самым глубоким озером в мире.",
    "Санкт-Петербург был основан Петром Первым в 1703 году.",
    "У человека обычно 32 постоянных зуба.",
    "Москва является крупнейшим городом России по численности населения.",
    "Волга — самая длинная река в Европе.",
    "Транссибирская магистраль является одной из самых протяжённых железных дорог в мире.",
    "Сердце взрослого человека в среднем делает около 70 ударов в минуту в состоянии покоя.",
    "Земля совершает полный оборот вокруг своей оси примерно за 24 часа.",
    "Кислород составляет около 21 процента от состава атмосферного воздуха.",
    "Эрмитаж является одним из крупнейших художественных музеев мира."
]


def decide_qa_answer(answer: str, confidence: float, threshold: float = 0.98) -> Tuple[str, float]:
    if not answer or answer.strip() == "":
        return "Не могу ответить", confidence

    if confidence < threshold:
        return "Не могу ответить", confidence

    return answer, confidence


def main(threshold: float = 0.98):
    # склеиваем в одно большое поле контекста
    full_context = " ".join(CONTEXTS)

    # загружаем модель
    qa_model = build_model("squad_ru_bert", download=True, install=True)

    print(f"Текущий порог уверенности: {threshold}\n")

    # набор тестовых вопросов
    test_questions = [
        "Сколько зубов у человека",
        "Кем был основан Санкт-Петербург",
        "Где находится Байкал",
        "Какая река самая длинная в Европе",
        "Какое сердце у человека в среднем",
        "Сколько процентов кислорода в воздухе",
        "Какой музей является крупнейшим художественным в мире",
        "Где находится Салехард",
        "Сколько часов длится оборот Земли вокруг своей оси"
    ]

    for question in test_questions:
        print(f"Вопрос: {question}")

        # проверка на слишком короткие вопросы
        if len(question.split()) < 2:
            print("Уверенность модели: 0.0")
            print("Итоговый ответ: Не могу ответить")
            print("-" * 40)
            continue

        answers, starts, confidences = qa_model([full_context], [question])

        confidence = float(confidences[0])
        answer = answers[0]

        final_answer, used_conf = decide_qa_answer(
            answer, confidence, threshold=threshold
        )

        print(f"Уверенность модели: {confidence}")
        print(f"Итоговый ответ: {final_answer}")
        print("-" * 40)


if __name__ == "__main__":
    main()

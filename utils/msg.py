import re
from rapidfuzz import fuzz, process
from loguru import logger
from config.filter import categories_dict
import time


class MessageProcessor:
    def __init__(self):
        self.categories_dict = categories_dict

    def extract_and_remove_phone_numbers(self, message):
        """
        Извлекает номера телефонов из сообщения и удаляет их.
        """
        # logger.info(f'Исходное сообщение для извлечения телефонов: "{message}"')
        phone_pattern = r"(?:\+|\d)[\d\-\(\) ]{9,}\d"
        phone_numbers = re.findall(phone_pattern, message)
        # logger.info(f"Найденные телефонные номера: {phone_numbers}")

        for phone_number in phone_numbers:
            message = message.replace(phone_number, "")

        cleaned_message = message.strip()
        # logger.info(f"Сообщение после удаления телефонов: \"{cleaned_message}\"")
        return phone_numbers, cleaned_message

    def find_best_category_and_score(self, message):
        """
        Находит категорию с наилучшим совпадением по сообщению.
        Если есть несколько категорий с одинаковым результатом, применяет дополнительную логику для выбора.
        """
        # logger.info(f"Начинается поиск ближайшей категории для сообщения: \"{message}\"")
        best_score = 0
        best_categories = []
        message_lower = message.lower()

        for category, phrases in self.categories_dict.items():
            # Находим наилучшее совпадение фразы из текущей категории
            match, score, _ = process.extractOne(
                message_lower,
                phrases,
                scorer=fuzz.partial_token_sort_ratio,
            )
            # logger.info(f"Проверяется категория: \"{category}\" | Совпавшая фраза: \"{match}\" | Уверенность: {score:.2f}%")

            if score > best_score:
                # Обновляем список, если нашлось лучшее совпадение
                best_score = score
                best_categories = [(category, match)]
            elif score == best_score:
                # Добавляем категорию, если совпадение такое же
                best_categories.append((category, match))

        if not best_categories:
            logger.warning("Не удалось найти подходящую категорию.")
            return None, 0

        if len(best_categories) > 1:
            logger.info(
                f'Лучшая категория:"{best_categories}", уверенность: {best_score:.2f}%'
            )
            # Применение дополнительной логики для выбора между категориями
            best_category, best_match = self.resolve_tie(best_categories, message_lower)
        else:
            best_category, best_match = best_categories[0]
            logger.info(
                f'Лучшая категория: "{best_category}", совпавшая фраза: "{best_match}", уверенность: {best_score:.2f}%'
            )

        return best_category, best_score

    from rapidfuzz import fuzz, process

    def resolve_tie(self, categories, message):
        """
        Логика обработки ситуации, когда несколько категорий имеют одинаковые результаты.
        Сравнивает категории между собой и выбирает ту, у которой наибольшее совпадение с текстом сообщения.
        """
        # logger.info("Решение одинакового совпадения...")

        best_score = 0
        best_category = None

        for category, _ in categories:
            # Используем rapidfuzz для вычисления схожести текста (можно выбрать другой метод fuzz)
            score = fuzz.token_set_ratio(
                category.lower(), message
            )  # Сравниваем текст категории с сообщением

            # logger.info(
            #     f'Сравнение для категории: "{category}" | Уверенность: {score:.2f}%'

            # Обновляем результат, если текущая категория имеет лучший счет
            if score > best_score:
                best_score = score
                best_category = category

        logger.debug(
            f'Выбранная категория: "{best_category}" с уверенностью: {best_score:.2f}%'
        )
        return best_category, best_score

    def process_message(self, message):
        """
        Основной метод, извлекает телефоны, очищает сообщения
        и находит ближайшую категорию.
        """
        start_time = time.time()  # Начало замера времени
        # logger.info(f"Начало обработки сообщения: \"{message}\"")

        # Извлечение телефонов
        phones, cleaned_message = self.extract_and_remove_phone_numbers(message)

        # Поиск ближайшей категории
        closest_category, confidence = self.find_best_category_and_score(
            cleaned_message
        )

        elapsed_time = time.time() - start_time  # Общее время выполнения
        logger.debug(
            f'категория="{closest_category}", уверенность={confidence:.2f}%, время выполнения={elapsed_time:.4f} секунд'
        )

        return phones, cleaned_message, closest_category, confidence

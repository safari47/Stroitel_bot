from config.config import client, broker
from utils.msg import MessageProcessor
from loguru import logger
from config.filter import region_url

message_processor = MessageProcessor()

# @client.on_message()
async def keyword_handler(client, message):
    reg = region_url.get(message.chat.id)
    if not reg:
        logger.info("No region")
        return  # Пропускаем, если нет региона

    if not message.text:
        return  # Пропускаем, если нет текста

    logger.info(f"Получено сообщение в чате {message.chat.title}: {message.text}")

    try:
        phones, cleaned_message, closest_category, confidence = message_processor.process_message(message.text)
        
        if not phones:
            # logger.info("Сообщение пропущено, так как нет номеров телефонов.")
            return
        
        if confidence < 50:
            # logger.info("Сообщение пропущено, так как вероятность ниже 50%.")
            return

        data = {
            "phones": phones,
            "cleaned_message": cleaned_message,
            "closest_category": closest_category,
            "region": reg,
        }
        await broker.publish(data, channel="broadcast_message")
    
    except Exception as e:
        logger.error(f"Ошибка при обработке сообщения: {e}")

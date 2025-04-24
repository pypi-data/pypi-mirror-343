from enum import Enum


class RequestMessageTopic(str, Enum):
    """
    Represents a collection of predefined topics as an enumeration.

    This class is an enumeration that defines constant string values for use
    as topic identifiers. These topics represent specific actions or messages
    within a messaging or vector database management context. It ensures
    consistent usage of these predefined topics across the application.

    syntax: [hai].[source].[destination].[action]

    """
    # Telegram
    AI_TG_CHAT_SEND = "hai.ai.tg.chat.send"
    TG_AI_USER_CHAT_SEND = "hai.tg.ai.user.chat.send"
    AI_TG_CHAT_REPLY = "hai.ai.tg.chat.reply"

    # vector database
    AI_VECTORS_SAVE = "hai.ai.vectors.collection.save"

    AI_VECTORS_QUERY = "hai.ai.vectors.collection.query"
    AI_VECTORS_QUERY_RESPONSE = "hai.ai.vectors.collection.query.response"

    AI_VECTORS_METADATA_READ = "hai.ai.vectors.metadata.read"
    AI_VECTORS_METADATA_READ_RESPONSE = "hai.ai.vectors.metadata.read.response"

    # Twitter
    AI_TWITTER_GET_USER = "hai.ai.twitter.get.user"
    AI_TWITTER_GET_USER_RESPONSE = "hai.ai.twitter.get.user.response"

    TWITTER_USER_SEND_AI_CHAT_SEND = "hai.twitter.user.ai.chat.send"
    TWITTER_USER_SEND_AI_CHAT_SEND_RESPONSE = "hai.twitter.user.ai.chat.send.response"
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
    TG_CHAT_SEND = "hai.tg.chat.send"
    TG_USER_CHAT_SEND = "hai.tg.user.chat.send"
    TG_CHAT_REPLY = "hai.tg.chat.reply"

    # vector database
    VECTORS_SAVE = "hai.vectors.save"

    VECTORS_QUERY = "hai.vectors.query"
    VECTORS_QUERY_RESPONSE = "hai.vectors.query.response"

    VECTORS_METADATA_READ = "hai.vectors.metadata.read"
    VECTORS_METADATA_READ_RESPONSE = "hai.vectors.metadata.read.response"

    # Twitter
    TWITTER_GET_USER = "hai.twitter.get.user"
    TWITTER_GET_USER_RESPONSE = "hai.twitter.get.user.response"

    TWITTER_USER_SEND_AI_CHAT_SEND = "hai.twitter.user.chat.send"
    TWITTER_USER_SEND_AI_CHAT_SEND_RESPONSE = "hai.twitter.user.chat.send.response"

    # tools
    WEB_SEARCH = "hai.tools.web.search"
    WEB_SEARCH_RESPONSE = "hai.tools.web.search.response"

    WEB_GET_DOCS = "hai.tools.web.get.docs"
    WEB_GET_DOCS_RESPONSE = "hai.tools.web.get.docs.response"

    WEB_FIND_RELATED = "hai.tools.web.find.related"
    WEB_FIND_RELATED_RESPONSE = "hai.tools.web.find.related.response"
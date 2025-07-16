from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.runnables import (
    RunnablePassthrough,
)  # 1. Import RunnablePassthrough
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.schema.output_parser import StrOutputParser
from database import get_all_sweets

# Initialize the LLM
llm = ChatOpenAI(model="gpt-4o")

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful and friendly assistant for a sweet shop. "
            "Use the following list of sweets to answer the user's question.\n\n"
            "Sweets List:\n{context}",
        ),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ]
)

base_chain = (
    RunnablePassthrough.assign(context=lambda x: get_all_sweets())
    | prompt
    | llm
    | StrOutputParser()
)


def get_conversational_chain(session_id: str, redis_url: str):
    """
    Creates a chain that is aware of chat history and database context.
    """
    chain_with_history = RunnableWithMessageHistory(
        base_chain,
        lambda session_id: RedisChatMessageHistory(
            session_id=session_id, url=redis_url
        ),
        input_messages_key="input",
        history_messages_key="history",
    )
    return chain_with_history

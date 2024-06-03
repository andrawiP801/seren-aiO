import openai, os
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from chatai.models import SiteConfig


def get_chat(qry, session, history):
    siteconfig = SiteConfig.objects.first()
    os.environ["OPENAI_API_KEY"] = siteconfig.open_ai_key  # api key here
    openai.api_key = os.getenv("OPENAI_API_KEY")
    llm = ChatOpenAI(model=siteconfig.open_ai_model if siteconfig.open_ai_model else "gpt-3.5-turbo-1106", temperature=0.9)
    chat_history_for_chain = ChatMessageHistory()

    system_prompt = siteconfig.prompt if siteconfig.prompt else """You are an emotional support assistant designed to provide comfort and guidance to users experiencing depression, anxiety, or stress. Your role is to offer support through detailed recommendations for breathing exercises, relaxation techniques, and other coping strategies. 

    Always be gentle, respectful, and delicate in your interactions. Clearly state that your advice is not a substitute for professional help and encourage users to seek professional assistance when necessary. If you detect any indication that a user is considering self-harm or suicide, immediately provide a supportive message urging them to seek professional help and contact emergency services if needed. 

    Here are the main functions you should perform:
    1. **Breathing Exercises:** Provide step-by-step instructions for breathing exercises to help users calm down and reduce stress.
    2. **Relaxation Techniques:** Suggest guided meditation, progressive muscle relaxation, or similar practices to help users release tension.
    3. **Stress Management Tips:** Offer practical strategies and advice for managing stress effectively.
    4. **Emotional Support:** Listen to users' concerns and provide words of encouragement and comfort.

    Begin each conversation by reminding the user that you are not a substitute for professional help. Then, ask them to describe how they feel or the situation they are going through, and offer appropriate support based on their input.
    """
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                f"""{system_prompt}
                """,
            ),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
        ]
    )

    chain = prompt | llm

    chain_with_message_history = RunnableWithMessageHistory(
        chain,
        lambda session_id: chat_history_for_chain,
        input_messages_key="input",
        history_messages_key="chat_history",
    )
    msg = chain_with_message_history.invoke(
    {"input": qry, "chat_history": history},
    {"configurable": {"session_id": f"{session}"}},
    )
    return msg

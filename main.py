
import asyncio
import logging
import uuid  #  Import for unique session IDs
logging.getLogger("google_genai.types").setLevel(logging.ERROR)

from dotenv import load_dotenv
load_dotenv()

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from agent import root_agent



async def main():
    print("📊 Phoenix Dashboard Chatbot (Google ADK)")
    print("Type 'exit' to quit")

    # Minimal required ADK runtime setup. [web:32]
    session_service = InMemorySessionService()
    runner = Runner(agent=root_agent, app_name="phoenix-chatbot", session_service=session_service)

    # One fixed session for the whole terminal chat. (for memory)
    #await session_service.create_session(app_name="phoenix-chatbot", user_id="user", session_id="terminal")

    while True:
        user_text = input("\nUser: ")
        if user_text.lower() == "exit":
            break
    # New session = No memory
        session_id = str(uuid.uuid4())
        try:
            await session_service.create_session(
                app_name="phoenix-chatbot",
                user_id="user",
                session_id=session_id
            )

            msg = types.Content(role="user", parts=[types.Part(text=user_text)])

            final_text = ""
            async for event in runner.run_async(user_id="user", session_id=session_id, new_message=msg):
                if event.is_final_response() and event.content and event.content.parts:
                    final_text = event.content.parts[0].text
                if getattr(event, "turn_complete", False):
                    break

            print(f"\nAgent: {final_text}\n")
            
        except Exception as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    asyncio.run(main())

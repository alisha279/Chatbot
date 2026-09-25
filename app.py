from chatbot.chatbot import ChatBot
from chatbot.commands import handle_command


def main():

    bot = ChatBot()

    print("=" * 50)
    print("🤖 AI Chatbot")
    print("=" * 50)

    while True:

        # Get user input
        message = input("\nYou: ").strip()

        # Ignore empty input
        if not message:
            continue

        # Exit command
        if message.lower() == "/exit":
            print("👋 Goodbye!")
            break

        # Handle commands first
        command = handle_command(
            message,
            bot.memory,
            bot.prompt_manager
        )

        if command:
            print(f"\nBot: {command}")
            continue

        # Normal chat
        reply = bot.send_message(message)

        print(f"\nBot: {reply}")


if __name__ == "__main__":
    main()
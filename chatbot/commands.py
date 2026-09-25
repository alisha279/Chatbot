def clear_command(memory):
    memory.clear()
    return "✅ Conversation cleared."


def history_command(memory):
    total = len(memory.get_history())
    return f"📜 Conversation contains {total} messages."


def help_command():
    return """
Available Commands
------------------
/help               Show all commands
/clear              Clear conversation
/history            Show total messages
/mode               Show current mode
/mode <mode>        Change chatbot mode
/save               Save conversation
/load               Reload conversation
/exit               Exit chatbot
""".strip()


def mode_command(message, prompt_manager):

    parts = message.split()

    # User typed only: /mode
    if len(parts) == 1:
        return f"Current mode: {prompt_manager.get_mode()}"

    # User typed: /mode python
    mode = parts[1].lower()

    if prompt_manager.set_mode(mode):
        return f"✅ Switched to '{mode}' mode."

    available = ", ".join(prompt_manager.get_available_modes())

    return (
        f"❌ Unknown mode: '{mode}'\n"
        f"Available modes: {available}"
    )


def save_command(memory):
    memory.save_history()
    return "💾 Conversation saved."


def load_command(memory):
    memory.load_history()
    return "📂 Conversation loaded."


def handle_command(message, memory, prompt_manager):

    command_name = message.split()[0].lower()

    commands = {
        "/help": lambda: help_command(),
        "/clear": lambda: clear_command(memory),
        "/history": lambda: history_command(memory),
        "/mode": lambda: mode_command(message, prompt_manager),
        "/save": lambda: save_command(memory),
        "/load": lambda: load_command(memory),
    }

    command = commands.get(command_name)

    if command:
        return command()

    return None
from pathlib import Path

from pydantic_ai_visual.app import convert_to_chat_messages, load_messages

_HERE = Path(__file__).parent
demo_messages = _HERE / "all_messages.json"


def test_load_and_convert():
    """Test loading messages from a file."""
    messages = load_messages(f"file://{demo_messages.absolute().as_posix()}")
    assert messages

    chat_messages = convert_to_chat_messages(messages)
    assert chat_messages

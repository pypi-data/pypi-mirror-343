import base64
import json

import gradio as gr
import httpx
from gradio import ChatMessage
from pydantic_ai.messages import (
    BinaryContent,
    ModelMessage,
    ModelMessagesTypeAdapter,
    ModelRequest,
    ModelResponse,
    RetryPromptPart,
    SystemPromptPart,
    TextPart,
    ToolCallPart,
    ToolReturnPart,
    UserPromptPart,
)


def load_messages(messages: str) -> list[ModelMessage]:
    """Load messages from a file, URL, or direct JSON content."""
    if messages.startswith("file://"):
        with open(messages[7:]) as f:
            messages = f.read()
    if messages.startswith("http://") or messages.startswith("https://"):
        response = httpx.get(messages)
        messages = response.text
    return ModelMessagesTypeAdapter.validate_json(messages)


def convert_to_chat_messages(  # noqa: C901
    model_messages: list[ModelMessage],
) -> list[ChatMessage]:
    """Convert ModelMessage objects to ChatMessage objects for display in Gradio Chatbot."""
    chat_messages = []

    for message in model_messages:
        if isinstance(message, ModelRequest):
            # Handle request messages (user, system, tool return)
            for part in message.parts:
                if isinstance(part, UserPromptPart):
                    # Handle user prompt parts
                    if isinstance(part.content, str):
                        # Simple text content
                        chat_messages.append(ChatMessage(role="user", content=part.content))
                    else:
                        # Handle multi-part content (including images)
                        for content_part in part.content:
                            if isinstance(content_part, str):
                                chat_messages.append(ChatMessage(role="user", content=content_part))
                            elif (
                                hasattr(content_part, "is_image")
                                and content_part.is_image
                                and isinstance(content_part, BinaryContent)
                            ):
                                # Convert binary image to base64 for display
                                img_data = base64.b64encode(content_part.data).decode("utf-8")
                                img_type = content_part.media_type
                                img_src = f"data:{img_type};base64,{img_data}"
                                chat_messages.append(
                                    ChatMessage(
                                        role="user",
                                        content=f"<img src='{img_src}' alt='Image' />",
                                    )
                                )

                elif isinstance(part, SystemPromptPart):
                    # Display system prompts with a special format to make them stand out
                    chat_messages.append(
                        ChatMessage(
                            role="system",
                            content=part.content,
                            metadata={"title": "System Prompt"},
                        )
                    )

                elif isinstance(part, ToolReturnPart):
                    # Display tool returns
                    content = part.model_response_str()
                    chat_messages.append(
                        ChatMessage(
                            role="assistant",
                            content=content,
                            metadata={"title": f"🔧 Tool '{part.tool_name}' returned"},
                        )
                    )

                elif isinstance(part, RetryPromptPart):
                    # Display retry prompts
                    content = part.model_response()
                    title = "💥 Error"
                    if part.tool_name:
                        title = f"💥 Error using tool '{part.tool_name}'"
                    chat_messages.append(ChatMessage(role="assistant", content=content, metadata={"title": title}))

        elif isinstance(message, ModelResponse):
            # Handle response messages (text, tool calls)
            for part in message.parts:
                if isinstance(part, TextPart):
                    # Simple text response
                    if part.content.strip():  # Only add if there's actual content
                        chat_messages.append(ChatMessage(role="assistant", content=part.content))

                elif isinstance(part, ToolCallPart):
                    # Tool call
                    args_str = part.args_as_json_str() if isinstance(part.args, dict) else part.args
                    try:
                        # Try to format the JSON for better readability
                        args_obj = json.loads(args_str)
                        formatted_args = json.dumps(args_obj, indent=2)
                    except Exception:
                        formatted_args = args_str

                    content = f"**Tool**: `{part.tool_name}`\n\n**Arguments**:\n```json\n{formatted_args}\n```"
                    chat_messages.append(
                        ChatMessage(
                            role="assistant",
                            content=content,
                            metadata={"title": f"🛠️ Used tool '{part.tool_name}'"},
                        )
                    )
    return chat_messages


def render_messages(messages_source: str) -> list[ChatMessage]:
    """Load and convert messages from the provided source."""
    try:
        model_messages = load_messages(messages_source)
        chat_messages = convert_to_chat_messages(model_messages)
    except Exception as e:
        return [ChatMessage(role="system", content=f"Error loading messages: {e!s}")]
    # If no messages were rendered, show an error
    if not chat_messages:
        return [
            ChatMessage(
                role="system",
                content="No messages were found or could be rendered.",
            )
        ]

    return chat_messages


def get_url_params(request: gr.Request):
    """Extract URL parameters from the request."""
    try:
        params = request.query_params
        messages_url = params.get("messages", None)
    except Exception:
        return None
    else:
        return messages_url


def create_app():
    """Create the Gradio application."""
    with gr.Blocks() as app:
        gr.Markdown("# ModelMessage Visualizer")

        # State to store URL parameters
        url_params = gr.State(None)

        # Chatbot component for displaying messages
        chatbot = gr.Chatbot(
            type="messages",
            height=600,
            show_copy_button=True,
            sanitize_html=False,
            allow_tags=True,
            show_label=True,
        )

        # Input for manually loading messages
        with gr.Row():
            messages_input = gr.Textbox(
                label="Messages Source (URL, file path, or JSON)",
                placeholder="Enter URL, file:// path, or paste JSON directly",
                lines=1,
            )
            render_button = gr.Button("Render Messages")

        # Handle button click
        render_button.click(fn=render_messages, inputs=messages_input, outputs=chatbot)

        # Handle URL parameters on page load
        def on_url_params_load(messages_url):
            if messages_url:
                return messages_url, render_messages(messages_url)
            return "", []

        # Load URL parameters and automatically render if present
        app.load(get_url_params, None, url_params)

        # When URL parameters are loaded, update the input field and render messages
        url_params.change(
            fn=on_url_params_load,
            inputs=[url_params],
            outputs=[messages_input, chatbot],
        )

    return app


# Create and launch the app
app = create_app()

if __name__ == "__main__":
    app.launch(server_port=8891)

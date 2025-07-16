from open_rag_bot.services.llm.openai_client import OpenAIClient


def test_generate_response_calls_create(mocker):
    dummy_message = mocker.Mock(content="hello from openai!")
    dummy_choice = mocker.Mock(message=dummy_message)
    dummy_completion = mocker.Mock(choices=[dummy_choice])

    dummy_create = mocker.Mock(return_value=dummy_completion)
    dummy_chat = mocker.Mock()
    dummy_chat.completions.create = dummy_create

    dummy_client = mocker.Mock()
    dummy_client.chat = dummy_chat

    openai_client = OpenAIClient.__new__(OpenAIClient)
    openai_client.client = dummy_client

    history = [{"role": "user", "content": "ciao"}]
    out = openai_client.generate_response(history, model="gpt-4o")
    assert out == "hello from openai!"
    dummy_create.assert_called_once_with(messages=history, model="gpt-4o")

from open_rag_bot.services.llm.groq_client import GroqClient


def test_generate_response_calls_create(mocker):
    dummy_completion = mocker.Mock()
    dummy_completion.choices = [mocker.Mock(message=mocker.Mock(content="ok"))]

    dummy_create = mocker.Mock(return_value=dummy_completion)
    dummy_chat = mocker.Mock()
    dummy_chat.completions.create = dummy_create

    dummy_client = mocker.Mock()
    dummy_client.chat = dummy_chat

    groq_client = GroqClient.__new__(GroqClient)
    groq_client.client = dummy_client

    history = [{"role": "user", "content": "prova"}]
    out = groq_client.generate_response(history, model="fake-model")
    assert out == "ok"
    dummy_create.assert_called_once_with(messages=history, model="fake-model")

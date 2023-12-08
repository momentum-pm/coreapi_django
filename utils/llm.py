from openai import OpenAI
from django.conf import settings


class LLM:
    @staticmethod
    def from_chat(prompt, chat):
        from chat.models import Member

        messages = []
        messages.append({"role": "system", "content": prompt})

        for message in chat.messages.all():
            if message.member.role == Member.PERSON:
                role = "user"
            elif message.member.role == Member.ASSISTANT:
                role = "assistant"

            messages.append({"role": role, "content": message.content})
        print("REQUESTING", messages)
        if settings.ENV.LLM_REQUESTS:
            client = OpenAI(api_key=settings.ENV.OPEN_AI_KEY)
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
            )
            print(completion)
            text_response = completion["choices"][0]["messages"]["content"]
        else:
            text_response = "Yes"
        return text_response

    def __init__(self, api_key) -> None:
        self.client = OpenAI(api_key)
        pass

    def process(self, message):
        pass

    def get_next_message(self):
        pass

    def get_output(
        self, prompt, query, model="gpt-3.5-turbo", format="json_object", debug=False
    ):
        import json

        completion = self.client.chat.completions.create(
            model=model,
            response_format={"type": format},
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": query},
            ],
        )
        text_response = completion["choices"][0]["messages"]["content"]
        if format == "json_object":
            response = json.loads(text_response)
        else:
            response = text_response
        if debug:
            print(f"Response ({type(response)}): {text_response}")
        return response

    def get_embedding(self, text):
        completion = self.client.moderations.create(
            input=[text],
            model="text-embedding-ada-002",
        )
        embedding = completion.data[0].embedding
        return embedding

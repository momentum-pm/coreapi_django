from openai import OpenAI
from django.conf import settings


class LLM:
    DEFAULT_MODEL = "gpt-4-1106-preview"
    client = OpenAI()

    def create_assistant_id(
        self,
        name,
        instructions,
        functions=[],
        file_paths=[],
    ):
        tools = []

        # loading functions
        for function in functions:
            tools.append({"type": "function", "function": function})
        # loading files
        file_ids = []
        if len(file_paths) > 0:
            # appending retrieval tooll
            tools.append({"type": "retrieval"})

            # creating and appending files
            for file_path in file_paths:
                file = self.client.files.create(
                    file=open(file_path, "rb"),
                    purpose=name,
                )
                file_ids.append(file.id)
        print("CREATEING ASSISTANT")
        print(name)
        print(instructions)
        print(tools)
        print(file_ids)
        assistant = self.client.beta.assistants.create(
            name=name,
            instructions=instructions,
            model=self.DEFAULT_MODEL,
            tools=tools,
            file_ids=file_ids,
        )
        return assistant.id

    def create_thread_id(self):
        thread = self.client.beta.threads.create()
        return thread.id

    def create_run_id(
        self,
        thread_id,
        assistant_id,
        instructions,
    ):
        run = self.client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id,
            instructions=instructions,
        )
        return run.id

    def get_run_status(self, run_id, thread_id):
        return self.client.beta.threads.runs.retrieve(
            thread_id=thread_id, run_id=run_id
        )["status"]

    def get_message_id(self, content, file_paths, thread_id):
        file_ids = []
        for file_path in file_paths:
            file = self.client.files.create(
                file=open(file_path.file.file, "rb"),
                purpose="assistant",
            )
            file_ids.append(file.id)
        message = self.client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=content,
            file_ids=file_ids,
        )
        return message.id

    def get_messages(self, thread_id):
        messages = self.client.beta.threads.messages.list(thread_id=thread_id)
        return messages.data

    def get_embedding(self, text):
        completion = self.client.embeddings.create(
            input=[text],
            model="text-embedding-ada-002",
        )
        embedding = completion.data[0].embedding
        return embedding


llm = LLM()

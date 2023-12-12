from utils import models, views, responses, permissions
from . import serializers, models
from .actions import Actions


class ThreadsView(views.CreateModelMixin, views.ListModelMixin):
    permission_classes = [permissions.AllowAny]

    base_queryset = models.Thread.objects.all()
    request_serializer = serializers.ThreadCreateSerializer
    response_serializer = serializers.ThreadListSerializer
    filter_lookups = {
        "person": "member__person",
    }


class AssistantsView(views.ListModelMixin):
    permission_classes = [permissions.AllowAny]
    base_queryset = models.Assistant.objects.all()
    response_serializer = serializers.AssistantBaseSerializer


class CallsView(views.BaseViewSet):
    base_queryset = models.Call.objects.all()
    permission_classes = [permissions.AllowAny]

    @views.action(methods=["post"], detail=False)
    def post(self, *args, **kwargs):
        try:
            obj = self.get_object()
            output = self.request.data.get("output")
            obj.output = output
            obj.save()
            if output == "Yes":
                # TODO apply the change
                pass
            from utils.llm import llm
            thread = obj.message.thread
            run = thread.runs.first()
            llm.submit_output(
                thread_id=thread.remote_uuid,
                run_id=run.remote_uuid,
                call_id=obj.remote_uuid,
                output=output,
            )
            return responses.Ok(message=self.get_create_message(obj))
        except responses.BadRequest as response:
            return response


class MessagesView(views.CreateModelMixin, views.ListModelMixin):
    permission_classes = [permissions.AllowAny]
    request_serializer = {"create": serializers.MessageCreateSerializer}
    response_serializer = {"list": serializers.MessageRetrieveSerializer}
    filter_lookups = ["create_at__lt", "created_at__gt"]

    def get_base_queryset(self):
        if self.action == "list":
            thread = self.get_thread()
            from utils.llm import llm

            first_message = thread.messages.first()
            if first_message:
                should_check = False
                if first_message.type == models.Message.CALL:
                    incomplete_calls = message.calls.filter(output__isnull=True)
                    if incomplete_calls.exists() is False and message.content is None:
                        should_check = True
                if first_message.type == models.Message.USER:
                    should_check = True
                if should_check:
                    run = thread.runs.first()
                    remote_run = llm.get_remote_run(run.remote_uuid, thread.remote_uuid)
                    run_status = remote_run.status
                    if run_status in [
                        "completed",
                        "cancelling",
                        "cancelled",
                        "expired",
                        "failed",
                    ]:
                        # Adding assistant message
                        if run_status == "completed":
                            new_message = llm.get_last_message(
                                thread_id=thread.remote_uuid
                            )[0]
                            message_id = new_message.id
                            content = new_message.content[0].text.value
                        else:
                            message_id = "null"
                            content = "Sorry, some error eccured, please try again"
                        if message.type == models.Message.USER:
                            models.Message.objects.create(
                                remote_uuid=message_id,
                                content=content,
                                type=models.Message.ASSISTANT,
                                thread=thread,
                            )
                        else:
                            message.content = content
                            message.remote_uuid = message_id
                            message.save()
                    elif run_status in ["requires_action"]:
                        # Adding call message
                        tool_calls = (
                            remote_run.required_action.submit_tool_outputs.tool_calls
                        )
                        if message.type != models.Message.CALL:
                            message = models.Message.objects.create(
                                remote_uuid="call",
                                type=models.Message.CALL,
                                thread=thread,
                            )
                        for tool_call in tool_calls:
                            arguments = tool_call.function.arguments
                            function_name = tool_call.function.name
                            functions = models.Function.objects.filter(
                                assistant=thread.assistant
                            )
                            func = None
                            print(function_name)
                            for f in functions:
                                print("CHECKING FUNC")
                                print(f.specification)

                                if f.specification.get("name") == function_name:
                                    func = f

                            if func:
                                func_name = func.specification.get("name")
                                func_description = func.specification.get("description")
                                question = llm.get_response(
                                    f"""
                                    I will give you a function name, function description and input arguments of the function,
                                    and you should create a Yes/No Question that asks if the user wants to preform that function with those arguments.
                                    Just return the question alone, with the question mark at the end.
                                    function name: {func_name}
                                    function description: {func_description}
                                    function arguments: {arguments}
                                    """
                                )
                                models.Call.objects.create(
                                    func=func,
                                    arguments=arguments,
                                    message=message,
                                    question=question,
                                    remote_uuid=tool_call.id,
                                )
            return thread.messages.all()
        else:
            return super().get_base_queryset()

    def get_thread(self):
        return self.get_object(
            queryset=models.Thread.objects.all(), keyword="thread_pk"
        )

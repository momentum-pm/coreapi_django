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


from datetime import date as Date


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
                function_name = obj.function.specification.get("name")
                arguments = obj.arguments
                from goals.models import MetricValue, Metric, Person, Goal, Action

                goal = obj.message.thread.assistant.goal
                if function_name == "set_start_date":
                    date = Date.fromisoformat(arguments.get("date"))
                    goal.start = date
                    goal.save()
                if function_name == "set_end_date":
                    date = Date.fromisoformat(arguments.get("date"))
                    goal.end = date
                    goal.save()
                if function_name == "set_doing_percentage":
                    goal.state_percentage = float(arguments.get("doing_percentage"))
                    goal.save()
                if function_name == "set_status":
                    goal.state = float(arguments.get("status"))
                    goal.save()
                if function_name == "change_owner":
                    owner_id = arguments.get("owner_id", None)
                    if owner_id and Person.objects.filter(id=owner_id).exists():
                        person = Person.objects.get(id=owner_id)
                    else:
                        person = Person.objects.create(
                            about="A new person", name=arguments.get("owner_name")
                        )
                    goal.owner = person
                    goal.save()
                if function_name == "update_metricvalue":
                    MetricValue.objects.create(
                        metric=Metric.objects.get(id=arguments.get("metric_id")),
                        value=arguments.get("value"),
                        goal=goal,
                    )
                if function_name == "add_action":
                    person_id = arguments.get("person_id", None)
                    if person_id and Person.objects.filter(id=person_id).exists():
                        person = Person.objects.get(id=person_id)
                    else:
                        person = Person.objects.create(
                            about="A new person", name=arguments.get("owner_name")
                        )
                    Action.objects.create(
                        person=person,
                        summary=arguments.get("summary"),
                        goal=goal,
                    )
                if function_name == "remove_subgoal":
                    goal_id = arguments.get("subgoal_id")
                    if goal_id and Goal.objects.filter(id=goal_id).exists():
                        subgoal = Goal.objects.get(id=goal_id)
                        subgoal.delete()
                if function_name == "add_subgoal":
                    owner_id = arguments.get("owner_id", None)
                    owner_name = arguments.get("owner_name", None)
                    if owner_name:
                        if Person.objects.filter(id=owner_id).exists():
                            owner = Person.objects.get(id=owner_id)
                        else:
                            owner = Person.objects.create(
                                about="A new person", name=arguments.get("owner_name")
                            )
                    else:
                        owner = goal.owner
                    Goal.objects.create(
                        parent=goal,
                        name=arguments.get("name"),
                        summary=arguments.get("summary"),
                        owner=owner,
                    )

                # TODO apply the change
                pass
            from utils.llm import llm

            thread = obj.message.thread
            run = thread.runs.first()
            llm_output = llm.get_response(
                f"""
                    I will give you a question asked by Person1, and answered by Person2 with Yes or No
                    Write a 1 sentence answer instead of the Person2 with respect to their original answer
                    The question by Person1 was:{obj.question}
                    The answer:{output}

                """
            )
            llm.submit_output(
                thread_id=thread.remote_uuid,
                run_id=run.remote_uuid,
                call_id=obj.remote_uuid,
                output=llm_output,
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
                    incomplete_calls = first_message.calls.filter(output__isnull=True)
                    if (
                        incomplete_calls.exists() is False
                        and first_message.content is None
                    ):
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
                        if first_message.type == models.Message.USER:
                            models.Message.objects.create(
                                remote_uuid=message_id,
                                content=content,
                                type=models.Message.ASSISTANT,
                                thread=thread,
                            )
                        else:
                            first_message.content = content
                            first_message.remote_uuid = message_id
                            first_message.save()
                    elif run_status in ["requires_action"]:
                        # Adding call message
                        tool_calls = (
                            remote_run.required_action.submit_tool_outputs.tool_calls
                        )
                        if first_message.type != models.Message.CALL:
                            message = models.Message.objects.create(
                                remote_uuid="call",
                                type=models.Message.CALL,
                                thread=thread,
                            )
                        else:
                            message = first_message
                        for tool_call in tool_calls:
                            arguments = tool_call.function.arguments
                            function_name = tool_call.function.name
                            functions = models.Function.objects.filter(
                                assistant=thread.assistant
                            )
                            func = None
                            print(function_name)
                            for f in functions:
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

from utils import models

from assistants.models import Assistant, Function


class AnalyzerAssistant(Assistant):
    goal = models.OneToOneField(
        to="Goal", related_name="assistant", on_delete=models.CASCADE
    )

    def pre_save(self, in_create=False, in_bulk=False, index=None) -> None:
        if in_create:
            self.name = f"{self.goal.name} Goal Manager Assistant"
            self.instructions = (
                f"""
                You are an assistant who interacts with a user to get new updates on a given goal.
                The goal is described in the JSON format:
                id: {self.goal.id}
                name: {self.goal.name}
                summary:{self.goal.summary}
                The updates may be changes in people responsibilities on the task, or adding new engaged people with new responsibilities.
                The updates may be changes on the state of a property of the task. All of the properties of the task to be monitored are:
            """,
            )

        return super().pre_save(in_create, in_bulk, index)

    def get_instructions_for_run(self, member):
        unseen_notifications = self.goal.notifications.filter(is_seen=False)
        if unseen_notifications.exists():
            from goals.serializers import (
                NotificationSerializer,
                GoalFullRetrieveSerializer,
            )

            notifications = NotificationSerializer(unseen_notifications, many=True).data
            notifications_context = f"""
                You should inform the {member.name} about these new notifications,
                that arrived since your last conversation with them:
                {notifications}
            """
        else:
            notifications_context = ""
        goal = GoalFullRetrieveSerializer(goal=self.goal).data
        return f"""
            You are talking to {member.__str__()}, and today is {models.now().date()}.
            {notifications_context}
            The latest plan for the goal is:
            
            The latest status of the properties of the goal are:

            People currnet state of the goal is:
            {goal}
        """

    def post_save(self, in_create=False, in_bulk=False, index=None) -> None:
        if in_create:
            Function.objects.create(
                assistant=self,
                specification={
                    "name": "state_change_confirmed",
                    "description": """
                        When you detect any changes in people engaged, or changes in the state of properties of the task,
                        you should first get owner's approval on to apply the changes,
                        and the report information that caused this change alongside with the changes.
                        information: a brief of the new information that caused the changes""",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "id": {
                                "type": "string",
                                "description": "The city and state e.g. San Francisco, CA",
                            },
                            "timeline": {},
                        },
                        "required": ["location"],
                    },
                },
            )
        return super().post_save(in_create, in_bulk, index)

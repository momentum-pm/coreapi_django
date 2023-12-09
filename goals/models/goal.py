from utils import models


function_description = """
When you detect any changes in people engaged, or changes in the state of properties of the task,
	you should first get owner's approval on to apply the changes,
	and the report information that caused this change alongside with the changes.
	information: a brief of the new information that caused the changes
	new_state: {
id,
title,
summary,
timeline:[{
		title,
		state,
		responsibilities:[{
			people,
			summary,
			dependencies:[{
			responsibility,
			summary,
			}],
			}]
		}],
sub_goals: [{
	sub_goals:RECURSIVE
	}],
properties:[{
	id,
	name,
	value,
	}]
    """


class Goal(models.CreatableModel):
    assistant = models.OneToOneField(
        to="assistants.Assistant",
        on_delete=models.CASCADE,
    )

    owner = models.ForeignKey(
        to="Person",
        related_name="owned_goals",
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=255)
    summary = models.TextField(blank=True)
    parent = models.ForeignKey(
        to="Goal",
        related_name="children",
        null=True,
        blank=True,
        default=None,
        on_delete=models.CASCADE,
    )
    dependency_goals = models.ManyToManyField(
        to="Goal",
        related_name="dependent_goals",
        through="Dependency",
    )
    properties = models.ManyToManyField(
        to="Property",
        related_name="goals",
        through="Record",
    )
    entities = models.ManyToManyField(
        to="Entity",
        related_name="goals",
        through="Effect",
    )

    def fill_assistant(self):
        from assistants.models import Assistant, Function

        assistant = Assistant.objects.create(
            name=f"{self.name} Goal Manager Assistant",
            instructions=f"""You are an assistant who interacts with a user to get new updates on a given goal.
            The goal is described in the JSON format:
            id: {self.id}
            name: {self.name}
            summary:{self.summary}

            The updates may be changes in people responsibilities on the task, or adding new engaged people with new responsibilities.

            The updates may be changes on the state of a property of the task. All of the properties of the task to be monitored are:
            """,
        )
        Function.objects.create(
            assistant=self.assistant,
            specification={
                "name": "state_change_confirmed",
                "description": function_description,
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

        # TODO create files for assistant

        assistant.fill_remote_id()
        assistant.save()
        self.save()

    def __str__(self) -> str:
        return self.name

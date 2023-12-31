from utils import models
from assistants.models import Assistant, Function


class GoalDefinerAssistant(Assistant):
    @staticmethod
    def get_instance():
        if GoalDefinerAssistant.objects.exists():
            return GoalDefinerAssistant.objects.first()
        else:
            return GoalDefinerAssistant.objects.create()

    def get_default_name(self):
        return "Goal Definer Assistant"

    def get_default_instructions(self):
        return """
                Go through these questions one by one. Ask a question, get the answer, go to next one
                * What is the goal?
                * Clarify the goal by asking some questions but don't ask about the execution plan, steps and milestones.
                * Ask user about the metrics that should be monitored during the goal (e.g. risks, progress, other key metrics)
                When you have a proposal of the goal, present it to the user and ask for approval,
                if the user approved, return the goal in the given json format:
                {
                    name: the name of the goal,
                    summary: the summary of the goal,
                    properties:[a list of properties]
                    }
                
            """

    def get_instructions_for_run(self, member):
        return f"""
            You are talking to {member.__str__()}, and today is {models.now().date()}.
        """

    def define_functions(self):
        Function.objects.create(
            assistant=self,
            specification={
                "name": "new_goal_confirmed",
                "description": """
                    Once you have interacted with the user and became clear on the goal, get their approval,
                    and after they approved to finalize the goal, use this tool to notify us about the new goal
                    """,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "A name for website",
                        },
                        "summary": {
                            "type": "string",
                            "description": "A summary of the goal",
                        },
                        "subgoals": {"type": "list"},
                    },
                    "required": ["name","summary"],
                },
            },
        )

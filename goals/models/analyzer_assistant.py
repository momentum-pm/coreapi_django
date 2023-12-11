from utils import models

from assistants.models import Assistant, Function


class AnalyzerAssistant(Assistant):
    goal = models.OneToOneField(
        to="Goal", related_name="assistant", on_delete=models.CASCADE
    )

    def get_default_name(self):
        return f"{self.goal.name} Goal Manager Assistant"

    def _create_context_str(self, goal_info):
        # "notifications",
        ## goal general info
        goal_name = goal_info.get("name")
        goal_summary = goal_info.get("summary")
        goal_state = goal_info.get("state")
        ## goal update info
        goal_start = goal_info.get("start")
        goal_end = goal_info.get("end")
        goal_latest_metric_values = goal_info.get("latest_metric_values")
        goal_last_actions = goal_info.get("last_actions")
        goal_responsibilites = goal_info.get("responsibilites")
        # goal_subgoals = goal_info.get("subgoals")
        # goal_dependcies = goal_info.get("dependcies")

        goal_context = """
                        Each goal has a owner which is a person. Also each goal as an AI PM (artificial Intelligence project manager). Whenever new information comes in from assistants, Systems, Other PMs, or the owner, the PM will synthesize the info, find out what this info means, what actions it should take, and bring the actions to the owner. If the owner confirms, it does the actions.
                        Each goal also can have some subgoals. Goals (or subgoals with together) can be depenedant to each other. They can be parent/child. For example each goal is a parent for its subgoals.
                        Here are some events that can lead to the updates in a system designed in this architecture:
                        1. Updates to Key Metrics Data
                        2. Updates to Sub-Goal Progress
                        3. Updates to Dependencies
                        4. Updates to Risks
                        5. Updates to Related People
                        6. Updates to Entities

                        These events serve as triggers that prompt the need for updates within the system, ensuring that the information remains accurate and up-to-date for effective project management and goal achievement.
                        You are the AI PM of this goal:
                        Goal: {goal_name}
                        Summary: {goal_summary}
                        --------------------------------------------------------------------------------------------------------------------------------
                        Goal start date is : {goal_start} and end is : {goal_end}
                         --------------------------------------------------------------------------------------------------------------------------------
                        Latest Key Metrics Data: {goal_latest_metric_values}
                        --------------------------------------------------------------------------------------------------------------------------------
                        Summary of Latest Actions: {goal_latest_actions}
                         --------------------------------------------------------------------------------------------------------------------------------
                        Goal's subtasks and their reposible people are: {goal_responsibilites}
                       """.format(
            goal_name=goal_name,
            goal_summary=goal_summary,
            goal_latest_metric_values=goal_latest_metric_values,
            goal_start=goal_start,
            goal_end=goal_end,
            goal_responsibilites=goal_responsibilites,
            goal_latest_actions=goal_last_actions,
        )
        return goal_context

    def get_default_instructions(self):
        from goals.serializers import GoalInitiateSerializer

        data = GoalInitiateSerializer(self.goal).data
        default_instructions = """
                    You are the project-manager of {goal_name} goal which said with details in context.
                    You are responsible for all factors of the project and you should update project factors due to any new information will be given to you about the project.
                    Just update the timeline according to the changes
                    For example if someone gets sick, you should extend project timeline.
                    If a task is done or finished already, you should remove its time from timeline.
                    If a new subtask is added to project, you should estimate its time and update project timeline.
                    If any event happened that affects the project's time significantly, the risks should be updated.
                    You should list all of changes and updates should be applied in the system based on the new information and events user will gave you.
                    The new information will be given in messages.
                    Handle the project carefully. You are the project-manager.
                    Any new information come to you specify any change in all of the variables of the system specially the execution plan and timeline of the project.""".format(
            goal_name=data.get("name")
        )
        return default_instructions

    def get_instructions_for_run(self, member):
        from goals.serializers import GoalFullRetrieveSerializer

        data = GoalFullRetrieveSerializer(self.goal).data
        goal_context = self._create_context_str(data)
        goal_instruction = """
                            the goal owner is: {goal_owner}, 
                            today is: {today_date}
                            """.format(
            goal_name=self.goal.name,
            goal_owner=member.__str__(),
            today_date=models.now().date(),
        )

        goal_instruction += """ Context is: {context}""".format(context=goal_context)
        return goal_instruction

    def define_functions(self):
        # TODO REZA test interface
        # TODO REZA fix functions
        # TODO REZA handle sub-goal and responsibilities conflict
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
                    },
                    "required": ["location"],
                },
            },
        )

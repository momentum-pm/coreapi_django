from utils import serializers
from utils import models

from assistants.models import Assistant, Function


class GoalAIPMAssistant(Assistant):
    goal = models.OneToOneField(
        to="Goal", related_name="assistant", on_delete=models.CASCADE
    )

    def get_default_name(self):
        return f"{self.goal.name} Goal AI PM Assistant"

    def _create_context_str(self, goal_general_info, goal_update_info):
        ## goal general info
        goal_id = goal_general_info.get("id")
        goal_name = goal_general_info.get("name", "")
        goal_summary = goal_general_info.get("summary", "")

        ## goal update info
        goal_start = goal_update_info.get("start")
        goal_end = goal_update_info.get("end")
        goal_responsibilites = goal_update_info.get("responsibilites")
        goal_latest_metric_states = goal_update_info.get("latest_metrics_states")
        goal_subgoals = goal_update_info.get("subgoals")
        goal_dependcies = goal_update_info.get("dependcies")

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
                        Latest Key Metrics Data: {goal_latest_metric_states}
                        --------------------------------------------------------------------------------------------------------------------------------
                        Summary of Latest Actions: {goal_latest_actions}
                        --------------------------------------------------------------------------------------------------------------------------------
                        Goal start date is : {goal_start} and end is : {goal_end}
                        --------------------------------------------------------------------------------------------------------------------------------
                        Goal's subtasks and their reposibles are: {goal_responsibilites}
                        --------------------------------------------------------------------------------------------------------------------------------
                        Related People: {goal_related_people}
                        --------------------------------------------------------------------------------------------------------------------------------
                        Sub-Goals: {goal_subgoals}
                        --------------------------------------------------------------------------------------------------------------------------------
                        All the Entities: {goal_entities}
                        --------------------------------------------------------------------------------------------------------------------------------
                        Risks: {goal_risks}
                        --------------------------------------------------------------------------------------------------------------------------------
                        Dependency between tasks: {goal_dependencies}
                        --------------------------------------------------------------------------------------------------------------------------------
                        Execution plan: {goal_execution_plan}
                        --------------------------------------------------------------------------------------------------------------------------------
                        Project TimeLine: {goal_project_timeline}
                        --------------------------------------------------------------------------------------------------------------------------------
                        People Tasks: {goal_people_tasks}
                       """.format(
            goal_name=goal_name,
            goal_summary=goal_summary,
            goal_latest_metric_states=goal_latest_metric_states,
            goal_start=goal_start,
            goal_end=goal_end,
            goal_responsibilites=goal_responsibilites,
            goal_latest_actions=self.goal.goal_latest_actions,
            goal_subgoals=goal_subgoals,
            goal_entities=self.goal.Entities,
            goal_risks=self.goal.risks,
            goal_dependencies=goal_dependcies,
        )
        return goal_context

    def get_default_instructions(self):
        default_instructions= """
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
                    goal_name=self.goal.name

        # default_instructions = """
        #        You are the project manager of this goal: {goal_name} 
        #        """.format(
        #     self.goal.name
        # )
        # default_instructions += """Context is: {context}""".format(
        #     context=self._create_context_str()
        # )
        return default_instructions

    def get_instructions_for_run(self, member, goal_general_info:serializers.GoalPreDefineSerializer, goal_update_info:serializers.GoalThreadSerializer):
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

    def define_functions(self):
        Function.objects.create(
            assistant=self,
            specification={
                "name": "state_change_confirmed",
                "description": """
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
                    goal_name=self.goal.name
                ),
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


"""
json1: GoalPreDefineSerializer
{
id,
name,
summary,
metrics: ["metric","defenition"]
subgoals: ["id","name","summary"]
dependcies: ["id","name","summary"]
}

"""


"""
json2: GoalThreadSerializer
{

start,
end,
responsibilites: ["id","summary","people":["name","about","id"],"lastest_action","state"]
latest_metrics_states: ["metric","value","action"]
subgoals: ["id","start","end","state"]
dependcies: ["id","start","end","state"]

python dictionary
}
"""



"""

"""
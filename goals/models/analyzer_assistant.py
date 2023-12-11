from utils import models

from assistants.models import Assistant, Function


class AnalyzerAssistant(Assistant):
    goal = models.OneToOneField(
        to="Goal", related_name="assistant", on_delete=models.CASCADE
    )

    def get_default_name(self):
        from utils.llm import llm

        return llm.get_response(
            prompt=f"""Generate a 2 words cool title for an AI Assistant called: {self.goal.name}
            related to its duty which is: {self.goal.summary}
            The first word should be related to the duty of the AI Assistant,
            The second word should be a cybernetic word such as bot, link, assistant, ... or  their synonyms.
            Just output the 2 words"""
        )

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
        ),
        Function.objects.create(
            assistant=self,
            specification={
                "name": "set_start_date",
                "description": "Set the start date of the goal, return output as a json with fields 'message' and 'succeed'. 'message' explains the act and 'succeed' is a boolean output shows if the act was successful.",
                "parameters": {
                    "type": "object",
                    "properties": {
                    "date": {
                        "type": "string",
                        "description": "The start date of the goal e.g. 11 Dec 2023"
                    }
                    },
                    "required": [
                    "date"
                    ]
                }
            },
        ),
        Function.objects.create(
            assistant=self,
            specification={
                "name": "set_end_date",
                "description": "Set the end date of the goal, return output as a json with fields 'message' and 'succeed'. 'message' explains the act and 'succeed' is a boolean output shows if the act was successful.",
                "parameters": {
                    "type": "object",
                    "properties": {
                    "date": {
                        "type": "string",
                        "description": "The end date of the goal e.g. 28 Dec 2023"
                    }
                    },
                    "required": [
                    "date"
                    ]
                }
            },
        ),
        Function.objects.create(
            assistant=self,
            specification={
                "name": "add_subgoal",
                "description": "Add a subgoal with provided name, summary, owner name and owner ID to the goal. If you have subgoal's owner ID, use that. If you have not subgoal's owner ID, use owner name. If you have not none of them, ask the user about them.",
                "parameters": {
                    "type": "object",
                    "properties": {
                    "name": {
                        "type": "string",
                        "description": "Subgoal name"
                    },
                    "summary": {
                        "type": "string",
                        "description": "Subgoal summary"
                    },
                    "owner_name": {
                        "type": "string",
                        "description": "Subgoal owner name"
                    },
                    "owner_id": {
                        "type": "string",
                        "description": "Subgoal owner ID"
                    }
                    },
                    "required": [
                    "name",
                    "summary"
                    ]
                }
            },
        ),
        Function.objects.create(
            assistant=self,
            specification={
                "name": "remove_subgoal",
                "description": "Remove a subgoal from the goal. Both subgoal ID and subgoal name can be provided. If you have subgoal ID, remove the subgoal by subgoal ID. If you have not, remove the subgoal by subgoal name. If you have none of them, ask the user about the inputs.",
                "parameters": {
                    "type": "object",
                    "properties": {
                    "subgoal_id": {
                        "type": "string",
                        "description": "The id of the subgoal should be removed from this goal."
                    },
                    "subgoal_name": {
                        "type": "string",
                        "description": "The name of the subgoal should be removed from this goal."
                    }
                    },
                    "required": [
                    "subgoal_name",
                    "subgoal_id"]
                }
            },
        ),
        Function.objects.create(
            assistant=self,
            specification={
                "name": "set_status",
                "description": "Set the current status of the goal",
                "parameters": {
                    "type": "object",
                    "properties": {
                    "status": {
                        "type": "string",
                        "description": "The current status of the goal which can be 'To Do' or 'In progress' or 'Done'. Don't set the status something else than these. Change the input to one of these if it was not exactly the same"
                    }
                    },
                    "required": [
                    "status"
                    ]
                }
            },
        ),
        Function.objects.create(
            assistant=self,
            specification={
                "name": "set_doing_percentage",
                "description": "Set the current doing percentage of the goal",
                "parameters": {
                    "type": "object",
                    "properties": {
                    "doing_percentage": {
                        "type": "string",
                        "description": "The current doing percentage (progress percentage) of the goal which is a number between 0 and 1 or from 0 to 100 (in percentage)."
                    }
                    },
                    "required": [
                    "doing_percentage"
                    ]
                }
            },
        ),
        Function.objects.create(
            assistant=self,
            specification={
                "name": "add_action",
                "description": "Each action by a person should be added to goal's actions list.",
                "parameters": {
                    "type": "object",
                    "properties": {
                    "person_name": {
                        "type": "string",
                        "description": "The name of the person who has done the action."
                    },
                    "person_id": {
                        "type": "string",
                        "description": "The ID of the person who has done the action."
                    },
                    "summary": {
                        "type": "string",
                        "description": "The summary explanation of the action done for this goal."
                    }
                    },
                    "required": [
                    "person_name",
                    "person_id",
                    "summary"
                    ]
                }
            },
        ),
        Function.objects.create(
            assistant=self,
            specification={
                "name": "update_metricvalue",
                "description": "Update the evaluation metric value for this goal. Check the metric exists (whether metric_id or metric_name), if it doesn't exist don't do anything and tell the user the problem occured. ",
                "parameters": {
                    "type": "object",
                    "properties": {
                    "mertic_id": {
                        "type": "string",
                        "description": "The ID of the metric should be updated."
                    },
                    "mertic_name": {
                        "type": "string",
                        "description": "The name of the metric should be updated."
                    },
                    "value": {
                        "type": "string",
                        "description": "The new value of the metric."
                    }
                    },
                    "required": [
                    "mertic_id",
                    "mertic_name",
                    "value"
                    ]
                }
            },
        ),
        Function.objects.create(
            assistant=self,
            specification={
                "name": "change_owner",
                "description": "Change the owner of the goal. User should specify one of the owner name or owner ID. If none of them is specified, don't do anything and just ask the user about the new owner.",
                "parameters": {
                    "type": "object",
                    "properties": {
                    "owner_name": {
                        "type": "string",
                        "description": "The name of the owner of the goal"
                    },
                    "owner_id": {
                        "type": "string",
                        "description": "The ID of the owner of the goal"
                    }
                    },
                    "required": [
                    "owner_name",
                    "owner_id"
                    ]
                }
            },
        ),

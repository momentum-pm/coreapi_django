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
        goal_id = goal_info.get("id", "")
        goal_name = goal_info.get("name", "")
        goal_summary = goal_info.get("summary", "")
        goal_start_date = goal_info.get("start", "")
        goal_end_date = goal_info.get("end", "")
        goal_status = goal_info.get("state", "")
        goal_latest_actions = goal_info.get("last_actions", "")
        goal_metric_values = goal_info.get("latest_metric_values", "")
        goal_dependencies = goal_info.get("dependencies", "")
        goal_subgoals = goal_info.get("subgoals", "")

        goal_context = """
                        You are the AI PM of this goal:
                        Goal ID: {goal_id}
                        Goal name: {goal_name}
                        Summary: {goal_summary}
                        --------------------------------------------------------------------------------------------------------------------------------
                        Goal start date is : {goal_start_date} and end is : {goal_end_date}
                        --------------------------------------------------------------------------------------------------------------------------------
                        Goal last status: {goal_status}
                        --------------------------------------------------------------------------------------------------------------------------------
                        List of Latest Actions: {goal_latest_actions}
                        --------------------------------------------------------------------------------------------------------------------------------
                        Goal evaluation metric values: {goal_metric_values}
                        --------------------------------------------------------------------------------------------------------------------------------
                        Goal dependencies: {goal_dependencies}
                        --------------------------------------------------------------------------------------------------------------------------------
                        Goal subgoals: {goal_subgoals}
                        Never call more than on tasks in a run, Never include more than 1 function call in a run.
                       """.format(
            goal_id=goal_id,
            goal_name=goal_name,
            goal_summary=goal_summary,
            goal_start_date=goal_start_date,
            goal_end_date=goal_end_date,
            goal_status=goal_status,
            goal_latest_actions=goal_latest_actions,
            goal_metric_values=goal_metric_values,
            goal_dependencies=goal_dependencies,
            goal_subgoals=goal_subgoals,
        )
        return goal_context

    def get_default_instructions(self):
        from goals.serializers import GoalInitiateSerializer

        data = GoalInitiateSerializer(self.goal).data
        default_instructions = """
            You are project manager of the goal '{goal_name}' in an IT and software company. Each goal has an ID and contains:
            1. An owner (A person owns the goal and must confirm your decisions and changes to be applied on goal)
            2. Start Date (beginning date of the goal)
            3. End Date (finishing date of the goal)
            4. Goal name (Goal Name)
            5. Goal summary (a summary explaining the goal)
            6. metrics (Evaluation metrics of how much the goal has proceed)
            7. subgoals (Goal separated to some subgoals. Each subgoal also has an owner too. Subgoals splits the goal into smaller objects to achieve).
            8. status ('To Do' or 'In progress' or 'Done')
            9. doing percentage (shows the progress percentage of goal)
            10. actions (all of the actions done for this goal or all of the changes)

            You should manage this goal. Any new information comes:
            1. you should analyze it
            2. decide whether it affects to your goal or not
            3. if any change required to your goal factors
            4. tell the user the change you want to do and get his permission
            5. if he confirmed then apply the change on the goal.
            6. Tell the new information to your subgoals
            7. If you had any change, tell the change to your subgoals
            Notice call than more than one of these tool functions in one run:
             [set_start_date,set_end_date, add_subgoal, remove_subgoal, set_status,set_doing_percentage, update_metricvalue, add_action, set_owner]
            At each run you are only allowed to call one of mentioned tools alongside any other tools.
            After calling one of the mentioned tools, you will get an output on if the user approved the change.
            If user responds positive to the output of function calls, assume it is done, otherwise ask questions to clarify with them.
            Don't change anything if it was irrelevant. Do all of the steps said to you one by one carefully.

            The goal's info is:
            goal name: {goal_name},
            ------------------------------------------------------------------
            goal summary: {goal_summary},
            ------------------------------------------------------------------
            goal metrics: {goal_metrics},
            ------------------------------------------------------------------
            goal dependencies: {goal_dependencies},
            ------------------------------------------------------------------
            goal subgoals: {goal_subgoals},
            ------------------------------------------------------------------
            """.format(
            goal_name=data.get("name"),
            goal_summary=data.get("summary"),
            goal_metrics=data.get("metrics"),
            goal_dependencies=data.get("dependencies"),
            goal_subgoals=data.get("subgoals"),
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
                "name": "set_start_date",
                "description": "Set the start date of the goal, return output as a json with fields 'message' and 'succeed'. 'message' explains the act and 'succeed' is a boolean output shows if the act was successful.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "date": {
                            "type": "string",
                            "description": "The start date of the goal in YYYY-MM-DD format, e.g. 2023-12-23",
                        }
                    },
                    "required": ["date"],
                },
            },
        )
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
                            "description": "The end date of the goal  in YYYY-MM-DD format, e.g. 2023-12-28",
                        }
                    },
                    "required": ["date"],
                },
            },
        )
        Function.objects.create(
            assistant=self,
            specification={
                "name": "add_subgoal",
                "description": "Add a subgoal with provided name, summary, owner name and owner ID to the goal. If you have subgoal's owner ID, use that. If you have not subgoal's owner ID, use owner name. If you have not none of them, ask the user about them.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Subgoal name"},
                        "summary": {"type": "string", "description": "Subgoal summary"},
                        "owner_name": {
                            "type": "string",
                            "description": "The name of the new owner of the goal. If nobody where mentioned, dont't include an owner",
                        },
                        "owner_id": {
                            "type": "string",
                            "description": "If you have an id given before in the context, put it here. don't generate an id for a newly added person by yourself.  If nobody where mentioned, dont't include an owner",
                        },
                    },
                    "required": ["name", "summary"],
                },
            },
        )
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
                            "description": "The id of the subgoal should be removed from this goal.",
                        },
                        "subgoal_name": {
                            "type": "string",
                            "description": "The name of the subgoal should be removed from this goal.",
                        },
                    },
                    "required": ["subgoal_name", "subgoal_id"],
                },
            },
        )
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
                            "description": "The current status of the goal which can be exactly one of 'upcomming', 'ongoing', or 'passed'. Don't set the status something else than these. Change the input to one of these if it was not exactly the same",
                        }
                    },
                    "required": ["status"],
                },
            },
        )
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
                            "description": "The current doing percentage (progress percentage) of the goal which is an integer between 0 to 100 (in percentage).",
                        }
                    },
                    "required": ["doing_percentage"],
                },
            },
        )
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
                            "description": "The name of the person who has done the action.",
                        },
                        "person_id": {
                            "type": "string",
                            "description": "The ID of the person who has done the action.",
                        },
                        "summary": {
                            "type": "string",
                            "description": "The summary explanation of the action done for this goal.",
                        },
                    },
                    "required": ["person_name", "person_id", "summary"],
                },
            },
        )
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
                            "description": "The ID of the metric should be updated.",
                        },
                        "mertic_name": {
                            "type": "string",
                            "description": "The name of the metric should be updated.",
                        },
                        "value": {
                            "type": "string",
                            "description": "The new value of the metric.",
                        },
                    },
                    "required": ["mertic_id", "mertic_name", "value"],
                },
            },
        )
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
                            "description": "The name of the new owner of the goal",
                        },
                        "owner_id": {
                            "type": "string",
                            "description": "If you have an id given before in the context, put it here. don't generate an id for a newly added person by yourself",
                        },
                    },
                    "required": ["owner_name"],
                },
            },
        )

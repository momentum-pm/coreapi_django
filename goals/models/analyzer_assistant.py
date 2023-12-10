from utils import models

from assistants.models import Assistant, Function


class AnalyzerAssistant(Assistant):
    goal = models.OneToOneField(
        to="Goal", related_name="assistant", on_delete=models.CASCADE
    )

    def get_default_name(self):
        return f"{self.goal.name} Goal Manager Assistant"

    def get_default_instructions(self):
        from goals.serializers import GoalInitiateSerializer

        # TODO remove this comment
        """
                {
        "id": 1,
        "name": "Create a Personalized Virtual Health Assistant",
        "summary": "The goal is to develop a personalized virtual health assistant powered by AI technology. The assistant will provide users with personalized health recommendations, track their health data, and offer insights for maintaining a healthy lifestyle.",
        "metrics": [
            {
            "id": 1,
            "name": "Progress",
            "summary": "Progress, as a project metric, refers to the melays or issues, and make informed decisions to ensure successful project completion."
            }
        ],
        "dependencies": [],
        "dependents": [
            {
            "summary": "-",
            "target": {
                "name": "Develop an MVP for the virtual health assistant with basic features and functionality",
                "summary": "Develop an MVP for the virtual health assistant with basic features and functionality"
            }
            }
        ],
        "subgoals": [
            {
            "name": "Define the product vision and target audience in the healthcare industry",
            "summary": "Defining the product vision and target audience in the healthcare industry"
            },
        
        ],
        "parent": null
        }
        """
        data = GoalInitiateSerializer(self.goal).data

        # TODO SINA
        return f"""
                You are an assistant who interacts with a user to get new updates on a given goal.
                The goal is described in the JSON format:
                data: {data}
                The updates may be changes in people responsibilities on the task, or adding new engaged people with new responsibilities.
                The updates may be changes on the state of a property of the task. All of the properties of the task to be monitored are:
            """

    def get_instructions_for_run(self, member):
        from goals.serializers import GoalFullRetrieveSerializer

        # TODO data example
        """
        {
        "id": 1,
        "name": "Create a Personalized Virtual Health Assistant",
        "summary": "The goal is to develop a personalized virtual health assistant powered by AI technology. The assistant will provide users with personalized health recommendations, track their health data, and offer insights for maintaining a healthy lifestyle.",
        "start": "2023-12-10",
        "end": "2024-02-10",
        "state": "upcomming",
        "last_actions": [],
        "responsibilities": [
            {
            "id": 1,
            "person": {
                "id": 1,
                "name": "Reza Moslemi",
                "about": "Software"
            },
            "summary": "He should create the database",
            "status": "Nothing happened yet"
            }
        ],
        "metrics": [
            {
            "id": 1,
            "name": "Progress",
            "summary": "Progress, as a project metric, refers to the measurement of advancement or completion towards the desired goals or objectives of a project. It provides an indication of how much work has been accomplished and how far along the project is in relation to its overall timeline.\r\n\r\nProgress can be measured in various ways, depending on the nature of the project and its specific goals. Some common methods of measuring progress as a project metric include:\r\n\r\nPercentage Completion: This involves quantifying progress as a percentage of the total work or tasks completed compared to the total work or tasks in the project plan.\r\n\r\nMilestone Achievements: Identifying significant milestones or checkpoints within the project and tracking the completion of these milestones as a measure of progress.\r\n\r\nTask or Activity Tracking: Monitoring the completion of individual tasks or activities within the project plan and aggregating the progress of these tasks to determine overall project progress.\r\n\r\nGantt Chart or Timeline Analysis: Using visual representations such as Gantt charts or timelines to track the planned versus actual progress of tasks and activities over time.\r\n\r\nDeliverable Completion: Assessing progress based on the completion and delivery of key project deliverables or outcomes.\r\n\r\nThe measurement of progress as a project metric helps project managers and stakeholders gauge the project's current status, identify potential delays or issues, and make informed decisions to ensure successful project completion."
            }
        ],
        "latest_metric_values": [
            {
            "id": 4,
            "created_at": "2023-12-10T18:58:45.334634+03:30",
            "value": "70% done",
            "metric": "Progress"
            }
        ],
        "dependencies": [],
        "dependents": [
            {
            "summary": "-",
            "target": {
                "name": "Develop an MVP for the virtual health assistant with basic features and functionality",
                "summary": "Develop an MVP for the virtual health assistant with basic features and functionality"
            }
            }
        ],
        "subgoals": [
            {
            "name": "Define the product vision and target audience in the healthcare industry",
            "summary": "Defining the product vision and target audience in the healthcare industry"
            },
            {
            "name": "Conduct market research and identify user needs and preferences in the health and wellness domain",
            "summary": "Conduct market research and identify user needs and preferences in the health and wellness domain"
            },
            {
            "name": "Develop an MVP for the virtual health assistant with basic features and functionality",
            "summary": "Develop an MVP for the virtual health assistant with basic features and functionality"
            },
            {
            "name": "Enhance the MVP based on user feedback and industry best practices",
            "summary": "Enhance the MVP based on user feedback and industry best practices"
            },
            {
            "name": "Scale the product to handle increased user volumes and integrate with healthcare systems Parental Goals",
            "summary": "Scale the product to handle increased user volumes and integrate with healthcare systems\r\nParental Goals"
            }
        ],
        "parent": null,
        "notifications": [{
            "sender":{"name":"Sina"},
            "information":"A new information",
            "created_at":"2023-03-05"
        }]
}"""
        data = GoalFullRetrieveSerializer(self.goal).data

        # TODO SINA
        return f"""
            You are talking to {member.__str__()}, and today is {models.now().date()}.
            The latest plan for the goal is:
            {data}
        """

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

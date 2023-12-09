from utils import models


class Assistant(models.Model):
    remote_uuid = models.TextField()
    name = models.CharField(max_length=255)
    instructions = models.TextField()
    files = models.ManyToManyField(to="files.File", blank=True)
    member = models.OneToOneField(
        to="assistants.Member",
        on_delete=models.CASCADE,
        related_name="assistant",
    )

    def fill_remote_id(self):
        from utils.llm import llm

        functions = []
        for function in self.functions.all():
            functions.append(function.specification)
        file_paths = []
        for file in self.files.all():
            file_paths.append(file.file.file)
        remote_uuid = llm.create_assistant_id(
            name=self.name,
            instructions=self.instructions,
            functions=functions,
            file_paths=file_paths,
        )
        self.remote_uuid = remote_uuid
        self.save()

    def pre_save(self, in_create=False, in_bulk=False, index=None) -> None:
        if in_create:
            from .member import Member

            self.member = Member.objects.create()
        return super().pre_save(in_create, in_bulk, index)

    def post_save(self, in_create=False, in_bulk=False, index=None) -> None:
        if in_create:
            self.fill_remote_id()

        return super().post_save(in_create, in_bulk, index)

    def __str__(self) -> str:
        return self.name

    def get_instructions_for_run(self, member):
        return self.cast().get_instructions_for_run(member)

    def cast(self):
        from goals.models import AnalyzerAssistant

        if AnalyzerAssistant.objects.filter(pk=self.pk).exists():
            return AnalyzerAssistant.objects.get(pk=self.pk)

    @staticmethod
    def create_broadcaster():
        pass

    @staticmethod
    def create_form_goal(goal):
        pass

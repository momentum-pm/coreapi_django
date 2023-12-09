from utils import models


class Thread(models.Model):
    remote_uuid = models.TextField()
    member = models.ForeignKey(
        to="Member",
        on_delete=models.CASCADE,
        related_name="threads",
    )

    def pre_save(self, in_create=False, in_bulk=False, index=None) -> None:
        if in_create:
            from utils.llm import llm

            self.remote_uuid = llm.create_thread_id()
        return super().pre_save(in_create, in_bulk, index)

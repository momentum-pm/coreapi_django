from utils import models


class Member(models.Model):
    def get_or_create_thread(self):
        from .thread import Thread

        thread, _ = Thread.objects.get_or_create(member=self, defaults={"member": self})
        return thread

    def create_thread(self):
        from .thread import Thread

        return Thread.objects.create(member=self)

    @property
    def name(self):
        return self.__str__()

    def __str__(self) -> str:
        try:
            return self.person.__str__()
        except:
            pass
        try:
            return self.assistant.__str__()
        except:
            pass
        return super().__str__()

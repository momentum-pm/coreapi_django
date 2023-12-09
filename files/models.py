from uuid import UUID
from utils import models

# Create your models here.


class FileManager(models.Manager):
    def get_by_uuid(self, uuid):
        try:
            uuid = UUID(uuid)
            return self.get(uuid=uuid)
        except ValueError:
            raise self.model.DoesNotExist


class File(models.UUIDModel, models.CreatableModel):
    objects = FileManager()

    def file_upload_location(self, filename):
        format_index = filename.rfind(".")
        if format_index == -1:
            raise Exception()

        format = filename[filename.rfind(".") + 1 :]
        name = filename[: filename.rfind(".")]
        self.name = name
        self.format = format
        return f"novira/files/{self.uuid}/{filename}"

    def pre_save(self, in_create=False, in_bulk=False, index=None) -> None:
        super().pre_save(in_create, in_bulk, index)

        if in_create:
            self.size = self.file.size

    file = models.FileField(upload_to=file_upload_location)
    size = models.BigIntegerField()
    name = models.CharField(max_length=255)
    format = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.name}.{self.format}"

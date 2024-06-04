from django.core.files.storage import FileSystemStorage

class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        # Si el archivo ya existe, lo eliminamos primero
        if self.exists(name):
            self.delete(name)
        return name

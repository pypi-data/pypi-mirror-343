from django.contrib.admin import widgets as admin_widgets
from django.db import models
from filehub import widgets as filehub_widgets


class ImagePickerField(models.TextField):
    """
    A string field for storing image URLs. This field uses the `ImagePickerWidget`
    in forms to allow users to select images through a file manager interface.

    The widget allows users to pick an image from the file manager, which will
    then insert the image URL into the field. In the Django admin, it uses
    `AdminImagePickerWidget` for a more integrated interface.
    """

    def __init__(self, *args, file_type=None, file_ext=None, **kwargs):
        self.file_type = file_type
        self.file_ext = file_ext
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs['file_type'] = self.file_type
        kwargs['file_ext'] = self.file_ext
        return name, path, args, kwargs

    def formfield(self, **kwargs):
        defaults = {"widget": filehub_widgets.ImagePickerWidget}
        defaults.update(kwargs)

        # As an ugly hack, we override the admin widget
        if defaults["widget"] == admin_widgets.AdminTextareaWidget:
            defaults["widget"] = filehub_widgets.AdminImagePickerWidget

        if self.file_type:
            if not isinstance(self.file_type, list):
                raise ValueError("file_type must be a list of allowed file types")

        if self.file_ext:
            if not isinstance(self.file_ext, list):
                raise ValueError("file_ext must be a list of allowed file extensions")

        field = super().formfield(**defaults)
        field.widget.attrs.update({
            "data-file-type": ",".join(self.file_type) if self.file_type else "",
            "data-file-ext": ",".join(self.file_ext) if self.file_ext else "",
        })
        return field

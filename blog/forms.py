# blog/forms.py

from django import forms

# untk training111111111111111111111111111111111111111

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result

class FileFieldForm(forms.Form):
    # title = forms.CharField(max_length=200)
    file = MultipleFileField()



# untuk tester2222222222222222222222222222222222222222222222222222
# blog/forms.py


class UploadFileForm(forms.Form):
    file = forms.FileField()



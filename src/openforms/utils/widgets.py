from django import forms


class OpenFormsRadioSelect(forms.RadioSelect):
    template_name = "of_utils/widgets/radio.html"
    option_template_name = "of_utils/widgets/radio_option.html"

    def __init__(self, *args, **kwargs):
        self._inline = kwargs.pop("inline", False)
        super().__init__(*args, **kwargs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["widget"]["inline"] = self._inline
        return context

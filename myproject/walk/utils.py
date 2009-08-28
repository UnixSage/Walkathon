from django.utils.html import escape



def add_required_label_tag(original_function):
    """Adds the 'required' CSS class and an asterisks to required field labels."""
    def required_label_tag(self, contents=None, attrs=None):
        contents = contents or escape(self.label)
        if self.field.required:
            if not self.label.endswith(" *"):
                self.label += " *"
                contents += " *"
            attrs = {'class': 'required'}
        return original_function(self, contents, attrs)
    return required_label_tag

def decorate_bound_field():
    from django.forms.forms import BoundField
    BoundField.label_tag = add_required_label_tag(BoundField.label_tag)


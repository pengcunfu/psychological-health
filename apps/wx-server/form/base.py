from flask_wtf import FlaskForm


class BaseForm(FlaskForm):
    def get_first_error(self):
        if self.errors:
            for field, errors in self.errors.items():
                return errors[0]
        return None

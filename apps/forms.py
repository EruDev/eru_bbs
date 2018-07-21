from flask_wtf import FlaskForm


class BaseForm(FlaskForm):
    def get_error(self):
        error = self.errors.popitem()[0][1]
        return error
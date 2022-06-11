from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField
from wtforms.validators import DataRequired,Length,ValidationError
from flask_wtf.file import FileAllowed,FileField
from ksk.models import BreadSnack

class BreadSnackForm(FlaskForm):
    product_code = StringField('Product Code',validators=[DataRequired()])
    type = StringField('Type',validators=[DataRequired()])
    image_file = FileField('Upload An Image',validators=[FileAllowed(['jpg','jpeg'])])
    product_detail = TextAreaField('About Your Product',validators=[DataRequired(),Length(min=1,max=100)])
    submit = SubmitField('Upload')

    def validate_product_code(self,product_code):
        product = BreadSnack.query.filter_by(product_code=product_code.data).first()
        if product:
            raise ValidationError(f'This product code: {product_code.data} has already existed')
    
    def validate_type(self,type):
        product = BreadSnack.query.filter_by(type=type.data).first()
        if product:
            raise ValidationError(f'This product type: {type.data} has already existed')
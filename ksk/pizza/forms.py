from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField
from flask_wtf.file import FileField,FileAllowed
from wtforms.validators import ValidationError,DataRequired,Length
from ksk.models import Pizza

class PizzaForm(FlaskForm):
    product_code = StringField('Product Code',validators=[DataRequired()])
    type = StringField('Type',validators=[DataRequired()])
    image_file = FileField('Upload An Image',validators=[FileAllowed(['jpg','jpeg'])])
    product_detail = TextAreaField('About Your Product',validators=[DataRequired(),Length(min=1,max=100)])
    submit = SubmitField('Upload')

    def validate_product_code(self,product_code):
        product = Pizza.query.filter_by(product_code=product_code.data).first()
        if product:
            raise ValidationError(f'This product code: {product_code.data} has already existed')
    
    def validate_type(self,type):
        product = Pizza.query.filter_by(type=type.data).first()
        if product:
            raise ValidationError(f'This product type: {type.data} has already existed')
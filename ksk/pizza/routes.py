from flask import Blueprint,flash,url_for,redirect,render_template,request
from flask_login import login_required
from ksk.models import Pizza
from ksk import db
from ksk.pizza.utils import save_img_for_pizza
from ksk.pizza.forms import PizzaForm

pizzas = Blueprint('pizzas',__name__)

########## Pizza Upload #############
@pizzas.route('/upload/pizza',methods=['GET','POST'])
@login_required
def upload_pizza():
    form = PizzaForm()
    if form.validate_on_submit():
        pizza = Pizza(form.product_code.data,form.type.data,form.product_detail.data)
        if form.image_file.data:
            product_img = save_img_for_pizza((form.image_file.data))
            pizza.image_file = product_img
        db.session.add(pizza)
        db.session.commit()
        flash('New Product has been uploaded!','info')
        return redirect(url_for('pizzas.view_pizza')) 

    return render_template('product_upload_form.html',category="Pizza",title="Pizza Upload",form=form)

######### Pizza Client View #############
@pizzas.route('/product/pizza')
def view_pizza():
    page = request.args.get('page',1,type=int)
    pizzas = Pizza.query.order_by(Pizza.date_posted.desc()).paginate(page=page,per_page=3)
    return render_template('pizza_view.html',title="Pizza",pizzas=pizzas)

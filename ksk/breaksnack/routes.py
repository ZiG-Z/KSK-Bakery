from flask import Blueprint,request,redirect,render_template,url_for,flash
from flask_login import login_required
from ksk.breaksnack.utils import save_img_for_breadsnack
from ksk import db
from ksk.models import BreadSnack
from ksk.breaksnack.forms import BreadSnackForm

breadsnacks = Blueprint('breadsnacks',__name__)

########## Bread & Muffin Upload ##########

@breadsnacks.route('/upload/bread&snack',methods=['GET','POST'])
@login_required
def upload_breadsnack():
    form = BreadSnackForm()
    if form.validate_on_submit():
        breadsnack = BreadSnack(form.product_code.data,form.type.data,form.product_detail.data)
        if form.image_file.data:
            product_img = save_img_for_breadsnack((form.image_file.data))
            breadsnack.image_file = product_img
        db.session.add(breadsnack)
        db.session.commit()
        flash('New Product has been uploaded!','info')
        return redirect(url_for('breadsnacks.view_breadsnack')) 

    return render_template('product_upload_form.html',category="Bread & Snacks",title="Bread & Muffin Upload",form=form)

########### Bread & Muffin View #################
@breadsnacks.route('/product/bread&snack')
def view_breadsnack():
    page = request.args.get('page',1,type=int)
    breadsnacks = BreadSnack.query.order_by(BreadSnack.date_posted.desc()).paginate(page=page,per_page=3)
    return render_template('breadsnack_view.html',title="Bread & Snack",breadsnacks=breadsnacks)

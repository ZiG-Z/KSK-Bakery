from flask import Blueprint,flash,render_template,redirect,request,url_for,current_app
from flask_login import login_required,login_user,logout_user,current_user
from ksk.models import BreadSnack, Pizza, User
from ksk import bcrypt,db
from ksk.users.utils import send_mail,save_img_for_pizza,save_img_for_breadsnack
from ksk.users.forms import LoginForm,RequestResetForm,ResetPasswordForm,KSKPizzaUpdateForm,KSKBreadSnackUpdateForm
import os

users = Blueprint('users',__name__)

###### Admin Login #######
@users.route("/kskadmin",methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user)
            flash('You have successfully logged in')
            return redirect(url_for('users.admin_panel')) #need to modify later
        else:
            flash('Wrong Password or Email!','warning')
            return redirect(url_for('users.login'))
    return render_template('login.html',title="Login",form=form)

######## Admin Logout #########
@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

########### Admin Panel ###############
@users.route('/admin_panel')
@login_required
def admin_panel():
    return render_template('admin_panel.html',title="Admin Panel")

############# Account ################
@users.route('/account')
@login_required
def account():
    return render_template('account.html')


############ Generate Token #############
@users.route('/reset_password',methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('users.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_mail(user)
        flash('Reset Password Mail has been sent to your email account')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html',title='Reset Password',form=form)

############### Reset Password #############

@users.route('/reset_password/<token>',methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('users.home'))
    user = User.validate_token(token)
    if user is None:
        flash('That is an invalid or expired token','warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated!')
        return redirect(url_for('users.login'))

    return render_template('reset_password.html',title='Reset Password',form=form)

######### Admin KSK Pizza Update and Delete ########
@users.route('/ksk_pizzas')
@login_required
def ksk_pizzas():
    page = request.args.get('page',1,type=int)
    pizzas = Pizza.query.order_by(Pizza.date_posted.desc()).paginate(page=page,per_page=3)
    return render_template('ksk_pizzas.html',title='KSK Products',pizzas=pizzas)

@users.route('/edit_pizzas/<int:pizza_id>')
@login_required
def edit_pizzas(pizza_id):
    pizza = Pizza.query.get(pizza_id)
    return render_template('edit_pizzas.html',title="Edit Pizza Products",pizza=pizza)

@users.route('/update_pizza/<int:pizza_id>',methods=['POST','GET'])
@login_required
def update_pizza(pizza_id):
    pizza = Pizza.query.get_or_404(pizza_id)
    form = KSKPizzaUpdateForm()
    if form.validate_on_submit():
        if form.image_file.data:
            product_img = save_img_for_pizza(form.image_file.data)
            pizza.image_file = product_img
        pizza.type = form.type.data
        pizza.product_detail = form.product_detail.data
        db.session.commit()
        flash('Your proudct has been updated!')
        return redirect(url_for('users.ksk_pizzas'))
    elif request.method == "GET":
        form.type.data = pizza.type
        form.product_detail.data = pizza.product_detail 
    return render_template('pizza_update_form.html',title="Update Pizza",form=form,pizza=pizza)

@users.route('/delete_pizza/<int:pizza_id>',methods=['POST'])
@login_required
def delete_pizza(pizza_id):
    pizza = Pizza.query.get_or_404(pizza_id)
    if pizza.image_file != "default.jpg":
        picture_to_delete = os.path.join(current_app.root_path,'static/product_images/pizza',pizza.image_file)
        os.remove(picture_to_delete)
    db.session.delete(pizza)
    db.session.commit()
    flash('Your product has been deleted!')
    return redirect(url_for('users.ksk_pizzas'))

######### Admin KSK Bread & Snack Update and Delete ########
@users.route('/ksk_breadsnacks')
@login_required
def ksk_breadsnacks():
    page = request.args.get('page',1,type=int)
    breadsnacks = BreadSnack.query.order_by(BreadSnack.date_posted.desc()).paginate(page=page,per_page=3)
    return render_template('ksk_breadsnacks.html',title='KSK Products',breadsnacks=breadsnacks)

@users.route('/edit_breadsnacks/<int:breadsnack_id>')
@login_required
def edit_breadsnacks(breadsnack_id):
    breadsnack = BreadSnack.query.get(breadsnack_id)
    return render_template('edit_breadsnacks.html',title="Edit Bread & Snack Products",breadsnack=breadsnack)

@users.route('/update_breadsnack/<int:breadsnack_id>',methods=['POST','GET'])
@login_required
def update_breadsnack(breadsnack_id):
    breadsnack = BreadSnack.query.get_or_404(breadsnack_id)
    form = KSKBreadSnackUpdateForm()
    if form.validate_on_submit():
        if form.image_file.data:
            product_img = save_img_for_breadsnack(form.image_file.data)
            breadsnack.image_file = product_img
        breadsnack.type = form.type.data
        breadsnack.product_detail = form.product_detail.data
        db.session.commit()
        flash('Your proudct has been updated!')
        return redirect(url_for('users.ksk_breadsnacks'))
    elif request.method == "GET":
        form.type.data = breadsnack.type
        form.product_detail.data = breadsnack.product_detail 
    return render_template('breadsnack_update_form.html',title="Update Bread & Snacks",form=form,breadsnack=breadsnack)

@users.route('/delete_breadsnack/<int:breadsnack_id>',methods=['POST'])
@login_required
def delete_breadsnack(breadsnack_id):
    breadsnack = BreadSnack.query.get_or_404(breadsnack_id)
    if breadsnack.image_file != "default.jpg":
        picture_to_delete = os.path.join(current_app.root_path,'static/product_images/breadsnack',breadsnack.image_file)
        os.remove(picture_to_delete)
    db.session.delete(breadsnack)
    db.session.commit()
    flash('Your product has been deleted!')
    return redirect(url_for('users.ksk_breadsnacks'))


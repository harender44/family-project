
from flask import Blueprint, render_template, session, redirect, url_for, request
from functools import wraps

from ..models import *

user = Blueprint('user', __name__ , static_folder="static", template_folder="templates")

def is_user_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'id' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('hom.home'))
    return wrap


@user.route('/')
@is_user_in
def home():
    id = session['id']
    user = Users.query.filter_by(id=id).first()
    return render_template('user/user.html', user = user)


@user.route('/dna')
@is_user_in
def dna():
    id = session['id']
    user = Users.query.filter_by(id=id).first()
    return render_template('user/dna.html', user = user)

@user.route('/bio')
@is_user_in
def biography():
    id = session['id']
    user = Users.query.filter_by(id=id).first()
    return render_template('user/bio.html', user = user)

@user.route('/profile', methods=["GET","POST"])
@is_user_in
def profile():
    if Profile.query.filter_by(uid=session['id']).first() and FamilyDetails.query.filter_by(uid=session['id']).first():
        person = Users.query.filter_by(id=session['id']).first()
        profile = Profile.query.filter_by(uid=session['id']).first()
        family = FamilyDetails.query.filter_by(uid=session['id']).first()
        return render_template('user/profile.html',person=person, profile = profile, family=family)
    
    if request.method =="POST":
        gotra = request.form.get('gotra')
        religion = request.form.get('religion')
        caste = request.form.get('caste')
        s_caste = request.form.get('sub_caste')
        native_town = request.form.get('native_town')
        mother_tongue = request.form.get('mother_tongue')
        place_of_birth = request.form.get('place_of_birth')
        dob = request.form.get('dob')
        gender = request.form.get('gender')

        prof = Profile(uid = session['id'],gotra = gotra, religion=religion, caste=caste,gender=gender,sub_caste=s_caste,mother_tongue=mother_tongue,native_region=native_town,date_of_birth=dob,place_of_birth=place_of_birth)
        db.session.add(prof)

        father_name = request.form.get('father_name')
        mother_name = request.form.get('mother_name')
        grand_father = request.form.get('grand_father')
        grand_mother = request.form.get('grand_mother')
        g_grand_father = request.form.get('g_grand_father')
        g_grand_mother = request.form.get('g_grand_mother')
        spouse_name = request.form.get('spouse_name')
        kid = request.form.getlist('kids')

        print(kid)
        kids = ""
        if kid:
            for k in kid:
                try:
                    kids = kids + "," +k
                except:
                    kids = k
        else:
            kids = None

        fam = FamilyDetails(uid=session['id'],father_name=father_name,mother_name=mother_name,
        grand_father=grand_father,grand_mother=grand_mother,great_grand_father=g_grand_father,great_grand_mother=g_grand_mother,spouse_name=spouse_name,kids=kids)

        db.session.add(fam)
        db.session.commit()

    return render_template('user/profile.html')

@user.route('/dashboard')
@is_user_in
def dashboard():
    id = session['id']

    return render_template('user/dashboard.html', user = True)


@user.route('/contact', methods=['GET','POST'])
@is_user_in
def contact():
    id = session['id']
    return render_template('contact.html', user = True)


@user.route('/logout')
@is_user_in
def logout():
    id = session['id']
    session.pop('id', None)
    return redirect(url_for('hom.home'))


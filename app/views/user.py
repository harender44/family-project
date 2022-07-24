from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify,flash
from functools import wraps

from twilio.rest import Client
from .. import keys
client = Client(keys.account_sid, keys.auth_token)

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


@user.route('/dna', methods=['GET','POST'])
@is_user_in
def dna():
    if request.method == 'POST':
        f_name = request.form.get('f_name')
        l_name = request.form.get('l_name')
        email = request.form.get('email')
        number = request.form.get('number')
        residence = request.form.get('residence')
        reason = request.form.get('reason')
        
        record = DnaTest(user_id=session['id'],first_name=f_name,last_name=l_name,email=email,contact_number=number,residence=residence,reason=reason)
        db.session.add(record)
        db.session.commit()

        return redirect(url_for('user.home'))

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

        prof = Profile(uid = session['id'],gotra = gotra.lower(), religion=religion.lower(), caste=caste.lower(),gender=gender.lower(),sub_caste=s_caste.lower(),mother_tongue=mother_tongue.lower(),native_region=native_town.lower(),date_of_birth=dob,place_of_birth=place_of_birth.lower())
        db.session.add(prof)

        father_name = request.form.get('father_name')
        mother_name = request.form.get('mother_name')
        grand_father = request.form.get('grand_father')
        grand_mother = request.form.get('grand_mother')
        g_grand_father =''   #g_grand_father = request.form.get('g_grand_father')
        g_grand_mother =''     #g_grand_mother = request.form.get('g_grand_mother')
        spouse_name = request.form.get('spouse_name')
        kid = request.form.getlist('kid')

        kids = ""
        if kid:
            for k in kid:
                try:
                    kids = kids + "," +k.lower()
                except:
                    kids = k.lower()
        else:
            kids = None
        
        fam = FamilyDetails(uid=session['id'],father_name=father_name.lower(),mother_name=mother_name.lower(),
        grand_father=grand_father.lower(),grand_mother=grand_mother.lower(),great_grand_father=g_grand_father.lower(),great_grand_mother=g_grand_mother.lower(),spouse_name=spouse_name.lower(),kids=kids)

        db.session.add(fam)
        db.session.commit()

    return render_template('user/profile.html')

@user.route('/dashboard')
@is_user_in
def dashboard():
    id = session['id']
    me=Users.query.filter_by(id=id).first()
    frds = me.family_users
    if frds is not None:
        frs=[]
        req = []
        for i in frds.split(','):
            if i[-1] != '+':
                r = Users.query.filter_by(id=int(i)).first()
                req.append({'id':i,'name':r.sur_name+' '+r.first_name+' '+r.last_name})
            else:
                r = Users.query.filter_by(id=int(i[:-1])).first()
                frs.append({'id':i,'name':r.sur_name+' '+r.first_name+' '+r.last_name})
                frs.append(i)
    else:
        frs =None
        req=None
    return render_template('user/dashboard.html', user = True, friends=frs, requests=req)


@user.route('/contact', methods=['GET','POST'])
@is_user_in
def contact():
    if request.method == "POST":
        f_name = request.form.get('f_name')
        l_name = request.form.get('l_name')
        number = request.form.get('number')
        email = request.form.get('email')
        message = request.form.get('message')

        record = Contact(user_id=session['id'],first_name=f_name,last_name=l_name,contact_number=number,email=email,message=message)
        db.session.add(record)
        db.session.commit()
        return redirect(url_for('user.home'))
    id = session['id']
    return render_template('contact.html', user = True)


@user.route('/logout')
@is_user_in
def logout():
    id = session['id']
    session.pop('id', None)
    return redirect(url_for('hom.home'))

@user.route('/add_friend', methods=['POST'])
@is_user_in
def add_friend():
    me = Users.query.filter_by(id=session['id']).first()
    name=me.first_name
    id = request.form.get('id')
    friend = Users.query.filter_by(id=id).first().phone_number
    msg = f"Hey, {name} has invited you to the family tree on our app. To view him visit https://domain-name.com/user/{id}"
    try:
        '''
        client.messages.create(
            body=msg,   
            from_ = keys.my_number,
            to = '+91'+ friend
        )
        '''
        try:
            me.family_users = me + ','+id
        except:
            me.family_users = ''+id
        db.session.commit()
    except:
        return jsonify({"error":"Your request is not sent!!"})
    return jsonify({"success":"Your request has been sent successfully!!"})

@user.route('/<int:i>')
@is_user_in
def get_friend(i):
    friend = Users.query.filter_by(id=i).first()
    peers =friend.family_users
    if str(session['id']) in peers.split(','):
        return render_template('user/friend_request.html', friend=friend)
    return redirect(url_for('user.home'))

@user.route('/accept_friend', methods=["POST"])
@is_user_in
def accept_friend():
    id_ = request.form.get('id')
    me1 = Users.query.filter_by(id=session['id']).first()
    me = me1.family_users
    if me:
        me = id_+'+'
    else:
        me = me + ','+id_+'+'
    
    friend = Users.query.filter_by(id=id_).first()
    l = friend.family_users
    li = l.split(',')
    final_ = ''
    if li is not None:
        if ','+id_+',' in li:
            final_ = l.replace(','+id_+',',','+id_+'+,')
        elif id_+',' in li:
            final_ = l.replace(id_+',', id_+'+,')
        else:
            final_ = l.replace(','+id_, ','+id_+',')
    else:
        final_ = str(id_)+'+'
    l = final_

    try:
        me1.family_users = me1.family_users + me
    except:
        me1.family_users = me

    db.session.commit()
    
    return redirect(url_for('user.friend',friend_id=id_))

@user.route('/friend')
@is_user_in
def friend():
    if request.args['friend_id']:
        id_ = request.args['friend_id']
    elif request.form.get('friend_id'):
        id_ = request.form.get('friend_id')
    else:
        return redirect(url_for('user.home'))
    friend = Users.query.filter_by(id=id_).first()
    return render_template('user/friend.html', friend=friend)

@user.route('/search', methods=["POST"])
def search():
    q = request.form.get('q')
    qq = f"%{q}%"
    ppl_sn = Users.query.filter(Users.first_name.like(qq)).all()
    user = Users.query.filter_by(id=session['id']).first()
    sn = user.sur_name
    go = Profile.query.filter_by(uid=session['id']).first().gotra
    ppl_go = Profile.query.filter_by(gotra = go).all()
    if user.family_users is None:
        friends = []
    else:
        friends = user.family_users.split(',')
    suggestions = []
    for i in ppl_sn:
        if i.id == session['id'] or str(i.id) in friends:
            continue
        if i.sur_name == sn:
            suggestions.append([str(i.id),i.sur_name+" "+i.first_name + " "+i.last_name])
    for i in ppl_go:
        if i.id == session['id'] or str(i.id) in friends:
            continue
        f = Users.query.filter_by(id=i.uid).first()
        pp = str(i.id),f.sur_name+" "+f.first_name + " "+f.last_name
        if pp not in suggestions:
            suggestions.append(pp)
    return jsonify({'results': suggestions})










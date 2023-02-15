from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from marvel_inv.forms import CharacterForm
from marvel_inv.models import Character, db
import time




site = Blueprint('site', __name__, template_folder = 'site_templates')

"""
Note that in the above code, some arguments are specified when creating the 
Blueprint object. The first argument, 'site', is the Blueprint's name, this is used
by Flask's routing mechanism. The second argument, __name__, is the Blueprint's import name,
which Flask uses to locate the Blueprint's resources
"""

def unmute_video():
    time.sleep(35)  # wait for 3 seconds
    return """
        <script>
            var video = document.getElementById("my-video");
            video.muted = false;
        </script>
    """

unmute_video()

@site.route('/')
def home():
    return render_template('index.html')


@site.route('/profile', methods = ['GET', 'POST'])
@login_required
def profile():
    my_char = CharacterForm()
    try:
        if request.method == "POST" and my_char.validate_on_submit():
            name = my_char.name.data
            description = my_char.description.data
            power = my_char.power.data
            role = my_char.role.data
            identity = my_char.identity.data
            sidekick = my_char.sidekick.data
            comic = my_char.comic.data
            user_token = current_user.token
            char = Character(name, description, power, role, identity, sidekick, comic, user_token)

            db.session.add(char)
            db.session.commit()

            return redirect(url_for('site.profile'))

    except:
        raise Exception("Drone not created, please check your form and try again!")

    user_token = current_user.token

    heros = Character.query.filter_by(user_token = user_token)


    return render_template('profile.html', form = my_char, heros = heros)
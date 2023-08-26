import frontend.forms as forms
import frontend.models as models
import requests
from frontend.app import app, bcrypt
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import LoginManager
from flask_login import logout_user
from frontend.logs.logger import logger

login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id: int):
    try:
        user_data = requests.get(f"http://127.0.0.1:1337/api/v1/accounts/{user_id}")
        if user_data.status_code == 200:
            user_dict = user_data.json()
            user = models.User(id=user_dict["id"], is_active=user_dict["is_active"])
            return user
    except requests.exceptions.ConnectionError as error:
        app.logger.error(f"Connection error while fetching user data: {error}")
        return None
    except requests.exceptions.RequestException as error:
        app.logger.error(f"Request error while fetching user data: {error}")
        return None


@app.route("/")
def index():
    return render_template("index.html")


@login_manager.unauthorized_handler
def guest_callback():
    return redirect(url_for("log_in"))


@app.errorhandler(404)
def page_not_found(error):
    logger.error(f"404 Error: {request.url}")
    return render_template("404.html"), 404


@app.route("/game", methods=["GET", "POST"])
@login_required
def game():
    global game_id
    global game_word

    try:
        game_response = requests.post(
            f"http://127.0.0.1:1337/api/v1/games/create/{current_user.id}"
        )

        if game_response.status_code == 200:
            game_data = game_response.json()

            game_id = game_data.get("id")
            game_tries = game_data.get("game_tries")
            game_display = game_data.get("game_display")
            game_word = game_data.get("game_word")
            game_word_set = game_data.get("game_word_set")
            game_status = game_data.get("status")

            return render_template(
                "game.html",
                game_word_set=game_word_set,
                game_display=game_display,
                game_draw="/static/img/hang%d.png" % game_tries,
                game_tries=game_tries,
                game_status=game_status,
            )
    except requests.exceptions.RequestException as error:
        flash("Failed to start a new game, server error.", "danger")
        logger.error(f"Error while starting a new game: {error}")


@app.route("/play_game", methods=["GET", "POST"])
@login_required
def play_game():
    global game_id
    try:
        letter = request.form["letter"]
        play_data = {"game_id": game_id, "guess_letter": letter}
    except KeyError:
        return redirect(url_for("game"))
    try:
        game_response = requests.post(
            f"http://127.0.0.1:1337/api/v1/games/play/{game_id}", json=play_data
        )
        if game_response.status_code == 200:
            game_data = game_response.json()
            game_tries = game_data.get("game_tries")
            game_display = game_data.get("game_display")
            game_word_set = game_data.get("game_word_set")
            game_status = game_data.get("status")

        guesses = requests.get(
            f"http://127.0.0.1:1337/api/v1/guesses/game_guesses/{game_id}"
        )
        if guesses.status_code == 200:
            guesses_data = guesses.json()
            user_guesses = [item.get("guess_letter") for item in guesses_data]

        while game_status == "NEW":
            return render_template(
                "game.html",
                game_display=game_display,
                game_word_set=game_word_set,
                game_draw="/static/img/hang%d.png" % game_tries,
                game_tries=game_tries,
                user_guesses=user_guesses,
            )

        return render_template(
            "results.html",
            game_status=game_status,
            game_word=game_word,
            game_display=game_display,
            game_word_set=game_word_set,
            game_draw="/static/img/hang%d.png" % game_tries,
            game_tries=game_tries,
            user_guesses=user_guesses,
        )
    except requests.exceptions.RequestException as error:
        flash(
            "Failed to play the game due to a server error. Please try again later.",
            "danger",
        )
        logger.error(f"Error while playing the game: {error}")
        return redirect(url_for("game"))


@app.route("/registration", methods=["GET", "POST"])
def reg_in():
    if current_user.is_authenticated:
        logger.debug("Authenticated user redirected to index")
        return redirect(url_for("index"))

    form = forms.RegistrationForm()
    if form.validate_on_submit():
        pwd_hash = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user_data = {
            "email": form.email.data,
            "password": pwd_hash,
            "username": form.username.data,
        }
        try:
            response = requests.post(
                "http://127.0.0.1:1337/api/v1/accounts", json=user_data
            )
            if response.status_code == 200:
                flash("Account created successfully!", "success")
                logger.debug(f"New user {form.username.data} registered")
                return redirect(url_for("log_in"))
            else:
                flash("Failed to create account. Please try again.", "danger")
                logger.error("Failed to create new user")
        except requests.exceptions.RequestException as error:
            flash("Failed to create account, server error.", "danger")
            logger.error(f"Error creating account: {error}")

    return render_template("sign_in.html", form=form)


@app.route("/history", methods=["GET", "POST"])
@login_required
def get_user_games():
    user_id = current_user.id
    try:
        response = requests.get(f"http://127.0.0.1:1337/api/v1/games/{user_id}")
        if response.status_code == 200:
            games = response.json()
            logger.debug("get_user_games retrieve games.")
            return render_template("game_history.html", games=games)
        else:
            flash("Failed to get games, server error.", "danger")
            logger.error(f"Error while retrieving games: {error}")
    except requests.exceptions.RequestException as error:
        logger.error(f"Error while retrieving games: {error}")
        error_message = "Failed to retrieve games."
        return render_template("game_history.html", error_message=error_message)


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    try:
        response = requests.get(
            f"http://127.0.0.1:1337/api/v1/accounts/{current_user.id}"
        )
        if response.status_code == 200:
            user = response.json()
    except requests.exceptions.RequestException as error:
        logger.error(f"Error while fetching user account: {error}")
        user = None

    try:
        response = requests.get(
            f"http://127.0.0.1:1337/api/v1/games/stats/{current_user.id}"
        )
        if response.status_code == 200:
            stats = response.json()
    except requests.exceptions.RequestException as error:
        logger.error(f"Error while fetching game stats: {error}")
        stats = None

    try:
        response = requests.get(
            f"http://127.0.0.1:1337/api/v1/games/stats/lasts/{current_user.id}"
        )
        if response.status_code == 200:
            five = response.json()
    except requests.exceptions.RequestException as error:
        logger.error(f"Error while fetching last game stats: {error}")
        five = None

    logger.debug(f"User: {current_user.id} account page information loaded")
    return render_template(
        "account.html",
        account=user,
        stats=stats,
        last_five_games=five,
    )


@app.route("/account-update", methods=["GET", "POST"])
@login_required
def account_update():
    form = forms.AccountUpdate()
    if form.validate_on_submit():
        update_data = {"email": form.email.data, "username": form.username.data}
        try:
            response = requests.patch(
                f"http://127.0.0.1:1337/api/v1/accounts/{current_user.id}",
                json=update_data,
            )
            if response.status_code == 200:
                flash("Your account has been updated.", "success")
                logger.debug(f"ID: {current_user.id} acccount has been updated")
                return redirect(url_for("account"))
            else:
                logger.error(
                    f"Failed to update account. Status code: {response.status_code}"
                )
        except requests.exceptions.RequestException as e:
            logger.error(f"Error while updating account: {e}")
    return render_template("account_update.html", title="Account", form=form)


@app.route("/password-change", methods=["GET", "POST"])
@login_required
def password_change():
    form = forms.PasswordForm()
    if form.validate_on_submit():
        response = requests.get(
            f"http://127.0.0.1:1337/api/v1/accounts/{current_user.id}"
        )
        user = response.json()
        user_password = user.get("password")
        if bcrypt.check_password_hash(user_password, form.old_password.data):
            new_password_hash = bcrypt.generate_password_hash(
                form.new_password_first.data
            ).decode("utf-8")
            update_data = {"password": new_password_hash}
            rresponse = requests.patch(
                f"http://127.0.0.1:1337/api/v1/accounts/{current_user.id}",
                json=update_data,
            )
            if rresponse.status_code == 200:
                flash("Your password has been updated!", "success")
                return redirect(url_for("account"))
        else:
            logger.debug("Bad password, wrong old password.")
            flash("Failed to update. Check your password", "danger")
    return render_template(
        "password_update.html", title="Slaptažodžio keitimas", form=form
    )


@app.route("/login", methods=["GET", "POST"])
def log_in():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            response = requests.get(
                f"http://127.0.0.1:1337/api/v1/accounts/email/{form.email.data}"
            )

            if response.status_code == 200:
                user_data = response.json()
                user_id = user_data.get("id")
                user_password = user_data.get("password")
                user_status = user_data.get("is_active")
                if user_data and bcrypt.check_password_hash(
                    user_password, form.password.data
                ):
                    user = models.User(id=user_id, is_active=user_status)
                    login_user(user)
                    return redirect(url_for("index"))
                else:
                    logger.debug("Login failed, bad credentials.")
                    flash("Login failed. Check email email and password", "danger")
        except requests.exceptions.RequestException as error:
            flash("Login failed, server error.", "danger")
            logger.error(f"Error while logging: {error}")

    return render_template("log_in.html", title="Login", form=form)


@app.route("/logoff")
def atsijungti():
    logout_user()
    return redirect(url_for("index"))

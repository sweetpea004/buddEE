from flask import Flask, render_template, request, redirect, flash, session, abort
import os
import json
import usermanagement as um
import random
from datetime import datetime, date

app = Flask(__name__)
app.secret_key = os.urandom(32)
# app.secret_key = "temp secret key"


@app.get('/')
def redirect_home():
    return redirect('/home')


@app.get('/home')
def home():
    if 'user' in session:
        return redirect('/dashboard')
    else:
        return render_template('home.html')


@app.get('/about')
def about():
    return render_template("about.html")


@app.get('/help')
def display_help():
    # can be accessed without session

    return render_template('help.html')


@app.get('/signup')
def display_sign_up():
    return render_template("signup.html")


@app.post('/signup')
def sign_up():
    # load users
    users_list = um.load_users()

    username = request.form['username']
    password = request.form['create-password']
    password_confirm = request.form['password-confirm']

    # generate a unique and random id number for the user
    complete = False
    while complete == False:
        num = random.randint(1, 1000)
        found = False

        for user in users_list:
            if num == user['id']:
                found = True

        if found == False:
            id = num
            complete = True

    # Check that passwords are the same
    if password != password_confirm:
        flash('Passwords must be the same.', 'error')
        return redirect('/signup')
    else:  # check if user already exists before creating account
        if um.user_exists(username):
            flash('This account already exists', 'error')
            return redirect("/signup")
        else:
            um.add_user(username, id, password)

        # Make the user a file for their pets and exercises
        with open(f'user_data/{id}.json', 'w') as f:
            # TODO check with mr antonio if this is right
            json.dump({"pets": [], "activities": []}, f)

        flash('Sign up successful. Please log in.', 'info')
        return redirect("/login")


@app.get('/login')
def display_log_in():
    return render_template("login.html")


@app.post('/login')
def log_in():
    username = request.form['username']
    password = request.form['password']

    # find the possible ID of the user to be logged in
    users_list = um.load_users()
    for user in users_list:
        if user['username'] == username:
            id = user['id']

    # check if the username and password entered is correct then either log in or flash an error message
    if um.login(username, password):
        session['user'] = id
        return redirect('/dashboard')
    else:
        flash('Incorrect username or password', 'error')
        return redirect('/login')


def check_login():
    """If the user is currently logged in there will be a user variable in the seesion"""
    if 'user' not in session:
        abort(401)  # Unauthorised


def get_user_index():
    users_list = um.load_users()
    for index in range(len(users_list)):
        if users_list[index]['id'] == session['user']:
            target_index = index
    return target_index


def load_user_data():
    # loads the pets json file as an array of dictionaries
    with open(f"user_data/{session['user']}.json") as f:
        user_data = json.load(f)
    return user_data


def save_user_data(user_data_list):
    # Saves the given list of dictionaries to pets/user.json
    with open(f"user_data/{session['user']}.json", 'w') as f:
        json.dump(user_data_list, f, indent=4)


def load_adoption():
    with open("adoption.json") as f:
        pets_adoption = json.load(f)
    return pets_adoption


def save_adopted_pets(pets_adoption_list):
    # Saves the given list of dictionaries to adoption.json
    with open("adoption.json", 'w') as f:
        json.dump(pets_adoption_list, f, indent=4)


def time_since_last_exercise(name, birthday, activities):
    # Get current date
    current_date = date.today()

    # convert birthday to datetime module
    birthday = datetime.strptime(birthday, '%Y-%m-%d')

    # search to find the date with the lowest difference in comparision to the current date
    difference = current_date - birthday.date()

    for activity in activities:
        # check to see if the particular pet was being taken on the exercise
        if name in activity['pets_taken']:
            activity_date = datetime.strptime(
                activity['date'], '%Y-%m-%d').date()
            diff = current_date - activity_date
            if diff < difference:
                difference = diff

    # time since last exercise in days
    difference = difference.days

    return difference


def admiration_points(time, name, birthday):
    # convert the overall time originally in minutes into hours (integers not floats)
    time = time // 60

    # load activities for time_since_last_exercise
    user_data = load_user_data()
    activities = user_data['activities']

    # for every week of innactivity (from current date) retract 10 EXP/ 1 hour
    time_passed = time_since_last_exercise(name, birthday, activities)

    # convert time passed time to weeks - reduction
    reduction = time_passed // 7

    time = time - reduction

    # for every hour of activity equates to 10 admiration points (EXP)
    points = time * 10

    points = points / 1000

    # points cannot exceed 1000 or be lower than 0
    # keep in mind points are calculated between 0 and 1
    if points > 1:
        points = 1
    elif points < 0:
        points = 0

    # determine the relationship level between user and pet based on point amount
    relationship = "Acquainted"
    if points >= 0.1: # equivalent to 100
        relationship = "Closely Acquainted"
    if points >= 0.22: # equivalent to 220
        relationship = "Friends"
    if points >= 0.36: # equivalent to 360
        relationship = "Close Friends"
    if points >= 0.54: # equivalent to 540
        relationship = "Best Friends"
    if points >= 0.74: # equivalent to 740
        relationship = "Soulmates"

    return points, relationship


def pet_emotion(emotion, name, birthday):
    # load activities
    user_data = load_user_data()
    activities = user_data["activities"]

    # INCREASE EMOTION
    # find all exercises of whose dates have a difference less than or equal to seven from the current date

    # Get current date
    current_date = date.today()

    # loop through activities to find all dates with a difference of 7 days or less IF the pet is taken on that exercise
    count = 0
    for activity in activities:
        if name in activity['pets_taken']:
            act_date = datetime.strptime(activity['date'], '%Y-%m-%d')
            difference = current_date - act_date.date()
            if difference.days <= 7:
                count += 1

    # set new emotion to the current emotion of pet which changes later on if points added
    new_emotion = emotion

    # for the number of exercises done per week, increase emotion if count >= 5
    # becuse it's suggested you do some form of exercise everyday i felt that 5 was good.... maybe?
    if count >= 5:
        if emotion == "shy" or "sad":
            new_emotion = "neutral"
        elif emotion == "neutral":
            new_emotion = "happy"

    # DETERIORATE EMOTION
    # for every 2 weeks of innactivity, emotion deteriorates

    # check to see how long it has been since last entry
    time_passed = time_since_last_exercise(name, birthday, activities)

    # convert days to week
    weeks_passed = time_passed // 7

    deteriorations = weeks_passed // 2

    if deteriorations >= 1:
        if emotion == "shy" or emotion == "neutral":
            new_emotion = "sad"
        elif emotion == "happy":
            new_emotion = "neutral"

    return new_emotion


@app.get('/dashboard')
def display_dashboard():
    check_login()

    # get the users pets
    user_data = load_user_data()
    pets = user_data["pets"]

    num_pets = 0

    for pet in pets:
        num_pets += 1
        pet["points"], pet["relationship"] = admiration_points(
            pet["time"], pet["name"], pet["birthday"])
        pet['emotion'] = pet_emotion(
            pet['emotion'], pet['name'], pet['birthday'])

    # saves the pets list to the user_data dictionary which is then saved to the users json file (activities is unnafected)

    # saves list of pets to dictionary under the pet key
    user_data['pets'] = pets

    # saves dictionary to json file
    save_user_data(user_data)
    
    target_pet = -1

    try:
        # Get the id of the pet selected for display from the URL using request.args['id']
        pet_id = int(request.args['id'])

        # use id to save the target pet
        for pet in pets:
            if pet['id'] == pet_id:
                target_pet = pet
    except:
        pass

    return render_template("dashboard.html", pets=pets, num_pets=num_pets, target_pet=target_pet)


@app.get('/create')
def display_create():
    check_login()

    return render_template("create.html")


@app.post('/create')
def create():
    check_login()
    user_data = load_user_data()
    pets = user_data['pets']

    # double check the user has not reached the maximum amount of pets (including this newly created pet) which is 2
    num_pets = len(pets)
    if num_pets < 2:
        name = request.form['pet-name']
        species = request.form['species']

        # select a random personality for the pet
        personalities = ["Timid", "Confident",
                         "Independent", "Laidback", "Social", "Grumpy", "Sweet", "Cautious", "Feisty", "Bubbly", "Aloof", "Curious", "Playful", "Individualistiic", "Loyal", "Enthusiastic", "Easy-Going", "Chill", "Adventurous", "Affectionate", "Cheeky", "Ambitious", "Bold"]
        personality = random.choice(personalities)

        # Get current date to add as the pets birthday
        # MAKE SURE TO STRING THE DATE WHEN ADDING IT!
        current_date = str(date.today())

        # set constant data for the pet - consistent with every pet creation
        id = num_pets + 1
        time = 0
        points = 0
        relationship = "Acquainted"
        emotion = "shy"

        new_pet = {
            "id": id,
            "name": name,
            "personality": personality,
            "time": time,
            "points": points,
            "relationship": relationship,
            "species": species,
            "emotion": emotion,
            "birthday": current_date
        }

        pets.append(new_pet)

        # saves the pets list to the user_data dictionary which is then saved to the users json file (activities is unnafected)

        # saves list of pets to dictionary under the pet key
        user_data['pets'] = pets

        # saves dictionary to json file
        save_user_data(user_data)

        flash('You have successfuly created a buddEE!', 'info')
        return redirect('/dashboard')
    else:
        flash('You have already reached the limit on how many pets you can have', 'error')
        return redirect('/dashboard')


@app.get('/activity')
def display_activity():
    check_login()

    # get the users activities
    user_data = load_user_data()
    activities = user_data['activities']

    # add up the number of hours and minutes the user has
    time = 0

    for activity in activities:
        time += activity['time']

    hours = time // 60
    minutes = time % 60

    return render_template("activity.html", activities=activities, hours=hours, minutes=minutes)


@app.get('/addactivity')
def display_add_activity():
    check_login()
    return render_template("addactivity.html")


@app.post('/addactivity')
def add_activity():
    check_login()

    user_data = load_user_data()
    # load activities (specific to user)
    activities = user_data['activities']

    # load pets for future use (aka adding time)
    pets = user_data['pets']

    num_pets = len(pets)

    # user must have a pet to add an activity
    if num_pets > 0:
        # rquest data from form to add to json file
        date = request.form['date']
        hours = int(request.form['hours'])
        minutes = int(request.form['minutes'])
        activity = request.form['activity']

        # convert hours to minutes and add that to the minutes to get the overall time (in minutes)
        hours_to_minutes = hours * 60
        time = hours_to_minutes + minutes

        # add the overall time to each pet
        for pet in pets:
            pet['time'] += time

        # create an array of the names of the pets the user currently has aka the pets taken on the exercise
        pet_name_list = []

        for pet in pets:
            pet_name_list.append(pet['name'])

        # generate a unique and random id number for this activity
        complete = False
        while complete == False:
            num = random.randint(1, 1000)
            found = False

            for act in activities:
                if num == act['id']:
                    found = True

            if found == False:
                id = num
                complete = True

        new_activity = {
            "id": id,
            "date": date,
            "time": time,
            "activity": activity,
            "pets_taken": pet_name_list
        }

        activities.append(new_activity)

        # saves list of activities to dictionary under the acivities key and the pet times under the pet dictionary
        user_data['pets'] = pets
        user_data['activities'] = activities

        # saves dictionary to json file
        save_user_data(user_data)

        flash('You have successfully added a new activity!', 'info')
        return redirect('/activity')
    else:
        flash('You must have at least ONE pet to add an activity', 'error')
        return redirect('/activity')


@app.get('/editactivity')
def display_edit_activity():
    check_login()

    # Get the id of the activity from the URL using request.args['id']
    id = int(request.args['id'])

    # Open the activity list and find the dict with the id
    user_data = load_user_data()
    activities = user_data['activities']

    for activity in activities:
        if activity['id'] == id:
            target_activity = activity

    # Pass in the specific dict to the editactivity.html template
    return render_template('editactivity.html', activity=target_activity)


@app.post('/editactivity')
def edit_activity():
    check_login()

    # Get the id of the activity from the POSTed form using request.form['id']
    id = int(request.form['id'])

    # Open the activity list and find the dict with the id
    user_data = load_user_data()
    activities = user_data['activities']
    pets = user_data['pets']

    for index in range(len(activities)):
        if activities[index]['id'] == id:
            target_index = index

    # Use the POSTed form data to make changes in that activity
    activities[target_index]['date'] = request.form['date']
    activities[target_index]['activity'] = request.form['activity']

    # get the overall time and check the difference between the last time to make adjustments in the pets
    hours = int(request.form['hours'])
    minutes = int(request.form['minutes'])

    # convert hours to minutes and add that to the minutes to get the overall time (in minutes)
    hours_to_minutes = hours * 60
    time = hours_to_minutes + minutes

    if time < activities[target_index]['time']:
        # for every pet in the pets_taken list, subtract the time difference from their time
        for pet_name in activities[target_index]['pets_taken']:
            for pet in pets:
                if pet['name'] == pet_name:
                    time_diff = activities[target_index]['time'] - time
                    pet['time'] -= time_diff
    else:
        # for every pet in the pets_taken list, add the time difference to their time
        for pet_name in activities[target_index]['pets_taken']:
            for pet in pets:
                if pet['name'] == pet_name:
                    time_diff = time - activities[target_index]['time']
                    pet['time'] += time_diff

    activities[target_index]['time'] = time

    # saves list of activities to dictionary under the acivities key and the pet times under the pet dictionary
    user_data['pets'] = pets
    user_data['activities'] = activities

    # saves dictionary to json file
    save_user_data(user_data)

    flash(
        f"Activity: {request.form['activity']} {request.form['date']} successfully updated")
    return redirect('/activity')


@app.get('/deleteactivity')
def display_delete_activity():
    check_login()

    # Get the id of the activity from the URL using request.args['id']
    id = int(request.args['id'])

    # Open the activity list and find the dict with the id
    user_data = load_user_data()
    activities = user_data['activities']

    for activity in activities:
        if activity['id'] == id:
            target_activity = activity

    # Pass in the specific dict to the editactivity.html template
    return render_template('deleteactivity.html', activity=target_activity)


@app.post('/deleteactivity')
def delete_activity():
    check_login()

    # Get the id of the activity from the URL using request.form['id']
    id = int(request.form['id'])

    # Open the activity list and find the dict with the id
    user_data = load_user_data()
    activities = user_data['activities']
    pets = user_data['pets']

    for index in range(len(activities)):
        if activities[index]['id'] == id:
            target_index = index

    # Store the info of the activity to be deleted
    date = activities[target_index]['date']
    activity = activities[target_index]['activity']

    # remove the amount of time in the activity to be deleted from the pets
    time = activities[target_index]['time']

    # for every pet in the pets_taken list, subtract the time difference from their time
    for pet_name in activities[target_index]['pets_taken']:
        for pet in pets:
            if pet['name'] == pet_name:
                pet['time'] -= time

    # Delete the activity from activities
    del activities[target_index]

    # saves list of activities to dictionary under the acivities key and the pet times under the pet dictionary
    user_data['activities'] = activities
    user_data['pets'] = pets

    # saves dictionary to json file
    save_user_data(user_data)

    flash(f'Activity: {activity} {date} has been deleted.')
    return redirect('/activity')


@app.get('/adoption')
# for now: displaying as a table (aspirational feature being a searching system)
def display_adoption():
    check_login()

    # get the list of pets to display
    pets_adoption = load_adoption()

    return render_template('adoption.html', pets_adoption=pets_adoption)


@app.get('/confirmadopt')
def display_confirm_adopt():
    check_login()

    # Get the id of the pet from the URL using request.args['id']
    id = int(request.args['id'])

    # Open the adoption list and find the dict with the id
    pets_adoption = load_adoption()

    for pet in pets_adoption:
        if pet['id'] == id:
            target_pet = pet

    # Pass in the specific dict to the confirmadopt.html template
    return render_template('confirmadopt.html', buddEE=target_pet)


@app.post('/confirmadopt')
def confirm_adopt():
    check_login()

    # Get the id of the buddEE from the URL using request.form['id']
    id = int(request.form['id'])

    # get the users user_data (for pets) and the current adoption list
    user_data = load_user_data()
    pets = user_data['pets']

    pets_adopted = load_adoption()

    # get index of the soon-to-be adopted pet
    for index in range(len(pets_adopted)):
        if pets_adopted[index]['id'] == id:
            target_index = index

    # save all the information about the pet to be adopted and place it in the users dict (if they have less than 2 pets)
    if len(pets) < 2:
        name = pets_adopted[target_index]['name']
        personality = pets_adopted[target_index]['personality']
        species = pets_adopted[target_index]['species']
        birthday = pets_adopted[target_index]['birthday']

        # set constant data for the pet - consistent with every pet creation
        pet_id = len(pets) + 1
        time = 0
        points = 0
        relationship = "Acquainted"
        emotion = "shy"

        adopted_pet = {
            "id": pet_id,
            "name": name,
            "personality": personality,
            "time": time,
            "points": points,
            "relationship": relationship,
            "species": species,
            "emotion": emotion,
            "birthday": birthday
        }

        pets.append(adopted_pet)

        user_data['pets'] = pets
        # saves dictionary to json file
        save_user_data(user_data)

        # delete the pet from the adoption list
        del pets_adopted[target_index]

        save_adopted_pets(pets_adopted)

        flash(f'You have successfully adopted {name}, Congrats!', 'info')
        return redirect('/dashboard')
    else:
        flash('You have already reached the limit on how many pets you can have', 'error')
        return redirect('/dashboard')


@app.get('/account')
def display_account():
    check_login()

    index = get_user_index()

    users_list = um.load_users()
    user = users_list[index]

    return render_template('account.html', user=user)


@app.post('/editusername')
def edit_username():
    check_login()
    # collect the filled out form and check for any changes using function in um
    new_username = request.form['username']

    users_list = um.load_users()

    target_index = get_user_index()

    # if the new username differ to the current username, change it (as long as there isnt a user with the same name)
    if um.user_exists(new_username) and new_username == users_list[target_index]['username']:
        # the user already has this exact username
        flash('Cannot change to username you already have.', 'error')
        return redirect('/account')
    elif um.user_exists(new_username) == False:
        # username is unique
        if new_username != "" and new_username != " ":
            # username is not empty
            um.change_username(target_index, new_username)
            flash('username has been changed', 'info')
            return redirect('/account')
        else:
            # username IS empty
            flash('username cannot be empty', 'error')
            return redirect('/account')
    else:
        # username is already taken
        flash('That username is already taken.', 'error')
        return redirect('/account')


@app.post('/editpassword')
def edit_password():
    check_login()
    # collect the filled out form and check for any changes using function in um
    new_password = request.form['password']

    target_index = get_user_index()

    # as long as the new password is not nothing and not just a space it is valid
    if new_password != "" and new_password != " ":
        # new password is not empty - you can change it
        um.change_password(target_index, new_password)
        flash('password has been changed', 'info')
        return redirect('/account')
    else:
        flash('password cannot be empty', 'error')
        return redirect('/account')


@app.get('/deleteaccount')
def display_delete_account():
    check_login()

    index = get_user_index()

    users_list = um.load_users()
    user = users_list[index]

    return render_template('deleteaccount.html', user=user)


@app.post('/deleteaccount')
def delete_account():
    check_login()

    user_id = session['user']

    index = get_user_index()

    users_list = um.load_users()
    username = users_list[index]['username']

    # get the users current pets to add to the adoption.json file
    user_data = load_user_data()
    pets = user_data['pets']

    adoption_list = load_adoption()

    for pet in pets:
        # save all pet info
        name = pet['name']
        personality = pet['personality']
        species = pet['species']
        birthday = pet['birthday']

        # generate a unique and random id number for the pet
        complete = False
        while complete == False:
            num = random.randint(1, 1000)
            found = False

            for adoption_pet in adoption_list:
                if num == adoption_pet['id']:
                    found = True

            if found == False:
                id = num
                complete = True

        new_adoption_pet = {
            "id": id,
            "name": name,
            "personality": personality,
            "species": species,
            "birthday": birthday
        }

        # append pet to the adoption_list
        adoption_list.append(new_adoption_pet)

    # save the adoption list
    save_adopted_pets(adoption_list)

    # pop the user's sesion
    session.pop('user', None)

    um.delete_account(user_id)

    # deletion of the user_data json file using os import
    os.remove(f"user_data/{user_id}.json")

    flash(
        f'You have successfully deleted your account {username}, we are sad to see you go!', 'info')
    return redirect('/')


@app.errorhandler(401)
def unauthorized(code):
    return render_template('401.html'), 401


@app.errorhandler(404)
def not_found(code):
    return render_template('404.html'), 404


@app.get('/logout')
def sign_out():
    session.pop('user', None)
    flash('You have successfully logged out!', 'info')
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True, port=5001)

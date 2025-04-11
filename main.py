import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
from dotenv import load_dotenv
import re
from functools import wraps


# Load environment variables from .env file
load_dotenv()

# Initialize the flask app
app = Flask(__name__)
app.secret_key = os.getenv("SECRET")


# ------------------------ BEGIN FUNCTIONS ------------------------ #
# Function to retrieve DB connection
def get_db_connection():
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_DATABASE"),
    )
    return conn

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash("You must be logged in to view this page.", "error")
            return redirect(url_for("login"))  # Redirect to login page if not logged in
        return f(*args, **kwargs)
    return wrapper

# Get all items from the "items" table of the db
# def get_all_items():
#     # Create a new database connection for each request
#     conn = get_db_connection()  # Create a new database connection
#     cursor = conn.cursor() # Creates a cursor for the connection, you need this to do queries
#     # Query the db
#     query = "SELECT name, quantity FROM items"
#     cursor.execute(query)
#     # Get result and close
#     result = cursor.fetchall() # Gets result from query
#     conn.close() # Close the db connection (NOTE: You should do this after each query, otherwise your database may become locked)
#     return result

# def get_all_building_names():
#     # Create a new database connection for each request
#     conn = get_db_connection()  # Create a new database connection
#     cursor = conn.cursor() # Creates a cursor for the connection, you need this to do queries
#     # Query the db
#     query = "SELECT BuildingName FROM BUILDING"
#     cursor.execute(query)
#     # Get result and close
#     result = cursor.fetchall() # Gets result from query
#     conn.close() # Close the db connection (NOTE: You should do this after each query, otherwise your database may become locked)
#     return [row[0] for row in result]

def get_all_building_names_and_ids():
    # Create a new database connection for each request
    conn = get_db_connection()  # Create a new database connection
    cursor = conn.cursor() # Creates a cursor for the connection, you need this to do queries
    # Query the db
    query = "SELECT BuildingID, BuildingName FROM BUILDING"
    cursor.execute(query)
    # Get result and close
    result = cursor.fetchall() # Gets result from query
    conn.close() # Close the db connection (NOTE: You should do this after each query, otherwise your database may become locked)
    print('look go')
    print(result)
    return result
    
    # return [row[0] for row in result]

# def get_results():
#     # Create a new database connection for each request
#     selected_building_id = session['selected_building_id']
#     selected_type = session['selected_type']
#     selected_gender = session['selected_gender']
#     conn = get_db_connection()  # Create a new database connection
#     cursor = conn.cursor() # Creates a cursor for the connection, you need this to do queries
#     # Query the db
#     query = "SELECT BuildingID, FloorNumber, RoomNumber, Rating FROM Clean_Squat.PreferencesView WHERE BuildingID = %s AND IsPrivate = %s AND Gender = %s ORDER BY CleaningTimeStamp DESC LIMIT 1"
#     cursor.execute(query, (selected_building_id, selected_gender, selected_type))
#     # Get result and close
#     result = cursor.fetchall() # Gets result from query
#     conn.close() # Close the db connection (NOTE: You should do this after each query, otherwise your database may become locked)
#     print("this is the result:")
#     print(result)
#     return result

# def get_results():
#     selected_building_id = session['selected_building_id']
#     selected_type = session['selected_type']
#     selected_gender = session['selected_gender']

#     conn = get_db_connection()
#     cursor = conn.cursor()

#     # Base query to join Buildings and PreferencesView
#     if selected_gender is None:
#         query = """
#         SELECT b.BuildingName, p.FloorNumber, p.RoomNumber, p.Rating
#         FROM Clean_Squat.PreferencesView p
#         JOIN Clean_Squat.BUILDING b ON p.BuildingID = b.BuildingID
#         WHERE p.BuildingID = %s AND p.IsPrivate = %s AND p.Gender IS NULL
#         ORDER BY p.CleaningTimeStamp DESC
#         LIMIT 1
#         """
#         cursor.execute(query, (selected_building_id, selected_type))
#     else:
#         query = """
#         SELECT b.BuildingName, p.FloorNumber, p.RoomNumber, p.Rating
#         FROM Clean_Squat.PreferencesView p
#         JOIN Clean_Squat.BUILDING b ON p.BuildingID = b.BuildingID
#         WHERE p.BuildingID = %s AND p.IsPrivate = %s AND p.Gender = %s
#         ORDER BY p.CleaningTimeStamp DESC
#         LIMIT 1
#         """
#         cursor.execute(query, (selected_building_id, selected_type, selected_gender))

#     result = cursor.fetchall()
#     conn.close()
#     print
#     return result

def get_results():
    
    
    selected_building_id = session['selected_building_id']
    selected_type = session['selected_type']
    selected_gender = session['selected_gender']

    conn = get_db_connection()
    cursor = conn.cursor()

    # Base query to join Buildings and PreferencesView
    if selected_gender is None:
        query = """
        SELECT b.BuildingName, p.FloorNumber, p.RoomNumber, p.Rating, p.RestroomID
        FROM Clean_Squat.PreferencesView p
        JOIN Clean_Squat.BUILDING b ON p.BuildingID = b.BuildingID
        WHERE p.BuildingID = %s AND p.IsPrivate = %s AND p.Gender IS NULL
        ORDER BY p.CleaningTimeStamp DESC
        LIMIT 1
        """
        cursor.execute(query, (selected_building_id, selected_type))
    else:
        query = """
        SELECT b.BuildingName, p.FloorNumber, p.RoomNumber, p.Rating, p.RestroomID
        FROM Clean_Squat.PreferencesView p
        JOIN Clean_Squat.BUILDING b ON p.BuildingID = b.BuildingID
        WHERE p.BuildingID = %s AND p.IsPrivate = %s AND p.Gender = %s
        ORDER BY p.CleaningTimeStamp DESC
        LIMIT 1
        """
        cursor.execute(query, (selected_building_id, selected_type, selected_gender))

    result = cursor.fetchall()

    # Save restroom ID to session for later use
    if result:
        session["selected_restroom_id"] = result[0][4]
    
   # Get average rating for the specific restroom being shown
    selected_restroom_id = result[0][4]  # Fetch the RestroomID from the result

    query_avg = """
    SELECT AVG(p.Rating)
    FROM Clean_Squat.PreferencesView p
    WHERE p.RestroomID = %s
    """
    cursor.execute(query_avg, (selected_restroom_id,))
    avg_rating = cursor.fetchone()[0]

    # Round average rating to 1 decimal place
    avg_rating = round(avg_rating, 1)

    # Debug: Print average rating
    print("DEBUG: Average Rating Retrieved =", avg_rating)

    conn.close()
    return result, avg_rating



# ------------------------ END FUNCTIONS ------------------------ #


# ------------------------ BEGIN ROUTES ------------------------ #
# EXAMPLE OF GET REQUEST

# When looking to display items dynamically, add < , items=items > as an argument in the return render_template()
# like this: < return render_template("index.html", items=items) >.
# this will allow jinga2 to take that argument as something it can use to prepare the information it needs to dsiplay.

#This route renders the index page of our website, which is the login page.
@app.route("/", methods=["GET"])
def index():
    #items = get_all_items() # Call defined function to get all items
    return render_template("index.html") 


#This route renders the registration page of the website.
# @app.route("/register", methods=["GET"])
# def register():
#     #items = get_all_items() # Call defined function to get all items
#     return render_template("clean_squat_register.html")  


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Get data from the registration form
        username = request.form["username"]
        password = request.form["password"]
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        
        role = "USER"  # Default role for new users
        print(f"Registering: {username}, {password}, {first_name}, {last_name}")

        # Validate the password
        if not validate_password(password):
            flash("Password must be at least 8 characters long, contain at least one uppercase letter, one lowercase letter, and one number.", "error")
            return redirect(url_for("register"))
        
        # Check if the username already exists
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Clean_Squat.USER WHERE Username = %s", (username,))
        existing_user = cursor.fetchone()  # Fetch one row if a match is found
        
        if existing_user:
            flash("Username already taken. Please choose another username.", "error")
            cursor.close()
            conn.close()
            return redirect(url_for("register"))  # Return to registration page

        try:
            # Connect to the database and insert the new user
            conn = get_db_connection()
            cursor = conn.cursor()

            # Insert user data into the database
            cursor.execute("""
                INSERT INTO Clean_Squat.USER (Username, Password, FirstName, LastName, Role)
                VALUES (%s, %s, %s, %s, %s)
            """, (username, password, first_name, last_name, role))  # Password is stored as plain text
            conn.commit()  # Commit the transaction
            cursor.close()
            conn.close()

            flash("User registered successfully!", "success")

            # Log the user in immediately after registration
            session['username'] = username  # Store the username in the session
            return redirect(url_for("index"))  # Redirect to the index page after successful registration

        except mysql.connector.Error as err:
            flash(f"MySQL Error: {err}", "error")
            return redirect(url_for("register"))
        except Exception as e:
            flash(f"Error: {str(e)}", "error")
            return redirect(url_for("register"))

    return render_template("register.html")  # Render the registration page


# Password validation function
def validate_password(password):
    # Password must be at least 8 characters, contain at least one uppercase letter, one lowercase letter, and one number
    import re
    pattern = re.compile("^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).{8,}$")
    return bool(pattern.match(password))





# Login route
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Connect to the database and check if the user exists
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Clean_Squat.USER WHERE Username = %s AND Password = %s", (username, password))
        user = cursor.fetchone()  # Fetch the user details if they exist

        cursor.close()
        conn.close()

        if user:
            # Store the user info in session (assuming user[0] is the UserID, user[1] is Username, and user[4] is the Role)
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['role'] = user[5]  # Assuming user[4] is the role column

            print(f"User Role: {session['role']}")  # Debugging: Check the role being stored in session

            #flash("Login successful!", "success")

            # Redirect based on user role
            if session['role'] == 'SUPERVISOR':
                print("Redirecting to Staff Dashboard")  # Debugging
                return redirect(url_for("staff_dashboard"))
            elif session['role'] == 'STAFF': 
                return redirect(url_for("staff_dashboard")) # Redirect to admin dashboard if user is an admin
            else:
                print("Redirecting to User Dashboard")  # Debugging
                return redirect(url_for("main"))  # Redirect to user dashboard if user is a regular user

        else:
            flash("Invalid username or password", "error")
            return redirect(url_for("login"))  # Stay on login page if credentials are incorrect

    return render_template("index.html")  # Render the login page

@app.route("/admin_dashboard", methods=["GET"])

def admin_dashboard():
    return render_template("admin_dashboard.html")

@app.route("/logout")
def logout():
    session.pop('user_id', None)  # Remove the user_id from the session
    session.pop('username', None)  # Remove the username from the session
    #flash("You have been logged out.", "success")
    return redirect(url_for("index"))  # Redirect to the index page after logout


#This route renders the main page of our website that allows users to input information to find a restroom or report an issue.
@app.route("/main", methods=["GET"])
@login_required
def main():
    #items = get_all_items() # Call defined function to get all items
    return render_template("clean_squat_main.html")


#This route renders the select building page of the website.
@app.route("/select_building", methods=["GET", "POST"])
@login_required
def select_building():
    if request.method == "POST":
        selected_building_id = request.form.get("building")  # Get the selected building from the form
        if selected_building_id:
            session["selected_building_id"] = selected_building_id  # Store the building in the session
        
        flash("Building Selected!", "success")
       # Redirect based on role
        # if session.get("role") in ["STAFF", "SUPERVISOR"]:
        #     return redirect(url_for("admin_dashboard"))  # Redirect to admin dashboard if the user is staff or supervisor
        # else:
        #     return redirect(url_for("main"))  # Red
        #  Redirect to main page after selecting the building
    list_of_buildings = get_all_building_names_and_ids() # Call defined function to get all items
    
    return render_template("clean_squat_bldg_select.html", buildings=list_of_buildings)  


#This route renders the restroom prefrences page of the website where users can select the prefrences they want for a restroom.
@app.route("/select_preferences", methods=["GET", "POST"])
@login_required
def select_preferences():
    if request.method == "POST":
        selected_type = request.form.get("type")  # "public" or "private"
        selected_gender = request.form.get("gender")  # "male", "female", or None

        # Convert selected_type to boolean
        if selected_type == "private":
            selected_type = True
            selected_gender = None  # Set gender to None if private
        elif selected_type == "public":
            selected_type = False
            # Gender remains whatever was submitted

        # Store in session
        session["selected_type"] = selected_type
        session["selected_gender"] = selected_gender

        print("Type:", selected_type)
        print("Gender:", selected_gender)

        flash("Preferences Selected!", "success")

        # if session.get("role") in ["STAFF", "SUPERVISOR"]:
        #     return redirect(url_for("admin_dashboard"))  # Redirect to admin dashboard if the user is staff or supervisor
        # else:
        #     return redirect(url_for("main")) # Red  # Redirect after form submission

    all_sessions = dict(session)
    print("This is your session dictionary:")
    print(all_sessions)
    return render_template("clean_squat_preferences.html")
    


#This route renders results page of the website, showing users the bathroom that matches their preferences.
@app.route("/results", methods=["GET"])
@login_required
def results():
    # Check if building and preferences are selected
    if "selected_building_id" not in session:
        flash("Please select a building before proceeding.")
        return redirect(url_for("main"))  # Redirect to select building page

    if "selected_type" not in session or "selected_gender" not in session:
        flash("Please select your preferences before proceeding.")
        return redirect(url_for("main"))  # Redirect to select preferences page
    
    results, avg_ratings = get_results() # Call defined function to get all results
    if not results:
        return redirect(url_for('sorry'))
    return render_template("clean_squat_results.html", result=results, avg_rating=avg_ratings)   # Show results for regular users


#This route renders the rating page, where users can rate the restrooms they visited. 
@app.route("/rating", methods=["GET", "POST"])
@login_required
def rating():
    if request.method == "POST":
        rating_value = request.form.get('rating')
        restroom_id =  session.get("selected_restroom_id") #request.form.get('restroom_id') 
        user_id = session.get("user_id")

        print(f"POST request received: rating_value={rating_value}, restroom_id={restroom_id}, user_id={user_id}")

        # Only check if rating is missing
        if not rating_value:
            flash("Please select a rating before submitting.")
            return redirect(url_for("rating"))  # Stay on the same page"))

        try:
            rating_value = int(rating_value)
            restroom_id = int(restroom_id)
            if rating_value < 1 or rating_value > 5:
                flash("Rating must be between 1 and 5.")
                return redirect(url_for("results"))
        except ValueError:
            flash("Invalid rating value.")
            return redirect(url_for("results"))

        # Handle rating logic
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if the user has already rated this restroom
         # Always update the rating or insert a new one
        cursor.execute("""
            INSERT INTO Clean_Squat.RATING (Rating, UserID, RestroomID) 
            VALUES (%s, %s, %s) 
            ON DUPLICATE KEY UPDATE Rating = VALUES(Rating)
        """, (rating_value, user_id, restroom_id))
        flash("Thanks for rating!")

        conn.commit()
        conn.close()

        return redirect(url_for("results"))

    # Handle GET request to show the rating page
    return render_template("rating.html")




#This route renders the page that allows staff to navigate to two different pages, one to report cleaning, and the other to see reported issues.
@app.route("/staff_dashboard", methods=["GET"])
@login_required
def staff_dashboard():
    #items = get_all_items() # Call defined function to get all items
    return render_template("staff_dash.html")


#This route renders the page that allows staff to view all reported issues.
@app.route("/staff_issue_portal", methods=["GET"])
@login_required
def staff_issue_portal():
    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get all issues, including their updated status
    cursor.execute("""
        SELECT IssueID, Description, CompletionStatus
        FROM Clean_Squat.ISSUEREPORT
    """)
    issues = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("staff_issue_portal.html", issues=issues)


#This view is not rendering currently but I think Kristina might still be working on it - Daniel
# Sample backend code
@app.route('/selected_issue/<int:issue_id>', methods=['GET'])
def selected_issue(issue_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT i.IssueID, i.Description, i.CompletionStatus, b.BuildingName, p.FloorNumber, p.RoomNumber, i.ReportTimeStamp
        FROM Clean_Squat.ISSUEREPORT i
        JOIN Clean_Squat.RESTROOM p ON i.RestroomID = p.RestroomID
        JOIN Clean_Squat.BUILDING b ON p.BuildingID = b.BuildingID
        WHERE i.IssueID = %s
    """, (issue_id,))
    issue = cursor.fetchone()

    if issue:
        timestamp = issue[6]  # This is the timestamp value
        formatted_timestamp = timestamp.strftime('%B %d, %Y at %I:%M %p')  # Example format: 'December 25, 2021 at 03:30 PM'
        issue = list(issue)  # Convert tuple to list to modify it
        issue[6] = formatted_timestamp
    cursor.close()
    conn.close()

    return render_template('selected_issue.html', issue=issue)




@app.route("/report_an_issue", methods=["GET", "POST"])
@login_required
def report_an_issue():
    # Retrieve query parameters from the URL (GET request)
    building_name = request.args.get("building")
    floor_number = request.args.get("floor")
    room_number = request.args.get("room")

    # Print the query parameters to check their values
    print(f"GET Parameters: building_name={building_name}, floor_number={floor_number}, room_number={room_number}")

    if request.method == "POST":
        # Get form data from POST request (data submitted by the user)
        description = request.form["description"]
        timestamp = request.form["timestamp"]

        # Get hidden form data (values passed from GET request and pre-filled in the form)
        building_id = request.form["building_id"]
        floor = request.form["floor"]
        room = request.form["room"]

        # Print form data to check if the correct values are being passed
        print(f"POST Form Data: building_id={building_id}, floor={floor}, room={room}")

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            # Query to get the RestroomID for the selected BuildingID, FloorNumber, and RoomNumber
            cursor.execute("""
                SELECT RestroomID 
                FROM Clean_Squat.RESTROOM 
                WHERE BuildingID = %s AND FloorNumber = %s AND RoomNumber = %s
            """, (building_id, floor, room))
            restroom_id = cursor.fetchone()

            # Print the query result for debugging
            print(f"RestroomID: {restroom_id}")

            if not restroom_id:
                # If no RestroomID is found, flash an error message and redirect back to the form
                flash("No matching restroom found for the selected building, floor, and room.", "error")
                return redirect(url_for("report_an_issue"))

            # Proceed with inserting the issue, using the RestroomID
            restroom_id = restroom_id[0]  # Get the actual value of RestroomID
            cursor.execute("""
                INSERT INTO Clean_Squat.ISSUEREPORT (Description, CompletionStatus, ReportTimeStamp, RestroomID)
                VALUES (%s, %s, %s, %s)
            """, (description, False, timestamp, restroom_id))  # CompletionStatus is set to False initially

            # Commit the transaction
            conn.commit()

            # Flash success message after the cleaning report is successfully submitted
            flash("Successfully submitted issue report!", "success")

            # Redirect to the same page after successful submission, so the user stays on the page with the flash message
            return redirect(url_for("report_an_issue"))

        except mysql.connector.Error as err:
            # Catch MySQL errors
            flash(f"An error occurred while submitting the issue: {err}", "error")
            return redirect(url_for("report_an_issue"))

        except Exception as e:
            # Catch general exceptions
            flash(f"An unexpected error occurred: {str(e)}", "error")
            return redirect(url_for("report_an_issue"))

        finally:
            cursor.close()
            conn.close()

    # GET request: Fetch all buildings to display in the dropdown (if needed)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT BuildingID, BuildingName FROM Clean_Squat.BUILDING")
    buildings = cursor.fetchall()  # Fetch all buildings
    cursor.close()
    conn.close()

    # Return the template with the necessary values (building, floor, room, etc.)
    return render_template(
        "report_an_issue.html",
        buildings=buildings,
        building_name=building_name,
        floor_number=floor_number,
        room_number=room_number,
    )


#Do we need an additional view to display the update issue status? I honestly don't know
#I think it could be some language on the selected issue route that just sends a ALERT query 
# to update to completed status and then it runs a SELECT after that to update the page? -Daniel
@app.route("/update_issue_status/<int:issue_id>/<int:status>", methods=["POST"])
def update_issue_status(issue_id, status):
    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Update the issue status in the database
        cursor.execute("""
            UPDATE Clean_Squat.ISSUEREPORT 
            SET CompletionStatus = %s 
            WHERE IssueID = %s
        """, (status, issue_id))

        # Commit the changes
        conn.commit()
        flash("Issue status updated successfully!", "success")
        return redirect(url_for("staff_issue_portal"))  # Redirect back to the staff issue portal

    except mysql.connector.Error as err:
        flash(f"Error: {err}", "error")
        return redirect(url_for("staff_issue_portal"))

    finally:
        cursor.close()
        conn.close()


@app.route('/confirm_delete/<int:issue_id>', methods=['GET', 'POST'])
def confirm_delete(issue_id):
    if request.method == 'POST':
        # Redirect to the delete_issue route to actually delete the issue
        return redirect(url_for('delete_issue', issue_id=issue_id))
    return render_template('confirm_delete.html', issue_id=issue_id)


@app.route('/delete_issue/<int:issue_id>', methods=['POST'])
def delete_issue(issue_id):
    # Delete the issue from the database
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Clean_Squat.ISSUEREPORT WHERE IssueID = %s", (issue_id,))
        conn.commit()
        flash("Issue deleted successfully!", "success")
    except mysql.connector.Error as err:
        flash(f"Error: {err}", "error")
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('staff_issue_portal'))


@app.route('/cancel_delete')
def cancel_delete():
    # Cancel deletion and return to the staff portal
    return redirect(url_for('staff_issue_portal'))





@app.route("/report-cleaning", methods=["GET", "POST"])
@login_required
def report_cleaning():
    # If it's a GET request, retrieve the parameters from the URL query string
    building_name = request.args.get('building_name')
    floor_number = request.args.get('floor_number')
    room_number = request.args.get('room_number')
    timestamp = request.args.get('timestamp')

    # If it's a POST request, handle the form submission
    if request.method == "POST":
        # Get data from form submission
        building_id = request.form["building_id"]
        floor_number = request.form["floor"]
        room_number = request.form["room"]
        timestamp = request.form["timestamp"]

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            # Query to get RestroomID for the selected BuildingID, FloorNumber, and RoomNumber
            cursor.execute("""
                SELECT RestroomID 
                FROM Clean_Squat.RESTROOM 
                WHERE BuildingID = %s AND FloorNumber = %s AND RoomNumber = %s
            """, (building_id, floor_number, room_number))
            restroom_id = cursor.fetchone()

            if restroom_id:
                cursor.execute("""
                    UPDATE Clean_Squat.RESTROOM
                    SET CleaningTimeStamp = %s
                    WHERE RestroomID = %s
                """, (timestamp, restroom_id[0]))
                conn.commit()

                flash("Successfully submitted cleaning report!", "success")
            else:
                flash("No matching restroom found for the selected building, floor, and room.", "error")

        except mysql.connector.Error as err:
            flash(f"MySQL Error: {err}", "error")
        except Exception as e:
            flash(f"Error: {str(e)}", "error")
        finally:
            cursor.close()
            conn.close()

        # Redirect to the cleaning reports list page after successful submission
        return redirect(url_for("report_cleaning"))

    # If it's a GET request, render the form with pre-filled values
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT BuildingID, BuildingName FROM Clean_Squat.BUILDING")
    buildings = cursor.fetchall()
    cursor.close()
    conn.close()

    # Return the template with pre-filled values
    return render_template("report_cleaning.html", 
                           buildings=buildings, 
                           building_name=building_name, 
                           floor_number=floor_number, 
                           room_number=room_number, 
                           timestamp=timestamp)


@app.route("/cleaning-reports-list", methods=["GET"])
@login_required
def cleaning_reports_list():
    # Connect to the database to fetch all restrooms with updated cleaning timestamps
    conn = get_db_connection()
    cursor = conn.cursor()

    # Query to fetch all restrooms, ordered by the most recent cleaning timestamp
    cursor.execute("""
    SELECT BuildingID, FloorNumber, RoomNumber, 
        DATE_FORMAT(CleaningTimeStamp, '%b %d, %Y at %h:%i %p') AS CleaningTimeStamp
    FROM Clean_Squat.RESTROOM
    ORDER BY CleaningTimeStamp DESC
    """)
    cleaning_reports = cursor.fetchall()

    cursor.close()
    conn.close()


    if not cleaning_reports:
        flash("No cleaning reports found.", "warning")

    return render_template("cleaning_reports_list.html", cleaning_reports=cleaning_reports)





#This route renders the page users are taken to if no bathrooms match their preferences.
@app.route("/sorry", methods=["GET"])
@login_required
def sorry():
    #items = get_all_items() # Call defined function to get all items
    return render_template("sorry.html")






# EXAMPLE OF POST REQUEST
@app.route("/new-item", methods=["POST"])
def add_item():
    try:
        # Get items from the form
        data = request.form
        item_name = data["name"] # This is defined in the input element of the HTML form on index.html
        item_quantity = data["quantity"] # This is defined in the input element of the HTML form on index.html

        # TODO: Insert this data into the database
        
        # Send message to page. There is code in index.html that checks for these messages
        flash("Item added successfully", "success")
        # Redirect to home. This works because the home route is named home in this file
        return redirect(url_for("home"))

    # If an error occurs, this code block will be called
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "error") # Send the error message to the web page
        return redirect(url_for("home")) # Redirect to home
# ------------------------ END ROUTES ------------------------ #


# listen on port 8080
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True) # TODO: Students PLEASE remove debug=True when you deploy this for production!!!!!
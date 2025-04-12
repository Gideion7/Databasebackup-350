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
app.secret_key = os.getenv("SECRET")  # Used to securely sign the session cookie


# ------------------------ BEGIN FUNCTIONS ------------------------ #

# Establishes and returns a new database connection using credentials from environment variables
def get_db_connection():
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_DATABASE"),
    )
    return conn


# Decorator to ensure a user is logged in before accessing a protected route
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash("You must be logged in to view this page.", "error")
            return redirect(url_for("login"))  # Redirect to login page if not logged in
        return f(*args, **kwargs)
    return wrapper


# Validates password strength: requires at least 8 characters, one uppercase, one lowercase, and one digit
def validate_password(password):
    import re
    pattern = re.compile("^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).{8,}$")
    return bool(pattern.match(password))


# Validates that the username contains only letters, digits, and underscores, and is 1–30 characters long
def validate_username(username):
    import re
    pattern = re.compile(r"^[A-Za-z0-9_]{1,30}$")
    return bool(pattern.fullmatch(username))


# Validates first name: allows only letters, up to 30 characters
def validate_first_name(first_name):
    pattern = re.compile(r"^[A-Za-z]{1,30}$")
    return bool(pattern.fullmatch(first_name))


# Validates last name: allows only letters, up to 30 characters
def validate_last_name(last_name):
    pattern = re.compile(r"^[A-Za-z]{1,30}$")
    return bool(pattern.fullmatch(last_name))


# Retrieves all building names and their IDs from the database
def get_all_building_names_and_ids():
    conn = get_db_connection()  # Create a new database connection
    cursor = conn.cursor()  # Create a cursor to perform queries
    query = "SELECT BuildingID, BuildingName FROM BUILDING"
    cursor.execute(query)
    result = cursor.fetchall()  # Fetch the results of the query
    conn.close()  # Always close the DB connection to avoid locks
    print('look go')
    print(result)
    return result


# Retrieves the most recent restroom rating based on session filters, and its average rating
def get_results():    
    selected_building_id = session['selected_building_id']
    selected_type = session['selected_type']
    selected_gender = session['selected_gender']

    conn = get_db_connection()
    cursor = conn.cursor()

    # Construct query based on whether gender is specified
    # dot notion was used in thses queries to simplify 
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

    # Save restroom ID to session for future use
    if result:
        session["selected_restroom_id"] = result[0][4]
        selected_restroom_id = result[0][4]  # RestroomID to get average rating

        # Query to calculate average rating for the selected restroom
        query_avg = """
        SELECT AVG(p.Rating)
        FROM Clean_Squat.PreferencesView p
        WHERE p.RestroomID = %s
        """
        cursor.execute(query_avg, (selected_restroom_id,))
        avg_rating = cursor.fetchone()[0]

        avg_rating = round(avg_rating, 1)  # Round average rating to 1 decimal place
        print("DEBUG: Average Rating Retrieved =", avg_rating)

        conn.close()
        return result, avg_rating
    else:
        conn.close()
        return None, None  # Return None if no restroom found
# ------------------------ END FUNCTIONS ------------------------ #


# ------------------------ BEGIN ROUTES ------------------------ #

# This route handles user registration logic and form rendering.
# It supports both GET (display form) and POST (process form) methods.
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Collect form data submitted by the user
        username = request.form["username"]
        password = request.form["password"]
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        role = "USER"  # Default role for all new registrants

        # Validation logic for form fields
        if not validate_password(password):
            flash("Password must be at least 8 characters long, contain at least one uppercase letter, one lowercase letter, and one number.", "error")
            return redirect(url_for("register"))
        
        if not validate_username(username):
            flash("Username must be 1–30 characters and contain only letters, numbers, or underscores.", "error")
            return redirect(url_for("register"))
        
        if not validate_first_name(first_name):
            flash("First Name must be 1-30 characters and contain only letters.")
            return redirect(url_for("register"))
        
        if not validate_last_name(last_name):
            flash("Last Name must be 1-30 characters and contain only letters.")
            return redirect(url_for("register"))

        # Check if the username already exists in the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Clean_Squat.USER WHERE Username = %s", (username,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            flash("Username already taken. Please choose another username.", "error")
            cursor.close()
            conn.close()
            return redirect(url_for("register"))

        try:
            # Insert the new user into the USER table
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Clean_Squat.USER (Username, Password, FirstName, LastName, Role)
                VALUES (%s, %s, %s, %s, %s)
            """, (username, password, first_name, last_name, role))  # NOTE: Storing password in plain text is insecure
            conn.commit()
            cursor.close()
            conn.close()

            flash("User registered successfully!", "success")

            # Automatically log in the user after successful registration
            session['username'] = username
            return redirect(url_for("index"))  # Redirect to login page

        except mysql.connector.Error as err:
            flash(f"MySQL Error: {err}", "error")
            return redirect(url_for("register"))
        except Exception as e:
            flash(f"Error: {str(e)}", "error")
            return redirect(url_for("register"))

    # If GET request, show the registration form
    return render_template("register.html")


# This route handles both displaying the login page and processing login form submissions.
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Get form data
        username = request.form["username"]
        password = request.form["password"]

        # Validate credentials against the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Clean_Squat.USER WHERE Username = %s AND Password = %s", (username, password))
        user = cursor.fetchone()
        cursor.close()

        if user:
            # Set user session variables after successful login
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['role'] = user[5]  # Make sure user[5] is the role column

            # Log session to database
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Clean_Squat.SESSION (UserID, Timestamp)
                VALUES (%s, NOW())
            """, (user[0],))
            conn.commit()
            cursor.close()

            # Role-based redirection
            if session['role'] == 'SUPERVISOR':
                return redirect(url_for("staff_dashboard"))
            elif session['role'] == 'STAFF':
                return redirect(url_for("staff_dashboard"))
            else:
                return redirect(url_for("main"))  # Normal user dashboard
        else:
            flash("Invalid username or password", "error")
            return redirect(url_for("login"))

    # If GET request or failed login, show login page again
    return render_template("index.html")


# This route renders the admin dashboard page, but only for users with the 'STAFF' or 'SUPERVISOR' roles.
@app.route("/admin_dashboard", methods=["GET"])
def admin_dashboard():
    # Restrict access to admin roles only
    if session.get('role') not in ['STAFF', 'SUPERVISOR']:
        return redirect(url_for('unauthorized'))  # Send unauthorized users away
    return render_template("admin_dashboard.html")  # Show dashboard


# This route logs out the user by clearing all session data.
@app.route("/logout")
def logout():
    # Remove session variables and clear entire session
    session.pop('user_id', None)
    session.pop('username', None)
    session.clear()
    return redirect(url_for("index"))  # Redirect to login page after logout

# This route renders the main dashboard after login.
# It serves as the homepage where users can search for restrooms or report issues.
@app.route("/main", methods=["GET"])
@login_required
def main():
    # Placeholder for future logic, e.g., fetching items or status
    return render_template("clean_squat_main.html")


# This route lets users select a building from a list.
# It stores the selected building's ID into the session for later filtering.
@app.route("/select_building", methods=["GET", "POST"])
@login_required
def select_building():
    if request.method == "POST":
        selected_building_id = request.form.get("building")  # Retrieve selected building ID from form
        if selected_building_id:
            session["selected_building_id"] = selected_building_id  # Store in session for use in future queries
        flash("Building Selected!", "success")
    
    # Fetch all building names and IDs from the database to populate the dropdown
    list_of_buildings = get_all_building_names_and_ids()
    return render_template("clean_squat_bldg_select.html", buildings=list_of_buildings)


# This route allows users to choose restroom preferences such as type and gender.
# Preferences are stored in the session for later filtering in the results page.
@app.route("/select_preferences", methods=["GET", "POST"])
@login_required
def select_preferences():
    if request.method == "POST":
        selected_type = request.form.get("type")  # Accepts "public" or "private"
        selected_gender = request.form.get("gender")  # Accepts "male" or "female"

        # Normalize preference data
        if selected_type == "private":
            selected_type = True  # Store as boolean
            selected_gender = None  # Gender doesn't apply to private restrooms
        elif selected_type == "public":
            selected_type = False  # Boolean False means public

        # Save preferences into the session
        session["selected_type"] = selected_type
        session["selected_gender"] = selected_gender

        print("Type:", selected_type)
        print("Gender:", selected_gender)
        flash("Preferences Selected!", "success")

    # Debug: Print all current session data for verification
    all_sessions = dict(session)
    print("This is your session dictionary:")
    print(all_sessions)

    return render_template("clean_squat_preferences.html")


# This route displays the restroom options based on the user's selected building and preferences.
@app.route("/results", methods=["GET"])
@login_required
def results():
    # Validate that necessary selections are in session
    if "selected_building_id" not in session:
        flash("Please select a building before proceeding.")
        return redirect(url_for("main"))

    if "selected_type" not in session or "selected_gender" not in session:
        flash("Please select your preferences before proceeding.")
        return redirect(url_for("main"))
    
    # Query the database for matching restrooms and their average ratings
    results, avg_ratings = get_results()
    
    if results is None:
        flash("The selected building or preferences do not exist.", "error")
        return redirect(url_for("sorry_page"))

    return render_template("clean_squat_results.html", result=results, avg_rating=avg_ratings)


# This route shows a simple error page if no suitable restrooms were found.
@app.route("/sorry")
def sorry_page():
    return render_template("sorry.html")


# This route is shown if a user attempts to access a page they are not authorized for.
@app.route("/unauthorized")
def unauthorized():
    return render_template("unauthorized.html")


# This route handles restroom rating submissions.
# It allows logged-in users to rate restrooms from 1 to 5 and updates the database.
@app.route("/rating", methods=["GET", "POST"])
@login_required
def rating():
    if request.method == "POST":
        rating_value = request.form.get('rating')
        restroom_id = session.get("selected_restroom_id")  # Pulled from session, set on selection
        user_id = session.get("user_id")

        print(f"POST request received: rating_value={rating_value}, restroom_id={restroom_id}, user_id={user_id}")

        # Validate input
        if not rating_value:
            flash("Please select a rating before submitting.")
            return redirect(url_for("rating"))

        try:
            rating_value = int(rating_value)
            restroom_id = int(restroom_id)
            if rating_value < 1 or rating_value > 5:
                flash("Rating must be between 1 and 5.")
                return redirect(url_for("results"))
        except ValueError:
            flash("Invalid rating value.")
            return redirect(url_for("results"))

        # Insert or update the rating in the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Clean_Squat.RATING (Rating, UserID, RestroomID) 
            VALUES (%s, %s, %s) 
            ON DUPLICATE KEY UPDATE Rating = VALUES(Rating)
        """, (rating_value, user_id, restroom_id))

        conn.commit()
        conn.close()

        flash("Thanks for rating!")
        return redirect(url_for("results"))
    # Render rating page on GET request
    return render_template("rating.html")

# This route renders the dashboard page for staff and supervisors.
# It provides navigation to other functionalities like cleaning reports and viewing reported issues.
@app.route("/staff_dashboard", methods=["GET"])
@login_required
def staff_dashboard():
    # Only allow users with STAFF or SUPERVISOR role to access this page
    if session.get('role') not in ['STAFF', 'SUPERVISOR']:
        return redirect(url_for('unauthorized'))
    
    return render_template("staff_dash.html")


# This route allows staff/supervisors to view all reported restroom issues.
# It pulls issue descriptions and their completion statuses from the database and displays them.
@app.route("/staff_issue_portal", methods=["GET"])
@login_required
def staff_issue_portal():
    if session.get('role') not in ['STAFF', 'SUPERVISOR']:
        return redirect(url_for('unauthorized'))
    
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch all reported issues with their current completion status
    cursor.execute("""
        SELECT IssueID, Description, CompletionStatus
        FROM Clean_Squat.ISSUEREPORT
    """)
    issues = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("staff_issue_portal.html", issues=issues)


# This route displays a detailed view of a selected issue.
# It includes building name, room, floor, and timestamp details.
@app.route('/selected_issue/<int:issue_id>', methods=['GET'])
def selected_issue(issue_id):
    if session.get('role') not in ['STAFF', 'SUPERVISOR']:
        return redirect(url_for('unauthorized'))

    conn = get_db_connection()
    cursor = conn.cursor()

    # Join issue, restroom, and building data for more contextual detail
    cursor.execute("""
        SELECT i.IssueID, i.Description, i.CompletionStatus, b.BuildingName, p.FloorNumber, p.RoomNumber, i.ReportTimeStamp
        FROM Clean_Squat.ISSUEREPORT i
        JOIN Clean_Squat.RESTROOM p ON i.RestroomID = p.RestroomID
        JOIN Clean_Squat.BUILDING b ON p.BuildingID = b.BuildingID
        WHERE i.IssueID = %s
    """, (issue_id,))
    issue = cursor.fetchone()

    # Format timestamp for a cleaner UI
    if issue:
        timestamp = issue[6]
        formatted_timestamp = timestamp.strftime('%B %d, %Y at %I:%M %p')
        issue = list(issue)
        issue[6] = formatted_timestamp

    cursor.close()
    conn.close()

    return render_template('selected_issue.html', issue=issue)


# This route allows users to report an issue in a specific restroom.
# It handles both GET (show form) and POST (submit issue) requests.
@app.route("/report_an_issue", methods=["GET", "POST"])
@login_required
def report_an_issue():
    # For GET requests, capture any location pre-filled from a previous page
    building_name = request.args.get("building")
    floor_number = request.args.get("floor")
    room_number = request.args.get("room")

    if request.method == "POST":
        description = request.form["description"]
        timestamp = request.form["timestamp"]
        building_id = request.form["building_id"]
        floor = request.form["floor"]
        room = request.form["room"]

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            # Find the restroom matching the building, floor, and room number
            cursor.execute("""
                SELECT RestroomID 
                FROM Clean_Squat.RESTROOM 
                WHERE BuildingID = %s AND FloorNumber = %s AND RoomNumber = %s
            """, (building_id, floor, room))
            restroom_id = cursor.fetchone()

            if not restroom_id:
                flash("No matching restroom found for the selected building, floor, and room.", "error")
                return redirect(url_for("report_an_issue"))

            # Insert issue report linked to the found restroom
            cursor.execute("""
                INSERT INTO Clean_Squat.ISSUEREPORT (Description, CompletionStatus, ReportTimeStamp, RestroomID)
                VALUES (%s, %s, %s, %s)
            """, (description, False, timestamp, restroom_id[0]))

            conn.commit()
            flash("Successfully submitted issue report!", "success")
            return redirect(url_for("report_an_issue"))

        except mysql.connector.Error as err:
            flash(f"MySQL Error: {err}", "error")
            return redirect(url_for("report_an_issue"))

        except Exception as e:
            flash(f"Unexpected error: {str(e)}", "error")
            return redirect(url_for("report_an_issue"))

        finally:
            cursor.close()
            conn.close()

    # GET request: fetch building list for dropdown selection
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT BuildingID, BuildingName FROM Clean_Squat.BUILDING")
    buildings = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template(
        "report_an_issue.html",
        buildings=buildings,
        building_name=building_name,
        floor_number=floor_number,
        room_number=room_number,
    )


# This route is used by staff/supervisors to mark an issue as resolved or unresolved.
# It is triggered by a form POST action from the issue portal.
@app.route("/update_issue_status/<int:issue_id>/<int:status>", methods=["POST"])
def update_issue_status(issue_id, status):
    if session.get('role') not in ['STAFF', 'SUPERVISOR']:
        return redirect(url_for('unauthorized'))

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            UPDATE Clean_Squat.ISSUEREPORT 
            SET CompletionStatus = %s 
            WHERE IssueID = %s
        """, (status, issue_id))

        conn.commit()
        flash("Issue status updated successfully!", "success")
        return redirect(url_for("staff_issue_portal"))

    except mysql.connector.Error as err:
        flash(f"Database Error: {err}", "error")
        return redirect(url_for("staff_issue_portal"))

    finally:
        cursor.close()
        conn.close()


# This route shows a confirmation page before deleting an issue.
# It prevents accidental deletions by requiring an explicit POST confirmation.
@app.route('/confirm_delete/<int:issue_id>', methods=['GET', 'POST'])
def confirm_delete(issue_id):
    if session.get('role') not in ['STAFF', 'SUPERVISOR']:
        return redirect(url_for('unauthorized'))

    if request.method == 'POST':
        # User confirmed deletion – redirect to the actual deletion route
        return redirect(url_for('delete_issue', issue_id=issue_id))
    
    # Render confirmation page with the selected issue_id
    return render_template('confirm_delete.html', issue_id=issue_id)


# This route performs the deletion of the issue from the database.
# It can only be accessed via POST for safety.
@app.route('/delete_issue/<int:issue_id>', methods=['POST'])
def delete_issue(issue_id):
    if session.get('role') not in ['STAFF', 'SUPERVISOR']:
        return redirect(url_for('unauthorized'))

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Delete the issue from the ISSUEREPORT table
        cursor.execute("DELETE FROM Clean_Squat.ISSUEREPORT WHERE IssueID = %s", (issue_id,))
        conn.commit()
        flash("Issue deleted successfully!", "success")
    except mysql.connector.Error as err:
        flash(f"Error: {err}", "error")
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('staff_issue_portal'))


# This route allows the user to cancel deletion and return to the staff portal.
@app.route('/cancel_delete')
def cancel_delete():
    if session.get('role') not in ['STAFF', 'SUPERVISOR']:
        return redirect(url_for('unauthorized'))
    
    return redirect(url_for('staff_issue_portal'))


# This route allows staff/supervisors to submit a cleaning report for a restroom.
# It accepts pre-filled location values via GET and form submission via POST.
@app.route("/report-cleaning", methods=["GET", "POST"])
@login_required
def report_cleaning():
    if session.get('role') not in ['STAFF', 'SUPERVISOR']:
        return redirect(url_for('unauthorized'))

    # Pre-fill values in form via query parameters
    building_name = request.args.get('building_name')
    floor_number = request.args.get('floor_number')
    room_number = request.args.get('room_number')
    timestamp = request.args.get('timestamp')

    if request.method == "POST":
        # Get form data submitted by the user
        building_id = request.form["building_id"]
        floor_number = request.form["floor"]
        room_number = request.form["room"]
        timestamp = request.form["timestamp"]

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            # Retrieve restroom ID using the submitted details
            cursor.execute("""
                SELECT RestroomID 
                FROM Clean_Squat.RESTROOM 
                WHERE BuildingID = %s AND FloorNumber = %s AND RoomNumber = %s
            """, (building_id, floor_number, room_number))
            restroom_id = cursor.fetchone()

            if restroom_id:
                # Update the CleaningTimeStamp for the identified restroom
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

        return redirect(url_for("report_cleaning"))

    # GET request: Fetch buildings for dropdown selection
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT BuildingID, BuildingName FROM Clean_Squat.BUILDING")
    buildings = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template(
        "report_cleaning.html",
        buildings=buildings,
        building_name=building_name,
        floor_number=floor_number,
        room_number=room_number,
        timestamp=timestamp
    )


# This route displays a list of all restrooms with their latest cleaning timestamps.
# Useful for staff/supervisors to track maintenance history.
@app.route("/cleaning-reports-list", methods=["GET"])
@login_required
def cleaning_reports_list():
    if session.get('role') not in ['STAFF', 'SUPERVISOR']:
        return redirect(url_for('unauthorized'))

    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch restroom cleaning records, formatted nicely for display
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

# ------------------------ END ROUTES ------------------------ #

# Application entry point.
# The app listens on all interfaces at port 8080.
# `debug=True` enables automatic reload on code changes and better error messages.
# IMPORTANT: debug=True SHOULD BE REMOVED IN PRODUCTION
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)  # TODO: REMOVE debug=True IN PRODUCTION!

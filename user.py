import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify

from auth import data
from db import DatabaseManager
from user_data import User_data  # Import user database to fetch email
dbm = DatabaseManager()
rec=dbm.rec_get_conn()
rec_cursor=rec.cursor()
user_bp = Blueprint('user', __name__)

@user_bp.route('/dashboard')
def dashboard():
    if 'user' not in session or session['user'] == 'admin':
        flash("Unauthorized Access!")
        return redirect(url_for('auth.index'))
    return render_template('user_dashboard.html')


@user_bp.route('/book_movie', methods=['GET', 'POST'])
def book_movie():
    if 'user' not in session:
        return redirect(url_for('auth.index'))

    conn = dbm.get_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        movie_name = request.form.get("movie_name")
        show_time = request.form.get("show_time")

        cursor.execute("INSERT INTO booked_tickets (movie_name, show_time, username) VALUES (?, ?, ?)",
                       (movie_name, show_time, session['user']))
        conn.commit()
        conn.close()

        flash("Movie booked successfully!")
        return redirect(url_for('user.dashboard'))

    # Fetch available movies from the database
    cursor.execute("SELECT name FROM movies")
    movies = cursor.fetchall()
    conn.close()

    return render_template('book_movie.html', movies=movies)

@user_bp.route('/select_show', methods=['POST'])
def select_show():
    if 'user' not in session:
        return redirect(url_for('auth.index'))

    movie_name = request.form.get("movie_name")

    if not movie_name:
        flash("Please select a movie!")
        return redirect(url_for('user.confirm_booking'))

    conn = dbm.get_connection()
    cursor = conn.cursor()

    # Fetch available shows and seats from `shows` table
    cursor.execute("SELECT show_time, tickets_available FROM shows WHERE movie_name = ?", (movie_name,))
    shows = cursor.fetchall()
    conn.close()

    return render_template('select_show.html', movie_name=movie_name, shows=shows)


@user_bp.route('/confirm_booking', methods=['POST'])
def confirm_booking():
    if 'user' not in session:
        return redirect(url_for('auth.index'))

    username = session['user']
    movie_name = request.form.get("movie_name")
    show_time = request.form.get("show_time")
    num_tickets = int(request.form.get("num_tickets"))

    conn = dbm.get_connection()
    cursor = conn.cursor()

    try:
        # Check available seats
        cursor.execute("SELECT tickets_available FROM shows WHERE movie_name = ? AND show_time = ?",
                       (movie_name, show_time))
        available_seats = cursor.fetchone()

        if not available_seats:
            flash("Show not found!")
            return redirect(url_for('user.dashboard'))
        available_seats = available_seats[0]  # Extract integer value

        if available_seats >= num_tickets:
            # Book the tickets
            cursor.execute("INSERT INTO bookings (movie_name, show_time, username, seat_number) VALUES (?, ?, ?, ?)",
                           (movie_name, show_time, username, num_tickets))

            # Reduce available seats
            cursor.execute("UPDATE shows SET tickets_available = tickets_available - ? WHERE movie_name = ? AND show_time = ?",
                           (num_tickets, movie_name, show_time))

            # Fetch user email from user_data table
            rec_cursor.execute("SELECT EmailID FROM user_data WHERE Username = ?", (username,))
            user_email = rec_cursor.fetchone()
            conn.commit()  # ✅ Commit changes only if everything succeeds

            if user_email:
                send_booking_email(user_email[0], movie_name, show_time, num_tickets)  # Send confirmation email
            flash(f"Booking confirmed for {num_tickets} ticket(s)! Confirmation email sent.")
        else:
            flash("Not enough tickets available!")

    except Exception as e:
        conn.rollback()  # ❌ Rollback in case of error
        flash(f"Error: {str(e)}")

    finally:
        conn.close()

    return redirect(url_for('user.dashboard'))



def send_booking_email(to_email, movie_name, show_time, num_tickets):
    sender_email = "Labheshk356@gmail.com"  # Your email
    sender_password = "tmov lzka fttp hsnu"  # Use App Password if using Gmail

    subject = "Movie Booking Confirmation"
    body = f"""
    Dear User,

    Your booking has been confirmed!

    Movie: {movie_name}
    Show Time: {show_time}
    Number of Tickets: {num_tickets}

    Thank you for choosing our service!

    Regards,
    Movie Booking Team
    """

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        # Connect to Gmail SMTP Server
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()  # Secure connection
        server.login(sender_email, sender_password)  # Login
        server.sendmail(sender_email, to_email, msg.as_string())  # Send email
        server.quit()
        print("Email sent successfully!")

    except Exception as e:
        print("Error sending email:", str(e))


# Cancel a Booking
@user_bp.route('/cancel_movie', methods=['GET', 'POST'])
def cancel_movie():
    if 'user' not in session:
        flash("Please log in to cancel a booking.")
        return redirect(url_for('auth.index'))

    conn = dbm.get_connection()
    cursor = conn.cursor()

    if request.method == 'GET':
        # Get user's booked movies
        cursor.execute("SELECT DISTINCT movie_name FROM bookings WHERE username = ?", (session['user'],))
        movies = [row[0] for row in cursor.fetchall()]

        # Get user's booked showtimes
        cursor.execute("SELECT DISTINCT show_time FROM bookings WHERE username = ?", (session['user'],))
        showtimes = [row[0] for row in cursor.fetchall()]

        conn.close()
        return render_template("cancel_movie.html", movies=movies, showtimes=showtimes)

    if request.method == 'POST':
        movie_name = request.form.get("movie_name")
        show_time = request.form.get("show_time")

        if not movie_name or not show_time:
            flash("Please select a valid movie and showtime.")
            return redirect(url_for('user.cancel_movie'))

        # Fetch ticket ID
        cursor.execute("SELECT id, seat_number FROM bookings WHERE movie_name = ? AND show_time = ? AND username = ?",
                       (movie_name, show_time, session['user']))
        booking = cursor.fetchone()

        if not booking:
            flash("No booking found for this movie and showtime!")
            conn.close()
            return redirect(url_for('user.cancel_movie'))

        ticket_id, num_tickets = booking

        # Now, cancel the booking
        cursor.execute("DELETE FROM bookings WHERE id = ? AND username = ?", (ticket_id, session['user']))
        cursor.execute("UPDATE shows SET tickets_available = tickets_available + ? WHERE movie_name = ? AND show_time = ?",
                       (num_tickets, movie_name, show_time))

        # Get user email for cancellation confirmation
        rec_cursor.execute("SELECT EmailID FROM user_data WHERE Username = ?", (session['user'],))
        user_email = rec_cursor.fetchone()

        conn.commit()
        conn.close()

        if user_email:
            send_cancel_email(user_email[0], movie_name, show_time, num_tickets)

        flash("Booking cancelled successfully! A confirmation email has been sent.")
        return redirect(url_for('user.dashboard'))


@user_bp.route('/get_show_times')
def get_show_times():
    if 'user' not in session:
        return redirect(url_for('auth.index'))

    movie_name = request.args.get("movie_name")

    conn = dbm.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT show_time FROM bookings WHERE movie_name = ? AND username = ?",
                   (movie_name, session['user']))
    show_times = [row[0] for row in cursor.fetchall()]
    conn.close()

    return jsonify({"show_times": show_times})


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_cancel_email(user_email, movie_name, show_time, num_tickets):
    sender_email = "Labheshk356@gmail.com"
    sender_password = "tmov lzka fttp hsnu"  # Use app password if needed
    subject = "Movie Booking Cancellation"

    # Email body with proper UTF-8 encoding
    email_body = f"""
    <html>
    <body>
        <h2>Your Booking Has Been Cancelled </h2>
        <p><strong>Movie:</strong> {movie_name}</p>
        <p><strong>Showtime:</strong> {show_time}</p>
        <p><strong>Tickets Cancelled:</strong> {num_tickets}</p>
        <p>We hope to see you again soon!</p>
    </body>
    </html>
    """

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = user_email
    msg["Subject"] = subject

    # Convert email body to UTF-8
    msg.attach(MIMEText(email_body, "html", "utf-8"))

    try:
        # Connect to SMTP Server (Example: Gmail)
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, user_email, msg.as_string())
        server.quit()
        print("Cancellation email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")


# View Bookings
@user_bp.route('/view_bookings')
def view_bookings():
    if 'user' not in session:
        flash("Please log in to view your bookings.")
        return redirect(url_for('auth.index'))

    conn = dbm.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, movie_name, show_time FROM bookings WHERE username = ?", (session['user'],))
    tickets = cursor.fetchall()
    conn.close()

    return render_template('view_bookings.html', tickets=tickets)

# Logout
@user_bp.route('/logout')
def logout():
    session.pop("user", None)
    flash("Logged out successfully!")
    return redirect(url_for('auth.index'))

            print("Database error:", e)




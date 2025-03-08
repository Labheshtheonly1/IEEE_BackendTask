from flask import Blueprint, render_template, request, redirect, url_for, flash,session
from db import DatabaseManager

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
db_manager = DatabaseManager()
db_manager.create_tables()  # Ensure tables exist

@admin_bp.route('/home')
def home():
    return render_template('admin_home.html')

# -----------------------
# ADD MOVIE
# -----------------------
@admin_bp.route('/add_movie_page')
def add_movie_page():
    return render_template('add_movie.html')


@admin_bp.route('/bookings')
def view_bookings():
    conn = db_manager.get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM bookings")
    bookings = cursor.fetchall()

    conn.close()

    return render_template('admin_bookings.html', bookings=bookings)


@admin_bp.route('/add_movie', methods=['POST'])
def add_movie():
    movie_name = request.form.get("movie_name")
    genre = request.form.get("genre")
    if not movie_name or not genre:
        flash("Please provide both movie name and genre.")
        return redirect(url_for('admin.add_movie_page'))

    success, message = db_manager.add_movie(movie_name, genre)
    if not success:
        flash(message)
        return redirect(url_for('admin.add_movie_page'))

    # Process dynamic slot entries
    slot_times = request.form.getlist('slot_time[]')
    slot_tickets = request.form.getlist('slot_tickets[]')
    for st, sticket in zip(slot_times, slot_tickets):
        if st:  # if a slot time is provided
            try:
                tickets = int(sticket)
            except ValueError:
                tickets = 0
            db_manager.add_show(movie_name, st, tickets)

    flash("Movie and slots added successfully!")
    return redirect(url_for('admin.home'))

# -----------------------
# REMOVE MOVIE (SLOTS)
# -----------------------
# Step 1: Select a movie
@admin_bp.route('/remove_movie_page', methods=['GET', 'POST'])
def remove_movie_page():
    if request.method == 'POST':
        movie_name = request.form.get("movie_id")
        if not movie_name:
            flash("Please select a movie.")
            return redirect(url_for('admin.remove_movie_page'))

        # Fetch slots for the selected movie
        slots = db_manager.get_shows_by_movie(movie_name)
        print(movie_name)
        print(slots)
        if not slots:
            flash("No slots found for that movie!")
            return redirect(url_for('admin.home'))

        return render_template('remove_movie.html', movie_name=movie_name, slots=slots)
    else:
        # Show a dropdown of all movies
        movies = db_manager.get_movies()
        return render_template('remove_movie_input.html', movies=movies)

# Step 2: Remove the chosen slot
@admin_bp.route('/delete_slot', methods=['GET', 'POST'])
def delete_slot():
    if request.method == 'POST':
        slot_id = request.form.get("slot_id")

        if not slot_id:
            flash("Please select a slot to remove!")
            return redirect(url_for('admin.home'))

        conn = db_manager.get_connection()
        cursor = conn.cursor()

        # Get the movie name of the show being deleted
        cursor.execute("SELECT movie_name FROM shows WHERE id = ?", (slot_id,))
        movie_name = cursor.fetchone()

        if movie_name:
            movie_name = movie_name[0]

            # Remove the show
            cursor.execute("DELETE FROM shows WHERE id = ?", (slot_id,))
            conn.commit()

            # Check if any shows remain for this movie
            cursor.execute("SELECT COUNT(*) FROM shows WHERE movie_name = ?", (movie_name,))
            remaining_shows = cursor.fetchone()[0]

            if remaining_shows == 0:
                # If no shows remain, delete the movie
                cursor.execute("DELETE FROM movies WHERE name = ?", (movie_name,))
                conn.commit()
                flash(f"Show removed. Since there are no more shows, the movie '{movie_name}' has also been deleted.")

            else:
                flash("Show removed successfully!")

        else:
            flash("Invalid show selected!")

        conn.close()
    else:
        return render_template('remove_movie.html')

    return redirect(url_for('admin.home'))




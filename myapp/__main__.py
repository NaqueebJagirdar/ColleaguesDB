import os
from datetime import date, timedelta, datetime

from flask import Flask, render_template, request, redirect, url_for
from myapp.models import db, Colleague, CalendarEntry

app = Flask(__name__)

# Use an absolute path to the database
BASEDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(BASEDIR, "database.db")

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_PATH}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize db with this app
db.init_app(app)

@app.route('/')
def home():
    """Landing page (index.html)."""
    return render_template('index.html')

from datetime import date, timedelta
from flask import Flask, render_template, request, redirect, url_for
from myapp.models import db, Colleague, CalendarEntry

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    # 1. Parse the "start" query param
    start_str = request.args.get('start', None)
    if start_str:
        try:
            start_date = datetime.strptime(start_str, "%Y-%m-%d").date()
        except ValueError:
            # If the user typed an invalid date, fallback to current Monday
            start_date = get_current_monday()
    else:
        # Default to the current week's Monday
        start_date = get_current_monday()

    # 2. Build the date range for 7 days
    num_days = 7
    date_columns = [start_date + timedelta(days=i) for i in range(num_days)]

    # 3. Fetch colleagues and handle POST to save changes
    colleagues = Colleague.query.all()
    if request.method == 'POST':
        for colleague in colleagues:
            for day_date in date_columns:
                field_name = f"colleague_{colleague.id}_day_{day_date}"
                selected_value = request.form.get(field_name)

                entry = CalendarEntry.query.filter_by(
                    colleague_id=colleague.id,
                    date=day_date
                ).first()

                if selected_value and selected_value != "":
                    if not entry:
                        entry = CalendarEntry(colleague_id=colleague.id, date=day_date)
                        db.session.add(entry)
                    entry.entry_type = selected_value
                else:
                    if entry:
                        db.session.delete(entry)

        db.session.commit()
        return redirect(url_for('dashboard', start=start_date.strftime("%Y-%m-%d")))

    # 4. Build calendar_dict for the selected week
    entries = CalendarEntry.query.filter(
        CalendarEntry.date >= start_date,
        CalendarEntry.date < start_date + timedelta(days=num_days)
    ).all()

    calendar_dict = {}
    for e in entries:
        if e.colleague_id not in calendar_dict:
            calendar_dict[e.colleague_id] = {}
        calendar_dict[e.colleague_id][e.date] = e.entry_type

    # 5. Create "Previous" and "Next" links
    prev_monday = (start_date - timedelta(days=7)).strftime("%Y-%m-%d")
    next_monday = (start_date + timedelta(days=7)).strftime("%Y-%m-%d")

    current_monday = get_current_monday().strftime("%Y-%m-%d")
    current_link = url_for('dashboard', start=current_monday)

    return render_template(
        'edit_calendar.html',
        colleagues=colleagues,
        date_columns=date_columns,
        calendar_dict=calendar_dict,
        start_date=start_date,
        prev_link=url_for('dashboard', start=prev_monday),
        next_link=url_for('dashboard', start=next_monday),
        current_link=current_link
    )


@app.route('/calendar/<int:colleague_id>')
def calendar_view(colleague_id):
    """
    Shows a single colleague's calendar entries (all dates in DB).
    For a more detailed monthly or weekly view, you'd filter by date range.
    """
    colleague = Colleague.query.get_or_404(colleague_id)
    entries = CalendarEntry.query.filter_by(colleague_id=colleague_id).all()

    return render_template('calendar.html', colleague=colleague, entries=entries)

def get_current_monday():
    print("DEBUG: datetime.now() =", datetime.now())
    print("DEBUG: System weekday() is:", datetime.now().weekday())
    override = os.environ.get('FAKE_CURRENT_DATE')

    if override:
        # parse e.g. "2025-03-10"
        forced_date = datetime.strptime(override, "%Y-%m-%d").date()
        return forced_date - timedelta(days=forced_date.weekday())
    else:
        today = datetime.now().date()
        return today - timedelta(days=today.weekday())


@app.route('/edit_calendar', methods=['GET', 'POST'])
def edit_calendar():
    """
    Displays a weekly table with a dynamic start date.
    Allows POST submissions to save changes.
    """

    # 1. Determine the start date from query param (?start=YYYY-MM-DD)
    start_str = request.args.get('start', None)
    if start_str:
        try:
            start_date = datetime.strptime(start_str, "%Y-%m-%d").date()
        except ValueError:
            start_date = get_current_monday()  # fallback if invalid
    else:
        start_date = get_current_monday()      # default to current Monday

    # 2. Build a 7-day range from start_date
    num_days = 7
    date_columns = [start_date + timedelta(days=i) for i in range(num_days)]

    # 3. Fetch all colleagues
    colleagues = Colleague.query.all()

    # 4. If POST, process the form data
    if request.method == 'POST':
        for colleague in colleagues:
            for day_date in date_columns:
                field_name = f"colleague_{colleague.id}_day_{day_date}"
                selected_value = request.form.get(field_name)

                entry = CalendarEntry.query.filter_by(
                    colleague_id=colleague.id,
                    date=day_date
                ).first()

                if selected_value and selected_value != "":
                    # Create or update
                    if not entry:
                        entry = CalendarEntry(colleague_id=colleague.id, date=day_date)
                        db.session.add(entry)
                    entry.entry_type = selected_value
                else:
                    # Remove if blank or "-"
                    if entry:
                        db.session.delete(entry)

        db.session.commit()
        # Redirect to the same week so user sees updated data
        return redirect(url_for('edit_calendar', start=start_date.strftime("%Y-%m-%d")))

    # 5. Build a dictionary for the current week’s data
    entries = CalendarEntry.query.filter(
        CalendarEntry.date >= start_date,
        CalendarEntry.date < start_date + timedelta(days=num_days)
    ).all()

    calendar_dict = {}
    for e in entries:
        if e.colleague_id not in calendar_dict:
            calendar_dict[e.colleague_id] = {}
        calendar_dict[e.colleague_id][e.date] = e.entry_type

    # 6. Create links for previous and next weeks
    prev_monday = (start_date - timedelta(days=7)).strftime("%Y-%m-%d")
    next_monday = (start_date + timedelta(days=7)).strftime("%Y-%m-%d")

    current_monday = get_current_monday().strftime("%Y-%m-%d")

    return render_template(
        'edit_calendar.html',  # The template file
        colleagues=colleagues,
        date_columns=date_columns,
        calendar_dict=calendar_dict,
        start_date=start_date,
        prev_link=url_for('edit_calendar', start=prev_monday),
        next_link=url_for('edit_calendar', start=next_monday),
        current_link=url_for('edit_calendar', start=current_monday)
    )

@app.route('/stats')
def stats():
    """
    Shows how many days each colleague is 'Working' (available)
    from Mon-Fri for a given week.
    """
    # 1. Parse ?start=YYYY-MM-DD, default to current Monday
    start_str = request.args.get('start', None)
    if start_str:
        try:
            start_date = datetime.strptime(start_str, "%Y-%m-%d").date()
        except ValueError:
            start_date = get_current_monday()
    else:
        start_date = get_current_monday()

    # 2. Build a list of Monday->Friday dates
    #    If start_date is Monday, these are Mon-Fri.
    #    If you want to force the code to re-align to Monday, do so as well.
    #    For simplicity, we assume start_date is already Monday from get_current_monday.
    num_days = 5  # only Mon-Fri
    date_columns = [start_date + timedelta(days=i) for i in range(num_days)]

    # 3. Fetch all colleagues
    colleagues = Colleague.query.all()

    # 4. Query relevant CalendarEntry rows for these 5 days
    entries = CalendarEntry.query.filter(
        CalendarEntry.date >= start_date,
        CalendarEntry.date < start_date + timedelta(days=num_days)
    ).all()

    # 5. Build a structure to count how many "Working" days per colleague
    #    { colleague_id: count_of_working_days }
    working_counts = {}
    for colleague in colleagues:
        working_counts[colleague.id] = 0

    for e in entries:
        if e.entry_type == "Working":
            # increment if it's "Working"
            working_counts[e.colleague_id] += 1

    # 6. We'll pass a list of "stats" for the template:
    #    each item = (colleague, working_days, total_days=5)
    stats_data = []
    for colleague in colleagues:
        stats_data.append({
            "colleague": colleague,
            "working_days": working_counts[colleague.id],
            "total_days": 5
        })

    # 7. Create prev/next links (optional, if you want weekly navigation)
    prev_monday = (start_date - timedelta(days=7)).strftime("%Y-%m-%d")
    next_monday = (start_date + timedelta(days=7)).strftime("%Y-%m-%d")
    current_monday = get_current_monday().strftime("%Y-%m-%d")

    return render_template(
        "stats.html",
        start_date=start_date,
        stats_data=stats_data,
        prev_link=url_for('stats', start=prev_monday),
        next_link=url_for('stats', start=next_monday),
        current_link=url_for('stats', start=current_monday),
    )



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

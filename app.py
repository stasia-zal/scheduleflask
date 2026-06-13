import sys
from schedule_uek_web_excel.tracker import save_as_icalendar, scrape_data, save_as_csv
from flask import Flask, request, send_file, render_template
import io
import json
# from your_script import get_student_schedule, get_lecturer_schedule

app = Flask(__name__)


@app.route('/')
def index():
    try:
        with open('dic.json', 'r', encoding='utf-8-sig') as f:
            dictionary_data = json.load(f)
    except FileNotFoundError:
        dictionary_data = []
    return render_template('index.html', dictionary=dictionary_data)

@app.route('/api/get-schedule', methods=['GET'])
def get_schedule():
    role = request.args.get('role')      # 'student' or 'lecturer'
    code = request.args.get('query')    # The typed string
    file_format = request.args.get('format')  # 'ics' or 'csv'

    try:
        is_lecturer = (role == 'lecturer')
        raw_schedule=scrape_data(code,is_lecturer)
        if not raw_schedule:
            return "Failed to fetch schedule data. Check your ID or credentials.", 400
        if file_format == 'csv':
            ical=save_as_csv(raw_schedule, f'{code}.csv')
            download_name=f'{code}.csv'
            file_stream = io.BytesIO(ical.encode('utf-8-sig'))
            mimetype = 'text/csv'
        else:
            formatted_data = save_as_icalendar(raw_schedule,f'{code}.ics')
            download_name=f'{code}.ics'
            file_stream = io.BytesIO(formatted_data)
            mimetype = 'text/calendar'
        return send_file(
            file_stream,
            mimetype=mimetype,
            as_attachment=True,
            download_name=download_name
        )

    except Exception as e:
        return f"Error creating file: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
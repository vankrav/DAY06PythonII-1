import datetime

from flask import Flask, request, send_file
import pandas as pd
import tempfile
# from database.dbapi import DatabaseConnector

app = Flask(__name__)


@app.route('/download/<int:book_id>')
def download_stats(book_id):
    # Get borrows for given book_id
    # db = DatabaseConnector("localhost", "postgres", "postgres", "postgres")
    # borrows = db.get_book_borrows(book_id)
    # print(borrows)
    borrows = [(1, 1, datetime.datetime(2023, 4, 15, 11, 58, 22, 27270), datetime.datetime(2023, 4, 15, 0, 0)),
     (3, 1, datetime.datetime(2023, 4, 15, 12, 1, 8, 322826), None)]
    # Drop user_id from borrows dataframe
    # borrows = borrows.drop('user_id', axis=1)

    # Create temporary file to save the statistics
    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp_file:
        # Write the statistics to the temporary file using pandas
        borrows.to_excel(tmp_file.name, index=False)

    # Return the temporary file to the user as a downloadable file
    return send_file(tmp_file.name, as_attachment=True, attachment_filename='book_stats.xlsx')


if __name__ == '__main__':
    app.run()
    # db = DatabaseConnector("localhost", "postgres", "postgres", "postgres")
    # borrows = db.get_book_borrows(1)
    # print(borrows)
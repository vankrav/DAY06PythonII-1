import datetime
from os import path
import openpyxl
from flask import Flask, request, send_file, send_from_directory
import pandas as pd
import tempfile
from database.dbapi import DatabaseConnector

app = Flask(__name__)


@app.route('/download/<int:book_id>', methods=['GET', 'POST'])
def download_stats(book_id):
    # Get borrows for given book_id
    db = DatabaseConnector("localhost", "postgres", "postgres", "postgres")
    borrows = db.get_book_borrows(book_id)
    borrows.to_excel(r'book_stats.xlsx')
    # print(borrows)

    # Drop user_id from borrows dataframe
    # borrows = borrows.drop('user_id', axis=1)

    # Create temporary file to save the statistics

    return send_file('book_stats.xlsx')

if __name__ == '__main__':
    app.run()

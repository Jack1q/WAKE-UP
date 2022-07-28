import calendar
from flask import Flask, redirect, url_for, render_template, request, flash
from flask_wtf import FlaskForm
from numpy import save
from wtforms import IntegerField, StringField, SubmitField, BooleanField, SelectMultipleField, FieldList
from wtforms.validators import Length, ValidationError

import config

app = Flask(__name__)
app.config['SECRET_KEY'] = 'temp_key'


class SettingsForm(FlaskForm):
    """ Fields for alarm settings """

    stock_ticker = StringField("Stock Ticker", validators=[Length(max=5)])
    custom_message = StringField("Custom Message", validators=[Length(max=16)])
    alarm_hour = IntegerField("Alarm Hour")
    alarm_minute = IntegerField("Alarm Minute")
    email_address = None
    email_password = None
    instagram_username = StringField("Instagram Username", validators=[Length(max=25)])

    # next step - setup display picker

    # countdown_year = IntegerField('Year')
    # countdown_month = IntegerField('Month')
    # countdown_day = IntegerField('Day')
    # countdown_hour = IntegerField('Hour')
    submit = SubmitField('Save changes')

    def validate_alarm_hour(self, alarm_hour):
        if alarm_hour == None or alarm_hour.data == None or alarm_hour.data < 0 or alarm_hour.data > 23:
            raise ValidationError("Hour must be an integer beteen 0 and 23.")
    def validate_alarm_minute(self, alarm_minute):
        if alarm_minute == None or alarm_minute.data == None or alarm_minute.data < 0 or alarm_minute.data > 59:
            raise ValidationError("Minute must be between 0 and 59.")


def add_sleep_in_attrs():
    for e, day in enumerate(calendar.day_name):
        setattr(SettingsForm, str(e), BooleanField(day[0:3]))

def prettify_num(n):
    if n < 10:
        return '0' + str(n)
    return str(n)


@app.route('/', methods=['GET', 'POST'])
def home():
    """
    This serves the page for the dashboard.
    """
    form = SettingsForm()
    settings = config.get_settings_dictionary()

    if form.validate_on_submit():
        if form.custom_message.data != settings["CUSTOM_MESSAGE"]:
            settings["CUSTOM_MESSAGE"] = form.custom_message.data
        if form.stock_ticker.data != settings["STOCK_TICKER"]:
            settings["STOCK_TICKER"] = form.stock_ticker.data
        if form.instagram_username.data != settings["INSTAGRAM_USERNAME"]:
            settings["INSTAGRAM_USERNAME"] = form.instagram_username.data
        if form.alarm_hour.data != settings["ALARM_HOUR"]:
            settings["ALARM_HOUR"] = form.alarm_hour.data
        if form.alarm_minute.data != settings["ALARM_MINUTES"]:
            settings["ALARM_MINUTES"] = form.alarm_minute.data

        for e in range(len(calendar.day_name)):
            sleep_in = getattr(form, str(e)).data
            if sleep_in and e not in settings["SLEEP_IN_DAYS"]:
                settings["SLEEP_IN_DAYS"].append(e)
            elif not sleep_in and e in settings["SLEEP_IN_DAYS"]:
                settings["SLEEP_IN_DAYS"].remove(e)
        
        flash('settings updated', 'success')
        config.update_settings_file(settings)

        return redirect(url_for('home'))
    elif request.method == 'GET':
        form.custom_message.data = settings["CUSTOM_MESSAGE"]
        form.stock_ticker.data = settings["STOCK_TICKER"]
        form.instagram_username.data = settings["INSTAGRAM_USERNAME"]
        form.alarm_hour.data = prettify_num(settings["ALARM_HOUR"])
        form.alarm_minute.data = prettify_num(settings["ALARM_MINUTES"])
        # form.sleep_in_monday.data = 0 in settings["SLEEP_IN_DAYS"]
        for i in range(len(calendar.day_name)):
            getattr(form, str(i)).data = i in settings["SLEEP_IN_DAYS"]
        getattr(form, str(i)).data = settings["SLEEP_IN_DAYS"]

    return render_template('index.html', form=form, icons=False) # icons can be enabled if you want


@app.route('/about')
def about():
    return "about"

if __name__ == '__main__':
    add_sleep_in_attrs()
    app.run(debug=True)
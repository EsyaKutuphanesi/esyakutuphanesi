# -*- coding: utf-8 -*-
import uuid
import json
import os
from datetime import datetime

from flask import render_template, send_from_directory, flash, url_for, redirect, request, jsonify, g
from flask_login import current_user, login_required, logout_user

from __init__ import app, db
from forms import *
from models import *
from array import *


@app.errorhandler(404)
def page_not_found(error):
    return render_template('/404.html', user=current_user), 404

@app.route('/coiki')
@app.route('/')
def carbon_emission():
    return render_template("coiki.html", user=current_user)


@app.route('/coiki_hesapla')
def calculate_carbon():
    return render_template("coiki_hesapla.html", user=current_user)


@app.route('/sonuc', methods=["GET", "POST"])
def results():

    if request.method == 'POST':

        city = request.form.get('place')
        age = request.form.get('age')
        gender = request.form.get('gender')
        education = request.form.get('education')
        work = request.form.get('work')

        new_user = SurveyUser(
            city=city,
            age=age,
            gender=gender,
            education=education,
            work=work
        )
        db.session.add(new_user)
        db.session.commit()

        lcd_is_shared = 0
        computer_is_shared = 0
        laptop_is_shared = 0
        keyboard_is_shared = 0
        mouse_is_shared = 0
        harddisk_is_shared = 0
        network_is_shared = 0
        printer_is_shared = 0
        bike_is_shared = 0
        elect_bike_is_shared = 0
        scooter_is_shared = 0
        elect_car_is_shared = 0
        fuel_car_is_shared = 0
        diesel_car_is_shared = 0


        data = []
        if request.form.get('lcd') and request.form.get('lcd_number') and request.form.get('lcd_sp'):

            cc_lcd = float('336.13')
            sharing_rate_lcd = float(request.form.get('lcd_sp')) / float(request.form.get('lcd_number'))

            lcd_cc_shared = 0
            lcd_cc = 0
            if sharing_rate_lcd > 1:
                lcd_is_shared = 1
                lcd_cc_shared = cc_lcd * (float(request.form.get('lcd_sp')) - float(request.form.get('lcd_number')))
            else:
                lcd_cc = cc_lcd * float(request.form.get('lcd_number'))

            data.append([request.form.get('lcd'),
                         request.form.get('lcd_number'),
                         request.form.get('lcd_sp'),
                         lcd_cc,
                         lcd_cc_shared,
                         lcd_is_shared
                         ])

        if request.form.get('computer') and request.form.get('computer_number') and request.form.get('computer_sp'):

            cc_comp = float('523.42')
            sharing_rate_computer = float(request.form.get('computer_sp')) / float(request.form.get('computer_number'))

            computer_cc_shared = 0
            computer_cc = 0
            if sharing_rate_computer > 1:
                computer_is_shared = 1
                computer_cc_shared = cc_comp * (float(request.form.get('computer_sp')) - float(request.form.get('computer_number')))
            else:
                computer_cc = cc_comp * float(request.form.get('computer_number'))

            data.append([request.form.get('computer'),
                         request.form.get('computer_number'),
                         request.form.get('computer_sp'),
                         computer_cc,
                         computer_cc_shared,
                         computer_is_shared
                         ])

        if request.form.get('laptop') and request.form.get('laptop_number') and request.form.get('laptop_sp'):

            cc_laptop = float('213.67')
            sharing_rate_laptop = float(request.form.get('laptop_sp')) / float(request.form.get('laptop_number'))

            laptop_cc_shared = 0
            laptop_cc = 0
            if sharing_rate_laptop > 1:
                laptop_is_shared = 1
                laptop_cc_shared = cc_laptop * (float(request.form.get('laptop_sp')) - float(request.form.get('laptop_number')))
            else:
                laptop_cc = cc_laptop * float(request.form.get('laptop_number'))

            data.append([request.form.get('laptop'),
                         request.form.get('laptop_number'),
                         request.form.get('laptop_sp'),
                         laptop_cc,
                         laptop_cc_shared,
                         laptop_is_shared
                         ])

        if request.form.get('keyboard') and request.form.get('keyboard_number') and request.form.get('keyboard_sp'):

            cc_kb = float('25.80')
            sharing_rate_keyboard = float(request.form.get('keyboard_sp')) / float(request.form.get('keyboard_number'))

            keyboard_cc_shared = 0
            keyboard_cc = 0
            if sharing_rate_keyboard > 1:
                keyboard_is_shared = 1
                keyboard_cc_shared = cc_kb * (float(request.form.get('keyboard_sp')) - float(request.form.get('keyboard_number')))
            else:
                keyboard_cc = cc_kb * float(request.form.get('keyboard_number'))

            data.append([request.form.get('keyboard'),
                         request.form.get('keyboard_number'),
                         request.form.get('keyboard_sp'),
                         keyboard_cc,
                         keyboard_cc_shared,
                         keyboard_is_shared
                         ])

        if request.form.get('mouse') and request.form.get('mouse_number') and request.form.get('mouse_sp'):

            cc_mouse = float('5.07')
            sharing_rate_mouse = float(request.form.get('mouse_sp')) / float(request.form.get('mouse_number'))

            mouse_cc_shared = 0
            mouse_cc = 0
            if sharing_rate_mouse > 1:
                mouse_is_shared = 1
                mouse_cc_shared = cc_mouse * float(request.form.get('mouse_sp')) - float(request.form.get('mouse_number'))
            else:
                mouse_cc = cc_mouse * float(request.form.get('mouse_number'))

            data.append([request.form.get('mouse'),
                         request.form.get('mouse_number'),
                         request.form.get('mouse_sp'),
                         mouse_cc,
                         mouse_cc_shared,
                         mouse_is_shared
                         ])

        if request.form.get('harddisk') and request.form.get('harddisk_number') and request.form.get('harddisk_sp'):

            cc_hd = float('14.31')
            sharing_rate_harddisk = float(request.form.get('harddisk_sp')) / float(request.form.get('harddisk_number'))

            harddisk_cc_shared = 0
            harddisk_cc = 0
            if sharing_rate_harddisk > 1:
                harddisk_is_shared = 1
                harddisk_cc_shared = cc_hd * (float(request.form.get('harddisk_sp')) - float(request.form.get('harddisk_number')))
            else:
                harddisk_cc = cc_hd * float(request.form.get('harddisk_number'))

            data.append([request.form.get('harddisk'),
                         request.form.get('harddisk_number'),
                         request.form.get('harddisk_sp'),
                         harddisk_cc,
                         harddisk_cc_shared,
                         harddisk_is_shared
                         ])

        if request.form.get('network') and request.form.get('network_number') and request.form.get('network_sp'):

            cc_network = float('6.56')
            sharing_rate_network = float(request.form.get('network_sp')) / float(request.form.get('network_number'))

            network_cc_shared = 0
            network_cc = 0
            if sharing_rate_network > 1:
                network_is_shared = 1
                network_cc_shared = cc_network * (float(request.form.get('network_sp')) - float(request.form.get('network_number')))
            else:
                network_cc = cc_network * float(request.form.get('network_number'))

            data.append([request.form.get('network'),
                         request.form.get('network_number'),
                         request.form.get('network_sp'),
                         network_cc,
                         network_cc_shared,
                         network_is_shared
                         ])

        if request.form.get('printer') and request.form.get('printer_number') and request.form.get('printer_sp'):

            cc_printer = float('66.73')
            sharing_rate_printer = float(request.form.get('printer_sp')) / float(request.form.get('printer_number'))

            printer_cc_shared = 0
            printer_cc = 0
            if sharing_rate_printer > 1:
                printer_is_shared = 1
                printer_cc_shared = cc_printer * (float(request.form.get('printer_sp')) - float(request.form.get('printer_number')))
            else:
                printer_cc = cc_printer * float(request.form.get('printer_number'))

            data.append([request.form.get('printer'),
                         request.form.get('printer_number'),
                         request.form.get('printer_sp'),
                         printer_cc,
                         printer_cc_shared,
                         printer_is_shared
                         ])

        if request.form.get('bike') and request.form.get('bike_number') and request.form.get('bike_sp'):

            cc_bike = float('159.42')
            sharing_rate_bike = float(request.form.get('bike_sp')) / float(request.form.get('bike_number'))

            bike_cc_shared = 0
            bike_cc = 0
            if sharing_rate_bike > 1:
                bike_is_shared = 1
                bike_cc_shared = cc_bike * (float(request.form.get('bike_sp')) - float(request.form.get('bike_number')))
            else:
                bike_cc = cc_bike * float(request.form.get('bike_number'))

            data.append([request.form.get('bike'),
                         request.form.get('bike_number'),
                         request.form.get('bike_sp'),
                         bike_cc,
                         bike_cc_shared,
                         bike_is_shared
                         ])

        if request.form.get('elect_bike') and request.form.get('elect_bike_number') and request.form.get('elect_bike_sp'):

            cc_ebike = float('457.70')
            sharing_rate_elect_bike = float(request.form.get('elect_bike_sp')) / float(request.form.get('elect_bike_number'))

            elect_bike_cc_shared = 0
            elect_bike_cc = 0
            if sharing_rate_elect_bike > 1:
                elect_bike_is_shared = 1
                elect_bike_cc_shared = cc_ebike * (float(request.form.get('elect_bike_sp')) - float(request.form.get('elect_bike_number')))
            else:
                elect_bike_cc = cc_ebike * float(request.form.get('elect_bike_number'))

            data.append([request.form.get('elect_bike'),
                         request.form.get('elect_bike_number'),
                         request.form.get('elect_bike_sp'),
                         elect_bike_cc,
                         elect_bike_cc_shared,
                         elect_bike_is_shared
                         ])

        if request.form.get('scooter') and request.form.get('scooter_number') and request.form.get('scooter_sp'):

            cc_scooter = float('426.05')
            sharing_rate_scooter = float(request.form.get('scooter_sp')) / float(request.form.get('scooter_number'))

            scooter_cc_shared = 0
            scooter_cc = 0
            if sharing_rate_scooter > 1:
                scooter_is_shared = 1
                scooter_cc_shared = cc_scooter * (float(request.form.get('scooter_sp')) - float(request.form.get('scooter_number')))
            else:
                scooter_cc = cc_scooter * float(request.form.get('scooter_number'))

            data.append([request.form.get('scooter'),
                         request.form.get('scooter_number'),
                         request.form.get('scooter_sp'),
                         scooter_cc,
                         scooter_cc_shared,
                         scooter_is_shared
                         ])

        if request.form.get('elect_car') and request.form.get('elect_car_number') and request.form.get('elect_car_sp'):

            cc_ecar = float('13024.78')
            sharing_rate_elect_car = float(request.form.get('elect_car_sp')) / float(request.form.get('elect_car_number'))

            elect_car_cc_shared = 0
            elect_car_cc = 0
            if sharing_rate_elect_car > 1:
                elect_car_is_shared = 1
                elect_car_cc_shared = cc_ecar * (float(request.form.get('elect_car_sp')) - float(request.form.get('elect_car_number')))
            else:
                elect_car_cc = cc_ecar * float(request.form.get('elect_car_number'))

            data.append([request.form.get('elect_car'),
                         request.form.get('elect_car_number'),
                         request.form.get('elect_car_sp'),
                         elect_car_cc,
                         elect_car_cc_shared,
                         elect_car_is_shared
                         ])

        if request.form.get('diesel_car') and request.form.get('diesel_car_number') and request.form.get('diesel_car_sp'):

            cc_dcar = float('10220.12')
            sharing_rate_diesel_car = float(request.form.get('diesel_car_sp')) / float(request.form.get('diesel_car_number'))

            diesel_car_cc_shared = 0
            diesel_car_cc = 0
            if sharing_rate_diesel_car > 1:
                diesel_car_is_shared = 1
                diesel_car_cc_shared = cc_dcar * (float(request.form.get('diesel_car_sp')) - float(request.form.get('diesel_car_number')))
            else:
                diesel_car_cc = cc_dcar * float(request.form.get('diesel_car_number'))

            data.append([request.form.get('diesel_car'),
                         request.form.get('diesel_car_number'),
                         request.form.get('diesel_car_sp'),
                         diesel_car_cc,
                         diesel_car_cc_shared,
                         diesel_car_is_shared
                         ])

        if request.form.get('fuel_car') and request.form.get('fuel_car_number') and request.form.get('fuel_car_sp'):

            cc_fcar = float('10162.44')
            sharing_rate_fuel_car = float(request.form.get('fuel_car_sp')) / float(request.form.get('fuel_car_number'))

            # paylaşarak engellediğin karbon salınımı hesabı
            fuel_car_cc_shared = 0
            fuel_car_cc = 0
            if sharing_rate_fuel_car > 1:
                fuel_car_is_shared = 1
                fuel_car_cc_shared = cc_fcar * (float(request.form.get('fuel_car_sp')) - float(request.form.get('fuel_car_number')))
            else:
                fuel_car_cc = cc_fcar * float(request.form.get('fuel_car_number'))

            data.append([request.form.get('fuel_car'),
                         request.form.get('fuel_car_number'),
                         request.form.get('fuel_car_sp'),
                         fuel_car_cc,
                         fuel_car_cc_shared,
                         fuel_car_is_shared
                         ])

        # sharing_p = 0
        # item_n = 0
        result = 0.0
        sharing_result = 0.0
        for t in data:
            new_survey = Survey(
                user_id=new_user.id,
                item_id=t[0],
                number=t[1],
                using_with=t[2],
                survey_time=datetime.utcnow()
            )
            db.session.add(new_survey)
            db.session.commit()
            t[2] = int(t[2])
            t[1] = int(t[1])

            if t[5] is 1:
                sharing_result = sharing_result + t[4]

            result = result + t[3]

        return render_template('sonuc.html', result=result, sharing_result=sharing_result)

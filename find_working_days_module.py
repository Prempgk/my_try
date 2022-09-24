def find_holiday(calendar_code):
    calendar_model = Calendar_Model.objects.get(id=calendar_code)
    gov_hol_model = calendar_model.Gov_holiday.all()
    gov_holiday = [hol.Start_date for hol in gov_hol_model]
    other_hol_model = calendar_model.Other_holiday.all()
    other_holiday = []
    for i in other_hol_model:
        inbetween_days = (i.End_date - i.Start_date).days + 1
        for j in range(inbetween_days):
            date = i.Start_date + timedelta(days=j)
            other_holiday.append(date)
    exam_schedule_model = Exam_Schedule.objects.filter(Calendar_code=calendar_code)
    exam_schedule = []
    for exam in exam_schedule_model:
        exam_days = (exam.End_date - exam.Start_date).days + 1
        for k in range(exam_days):
            exam_date = exam.Start_date + timedelta(days=k)
            exam_schedule.append(exam_date)
    for i in gov_holiday:
        if i in other_holiday:
            if i in exam_schedule:
                exam_schedule.remove(i)
                other_holiday.remove(i)
            else:
                other_holiday.remove(i)
        if i in exam_schedule:
            exam_schedule.remove(i)
    for j in other_holiday:
        if j in exam_schedule:
            exam_schedule.remove(j)
        else:
            pass
    return gov_holiday, other_holiday, exam_schedule


def find_sat(first, second, third, fourth, fifth, start_month, end_month, start_year, end_year):
    first_sat = []
    second_sat = []
    third_sat = []
    fourth_sat = []
    fifth_sat = []
    for month in range(start_month, 13):  # find the second saturday in starting year
        cal = calendar.monthcalendar(start_year, month)
        if first:
            if cal[0][calendar.SATURDAY]:
                f_sat = cal[0][calendar.SATURDAY]
                first_sat.append(datetime.date(start_year, month, f_sat))
            else:
                f_sat = cal[1][calendar.SATURDAY]
                first_sat.append(datetime.date(start_year, month, f_sat))
        if second:
            if cal[0][calendar.SATURDAY]:
                f_sat = cal[1][calendar.SATURDAY]
                second_sat.append(datetime.date(start_year, month, f_sat))
            else:
                f_sat = cal[2][calendar.SATURDAY]
                second_sat.append(datetime.date(start_year, month, f_sat))
        if third:
            if cal[0][calendar.SATURDAY]:
                f_sat = cal[2][calendar.SATURDAY]
                third_sat.append(datetime.date(start_year, month, f_sat))
            else:
                f_sat = cal[3][calendar.SATURDAY]
                third_sat.append(datetime.date(start_year, month, f_sat))
        if fourth:
            if cal[0][calendar.SATURDAY]:
                f_sat = cal[3][calendar.SATURDAY]
                fourth_sat.append(datetime.date(start_year, month, f_sat))
            else:
                f_sat = cal[4][calendar.SATURDAY]
                fourth_sat.append(datetime.date(start_year, month, f_sat))
        if fifth:
            if cal[0][calendar.SATURDAY]:
                if cal[4][calendar.SATURDAY]:
                    f_sat = cal[4][calendar.SATURDAY]
                    fifth_sat.append(datetime.date(start_year, month, f_sat))

    for month in range(1, end_month):  # find the second saturday in starting year
        cal = calendar.monthcalendar(end_year, month)
        if first:
            if cal[0][calendar.SATURDAY]:
                f_sat = cal[0][calendar.SATURDAY]
                first_sat.append(datetime.date(end_year, month, f_sat))
            else:
                f_sat = cal[1][calendar.SATURDAY]
                first_sat.append(datetime.date(end_year, month, f_sat))
        if second:
            if cal[0][calendar.SATURDAY]:
                f_sat = cal[1][calendar.SATURDAY]
                second_sat.append(datetime.date(end_year, month, f_sat))
            else:
                f_sat = cal[2][calendar.SATURDAY]
                second_sat.append(datetime.date(end_year, month, f_sat))
        if third:
            if cal[0][calendar.SATURDAY]:
                f_sat = cal[2][calendar.SATURDAY]
                third_sat.append(datetime.date(end_year, month, f_sat))
            else:
                f_sat = cal[3][calendar.SATURDAY]
                third_sat.append(datetime.date(end_year, month, f_sat))
        if fourth:
            if cal[0][calendar.SATURDAY]:
                f_sat = cal[3][calendar.SATURDAY]
                fourth_sat.append(datetime.date(end_year, month, f_sat))
            else:
                f_sat = cal[4][calendar.SATURDAY]
                fourth_sat.append(datetime.date(end_year, month, f_sat))
        if fifth:
            if cal[0][calendar.SATURDAY]:
                if cal[4][calendar.SATURDAY]:
                    f_sat = cal[4][calendar.SATURDAY]
                    fifth_sat.append(datetime.date(end_year, month, f_sat))
    return first_sat, second_sat, third_sat, fourth_sat, fifth_sat


def find_working_day(calendar_code):
    a = Calendar_Model.objects.get(id=calendar_code)
    start_date = a.School_reopen
    end_date = a.Last_working_day
    start_month = start_date.month
    end_month = end_date.month
    start_year = start_date.year
    end_year = end_date.year
    first = a.First_sat
    second = a.Sec_sat
    third = a.Third_sat
    fourth = a.Fourth_sat
    fifth = a.Fifth_sat
    working_days_per_week = a.Working_day
    non_working_days_per_week = []
    weekday_of_non_working_days = []
    for i in range(7):
        if str(i) in working_days_per_week:
            pass
        else:
            weekday_of_non_working_days.append(i)
            non_working_days_per_week.append(calendar.day_name[i])
    week = {}
    for i in range((end_date + timedelta(days=1) - start_date).days):  # find the  no of days between two dates
        day = calendar.day_name[(start_date + timedelta(days=i)).weekday()]
        week[day] = week[day] + 1 if day in week else 1
    for day_name in non_working_days_per_week:
        if day_name in week.keys():
            week[day_name] = 0
    sat = find_sat(first, second, third, fourth, fifth, start_month, end_month, start_year, end_year)
    all_sat = sat[0] + sat[1] + sat[2] + sat[3] + sat[4]
    hol = find_holiday(calendar_code)
    non_work_day = hol[0] + hol[1] + hol[2]
    for i in non_work_day:
        if first:
            if i in sat[0]:
                non_work_day.remove(i)
                all_sat.remove(i)
        if second:
            if i in sat[1]:
                non_work_day.remove(i)
                all_sat.remove(i)
        if third:
            if i in sat[2]:
                non_work_day.remove(i)
                all_sat.remove(i)
        if fourth:
            if i in sat[3]:
                non_work_day.remove(i)
                all_sat.remove(i)
        if fifth:
            if i in sat[4]:
                non_work_day.remove(i)
                all_sat.remove(i)
        if i.weekday() in weekday_of_non_working_days:
            if i in non_work_day:
                non_work_day.remove(i)
        else:
            pass
    total_working_days = sum(week.values()) + len(all_sat) - len(non_work_day)
    return total_working_days
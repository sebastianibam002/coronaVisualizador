from users.models import Afiliado, Period
import csv
import os
import mimetypes
from django.http.response import HttpResponse
from django.utils import timezone
from typing import List
from datetime import datetime, timedelta

def filter_period(month: int, year: int) -> List:
    """
    Given the period_look it returns a list that contains all the
    people that are in the given search
    1-2021
    """
    p = str(month) + "-" + str(year)
    return Period.objects.filter(period=p)

def filter_state(state_look: str) -> List:
    """
    Given an state G, B, P it looks over all the elements in the database and
    returns a list with the people that are in that state
    """
    return Afiliado.objects.filter(state=state_look)

def stats_state_and_period() -> List:
    """
    Returns two lists limited to number of people filtered by state and by period
    """
    
    # get all the period and iterate over that
    labels = []
    values = []
    all_per = Period.objects.all()
    all_per_edited = []
    for item in all_per:
        all_per_edited.append(item.period)

    # convert this list of all the periods in one that contains just once
    ls = []
    unique = set(all_per_edited)

    all_per = list(set(all_per_edited))    

    # get the elements of the periods and start counting
    for per in all_per:
        # good first
        labels.append(f"{per}-Bien")
        values.append(len(Period.objects.filter(period=per, state="G")))
        labels.append(f"{per}-Mal")
        values.append(len(Period.objects.filter(period=per, state="B")))
    
    return limit_to(5, labels, values)


def stats_bad_by_state() -> List:
    """
    returns a list that containst by percentage the reason what part of the process people failed the most
    """
    all_bad_people = len(filter_state("B"))
    # get just the columns that has a bad 
    bad_filter_one = (len(Afiliado.objects.filter(first_val="B")) / all_bad_people) * 100
    bad_filter_two = (len(Afiliado.objects.filter(second_val="B")) / all_bad_people) * 100
    bad_filter_three = (len(Afiliado.objects.filter(third_val="B")) / all_bad_people) * 100
    return [bad_filter_one, bad_filter_two, bad_filter_three]


def all_people() -> List:
    """
    Returns all the people in the current databse
    """
    return Afiliado.objects.all()


def stats_by_state():
    """
    Returns a list with the size of the G, B, D and another with the labels but just of the current period
  
    """
    # get the data of all the actual periods
    tod = datetime.today()
    today_month = tod.month
    today_year = tod.year
    ls_size = []
    dic = {'G': 0, 'B': 0, 'P': 0}
    for element in filter_period(today_month, today_year):
        # the type of element is a period
        dic[element.state] += 1
    
    ls_key, ls_value =  turn_into_lists(dic)

    return ls_value, ls_key


def turn_into_lists(dic_p):
    """
    Given a dictionary returns two lists one with the keys 
    one with the values
    """
    ls_keys = []
    ls_values = []
    for a in dic_p:
        ls_keys.append(a)
        ls_values.append(dic_p[a])
    return ls_keys, ls_values

def limit_to(number: int, ls_keys: List, ls_values: List):
    """
    Limits both lists to the last number results
    """
    ls_key_one, ls_val_two = [], []
    len_val = len(ls_keys)
    if len_val - number > 0:
        for a in range(len_val, len_val - number, -1):
            ls_key_one.append(ls_keys[a])
            ls_val_two.append(ls_values[a])

        ls_key_one.sort()
        ls_val_two.sort()

        return ls_key_one, ls_val_two
    ls_key_one.sort()
    # ls_val_two.sort()

    return ls_keys, ls_values

    

def stats_historic():
    """
    Returns an x period y lists number of people with each of the elements
    """
    # get all the periods
    all_periods = Period.objects.all()
    dic_periods = {}
    for per in all_periods:
        if per.period in dic_periods:
            dic_periods[per.period] += 1
        else:
            dic_periods[per.period] = 1
    
    # i will limit the results to just 5 periods max
    ls_key, ls_val = turn_into_lists(dic_periods)
    return limit_to(5, ls_key, ls_val)

def filter_range(from_month: int, from_year: int, to_month: int, to_year: int) -> List:
    """
    Returns a list of all the people among from - to. 
    It isn't necessary that the month should be included, could just the if there 
    are people there
    """
    # from_date = datetime(month=from_month, day= 1, year=from_year)
    # to_date = datetime(month=to_month, day=28, year=to_date )
    # get the total months and iterate over that number
    ls_return = []
    total_months = (to_year - from_year) * 12 + (to_month - from_month)
    from_date = datetime(month=from_month, day= 1, year=from_year)
    for month in range(total_months):
        # get the data of the first one if posible
        val = filter_period(from_date.month, from_date.year)
        ls_return.extend(val)
        # 32 days go over months
        time = timedelta(days=32)
        from_date = from_date + time
        # change the day to be just 1
        if from_date.day != 1:
            waste = from_date.day - 1
            from_date = from_date - timedelta(days=waste)

    # check the last one
    val = filter_period(from_date.month, from_date.year)
    ls_return.extend(val)

    return ls_return



from datetime import datetime, timedelta



def convertJulianToDateString(serial_date):
    """
    Convert Julian day to date
    :param julianDay: Julian day
    :return: Date in the format YYYY-MM-DD
    """
    base_date = datetime(1901, 1, 1)  # Excel's base date
    converted_date = base_date + timedelta(days=serial_date-1) 
    return converted_date.strftime("%d %B %Y")


def calculateAquaCropJulianDay(date_obj):
    """
    Calculate AquaCrop Julian day for a given date
    :param date_obj: A datetime.date object
    :return: Julian day number according to AquaCrop's system
    """
    # AquaCrop uses January 1, 2014 as day 41274
    reference_date = datetime(2014, 1, 1).date()
    reference_day = 41274
    
    # Calculate days difference
    delta = date_obj - reference_date
    
    # Add difference to reference day
    julian_day = reference_day + delta.days
    
    return julian_day
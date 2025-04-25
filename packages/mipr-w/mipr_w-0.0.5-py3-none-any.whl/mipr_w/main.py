import pandas as pd


def read_crash(directory):
    dates = ['CRASH_DATE_AND_TIME', 'REPORT_DATE_AND_TIME', 'NOTIFIED_TIME', 'DISPATCHED_TIME', 'ARRIVED_TIME',
                 'CLEARED_TIME']
    crash = pd.read_csv(directory + r'\crash_event.csv', parse_dates=dates)
    return crash

def read_crash_non_date(directory):
    crash = pd.read_csv(directory + r'\crash_event.csv')
    return crash

def read_driver(directory):
    driver = pd.read_csv(directory + r'\driver.csv')
    return driver

def read_vehicle(directory):
    vehicle = pd.read_csv(directory + r'\vehicle.csv')
    return vehicle

def read_passenger(directory):
    passenger = pd.read_csv(directory + r'\passenger.csv')
    return passenger

def read_non_motorist(directory):
    non_motorist = pd.read_csv(directory + r'\non_motorist.csv')
    return non_motorist

def read_violation(directory):
    violation = pd.read_csv(directory + r'\violation.csv')
    return violation


def impaired_driver(x):
    return x[(x.BLOOD_ALCOHOL_CONTENT > 0) | (x.DRUG_TEST_RESULTS == 'Positive') | (x.SUSPECTED_DRUG_USE_CODE == 'Y') | ( x.SUSPECTED_ALCOHOL_USE_CODE == 'Y') | (x.ALCOHOL_TESTED_CODE == 'Test Refused') | (x.DRUG_TESTED_CODE == 'Test Refused')]

def alcohol_driver(x):
    df = x[(x.BLOOD_ALCOHOL_CONTENT > 0) | (x.SUSPECTED_ALCOHOL_USE_CODE == 'Y') | ( x.ALCOHOL_TESTED_CODE == 'Test Refused')]
    return df

def drug_driver(x):
    return x[(x.DRUG_TEST_RESULTS == 'Positive') | (x.SUSPECTED_DRUG_USE_CODE == 'Y') | ( x.DRUG_TESTED_CODE == 'Test Refused')]

def add_alcohol_col(x):
    df = x[(x.BLOOD_ALCOHOL_CONTENT > 0) | (x.SUSPECTED_ALCOHOL_USE_CODE == 'Y') | ( x.ALCOHOL_TESTED_CODE == 'Test Refused')]
    df['alcohol'] = 1 
    col_list = list(x.columns)
    merged = x.merge(df, on = col_list, how='left')
    merged.alcohol.fillna(0, inplace=True)
    return merged

def add_drug_col(x):
    df = x[(x.DRUG_TEST_RESULTS == 'Positive') | (x.SUSPECTED_DRUG_USE_CODE == 'Y') | ( x.DRUG_TESTED_CODE == 'Test Refused')]
    df['drug'] = 1 
    col_list = list(x.columns)
    merged = x.merge(df, on = col_list, how='left')
    merged.drug.fillna(0, inplace=True)
    return merged

def add_impair_col(x):
    df = x[(x.BLOOD_ALCOHOL_CONTENT > 0) | (x.DRUG_TEST_RESULTS == 'Positive') | (x.SUSPECTED_DRUG_USE_CODE == 'Y') | ( x.SUSPECTED_ALCOHOL_USE_CODE == 'Y') | (x.ALCOHOL_TESTED_CODE == 'Test Refused') | (x.DRUG_TESTED_CODE == 'Test Refused')]
    df['impair'] = 1 
    col_list = list(x.columns)
    merged = x.merge(df, on = col_list, how='left')
    merged.impair.fillna(0, inplace=True)
    return merged

def fatal_including_moped(directory):
    crash = pd.read_csv(directory + r'\crash tables\crash_event.csv')
    driver = pd.read_csv(directory + r'\crash tables\driver.csv')
    vehicle = pd.read_csv(directory + r'\crash tables\vehicle.csv')
    passenger = pd.read_csv(directory + r'\crash tables\passenger.csv')
    veh_mc_moped = vehicle[vehicle.TYPE_OF_VEHICLE.isin(['Motorcycle', 'Moped'])]
    driver_injury = driver[driver.INJURY_SEVERITY == 'Fatal (within 30 days)']
    pass_injury = passenger[passenger.INJURY_SEVERITY == 'Fatal (within 30 days)']
    driver_injury_mc_moped = driver_injury.merge(veh_mc_moped, on = ['REPORT_NUMBER','CRASH_YEAR', 'VEHICLE_NUMBER'])
    pass_injury_mc_moped = pass_injury.merge(veh_mc_moped, on = ['REPORT_NUMBER','CRASH_YEAR', 'VEHICLE_NUMBER'])
    return f' Driver: {len(driver_injury_mc_moped)} , Passenger: {len(pass_injury_mc_moped)}, Total: {len(driver_injury_mc_moped) + len(pass_injury_mc_moped)}'

def serious_including_moped(directory):
    crash = pd.read_csv(directory + r'\crash tables\crash_event.csv')
    driver = pd.read_csv(directory + r'\crash tables\driver.csv')
    vehicle = pd.read_csv(directory + r'\crash tables\vehicle.csv')
    passenger = pd.read_csv(directory + r'\crash tables\passenger.csv')
    veh_mc_moped = vehicle[vehicle.TYPE_OF_VEHICLE.isin(['Motorcycle', 'Moped'])]
    driver_serious = driver[driver.INJURY_SEVERITY == 'Incapacitating']
    pass_serious = passenger[passenger.INJURY_SEVERITY == 'Incapacitating']
    driver_serious_mc_moped = driver_serious.merge(veh_mc_moped, on = ['REPORT_NUMBER','CRASH_YEAR', 'VEHICLE_NUMBER'])
    pass_serious_mc_moped = pass_serious.merge(veh_mc_moped, on = ['REPORT_NUMBER','CRASH_YEAR', 'VEHICLE_NUMBER'])
    return f'Driver: {len(driver_serious_mc_moped)}, Passenger: { len(pass_serious_mc_moped )}, Total: {len(driver_serious_mc_moped) + len(pass_serious_mc_moped ) }'


def fatal_mc_by_year(directory):
    crash = pd.read_csv(directory + r'\crash tables\crash_event.csv')
    driver = pd.read_csv(directory + r'\crash tables\driver.csv')
    vehicle = pd.read_csv(directory + r'\crash tables\vehicle.csv')
    passenger = pd.read_csv(directory + r'\crash tables\passenger.csv')
    veh_mc = vehicle[vehicle.TYPE_OF_VEHICLE.isin(['Motorcycle'])]
    driver_injury = driver[driver.INJURY_SEVERITY == 'Fatal (within 30 days)']
    pass_injury = passenger[passenger.INJURY_SEVERITY == 'Fatal (within 30 days)']
    driver_injury_mc = driver_injury.merge(veh_mc, on = ['REPORT_NUMBER','CRASH_YEAR', 'VEHICLE_NUMBER'])
    pass_injury_mc = pass_injury.merge(veh_mc, on = ['REPORT_NUMBER','CRASH_YEAR', 'VEHICLE_NUMBER'])
    return f' Driver: {len(driver_injury_mc)} , Passenger: {len(pass_injury_mc)}, Total: {len(driver_injury_mc) + len(pass_injury_mc)}'

def serious_mc_by_year(directory):
    crash = pd.read_csv(directory + r'\crash tables\crash_event.csv')
    driver = pd.read_csv(directory + r'\crash tables\driver.csv')
    vehicle = pd.read_csv(directory + r'\crash tables\vehicle.csv')
    passenger = pd.read_csv(directory + r'\crash tables\passenger.csv')
    veh_mc = vehicle[vehicle.TYPE_OF_VEHICLE.isin(['Motorcycle'])]
    driver_serious = driver[driver.INJURY_SEVERITY == 'Incapacitating']
    driver_serious_mc = driver_serious.merge(veh_mc, on = ['REPORT_NUMBER','CRASH_YEAR', 'VEHICLE_NUMBER'])
    pass_serious = passenger[passenger.INJURY_SEVERITY == 'Incapacitating']
    driver_serious_mc = driver_serious.merge(veh_mc, on = ['REPORT_NUMBER','CRASH_YEAR', 'VEHICLE_NUMBER'])
    pass_serious_mc = pass_serious.merge(veh_mc, on = ['REPORT_NUMBER','CRASH_YEAR', 'VEHICLE_NUMBER'])
    return f'Driver: {len(driver_serious_mc)}, Passenger: { len(pass_serious_mc)}, Total: {len(driver_serious_mc) + len(pass_serious_mc) }'

def injury_vehicle_by_year(directory, injury_severity, vehicle_list):
    crash = pd.read_csv(directory + r'\crash tables\crash_event.csv')
    driver = pd.read_csv(directory + r'\crash tables\driver.csv')
    vehicle = pd.read_csv(directory + r'\crash tables\vehicle.csv')
    passenger = pd.read_csv(directory + r'\crash tables\passenger.csv')
    veh_mc = vehicle[vehicle.TYPE_OF_VEHICLE.isin(vehicle_list)]
    driver_serious = driver[driver.INJURY_SEVERITY == injury_severity]
    driver_serious_mc = driver_serious.merge(veh_mc, on = ['REPORT_NUMBER','CRASH_YEAR', 'VEHICLE_NUMBER'])
    pass_serious = passenger[passenger.INJURY_SEVERITY == injury_severity]
    driver_serious_mc = driver_serious.merge(veh_mc, on = ['REPORT_NUMBER','CRASH_YEAR', 'VEHICLE_NUMBER'])
    pass_serious_mc = pass_serious.merge(veh_mc, on = ['REPORT_NUMBER','CRASH_YEAR', 'VEHICLE_NUMBER'])
    return f'Driver: {len(driver_serious_mc)}, Passenger: { len(pass_serious_mc)}, Total: {len(driver_serious_mc) + len(pass_serious_mc) }'

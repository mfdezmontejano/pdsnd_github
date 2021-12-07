import time
import datetime as dt
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    # get user input for city (chicago, new york city, washington)
    
    print('Hello! Let\'s explore some US bikeshare data!')
    k = 0
    cities = ['chicago','new york city','washington']
    while k == 0:
        city = input('\nPlease write the city you want to know data about among Chicago, New York City and Washington:\n').lower()
        for i in range(len(cities)):
            if city in cities[i]:
                conf = input('To confirm \'{}\' write \'c\':\n'.format(cities[i].title()))
                if conf == 'c':
                    city = cities[i]
                    k +=1
                    break

        if k == 0:
            print('Your previous input seems to be wrong.')
  
    # get user input for month (all, january, february, ... , june)

    k = 0
    months = ['0all','1january','2february','3march','4april','5may','6june']
    while k == 0:
        month = input('\nPlease write the month you want to know data about from January to June (Write \'all\' if you don\'t want to filter by month):\n').lower()
        for i in range(len(months)):
            if month in months[i]:
                conf = input('To confirm \'{}\' write \'c\':\n'.format(months[i][1:].title()))
                if conf == 'c':
                    month = months[i][1:]
                    k +=1
                    break

        if k == 0:
            print('Your previous input seems to be wrong. ')

    # get user input for day of week (all, monday, tuesday, ... sunday)

    k = 0
    week_d = ['0all','1monday','2tuesday','3wednesday','4thursday','5friday','6saturday','7sunday']
    while k == 0:
        day = input('\nPlease write the week day you want to know data about (Write \'all\' if you don\'t want to filter by week day):\n').lower()
        for i in range(len(week_d)):
            if day in week_d[i]:
                conf = input('To confirm \'{}\' write \'c\':\n'.format(week_d[i][1:].title()))
                if conf == 'c':
                    day = week_d[i][1:]
                    k +=1
                    break

        if k == 0:
            print('Your previous input seems to be wrong.')

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city], header=0)
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.strftime("%B")
    df['Day_of_week'] = df['Start Time'].dt.strftime('%A')
    
    if month != 'all':
        df = df[df['Month'] == month.title()]

    if day != 'all':
        df = df[df['Day_of_week'] == day.title()]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    
    input('Start time stats calculations')
    
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if len(np.unique(df['Month'])) != 1:
        print('The most frequent month is: {}'.format(df['Month'].mode()[0]))

    # display the most common day of week
    if len(np.unique(df['Day_of_week'])) != 1:
        print('The most frequent day of the week is: {}'.format(df['Day_of_week'].mode()[0]))

    # display the most common start hour
    print('The most frequent start hour: {}'.format(df['Start Time'].dt.hour.mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    
    input('Start stations and trips stats calculations')

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most commonly used start station: {}'.format(df['Start Station'].mode()[0]))

    # display most commonly used end station
    print('The most commonly used end station: {}'.format(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    comb = df['Start Station'] + ' - ' + df['End Station']
    print('The most frequent combination used: {}'.format(comb.mode()[0]))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    
    input('Start trip duration stats calculations')
    
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    durat_total = float(df['Trip Duration'].sum())
    durat_total_days = int(durat_total/(24*60*60))
    durat_total_hours = int((durat_total%(24*60*60))/(60*60))
    durat_total_mins = int(((durat_total%(24*60*60))%(60*60))/60)
    durat_total_secs = int(((durat_total%(24*60*60))%(60*60))%60)
    
    print('The total trip duration is: {} days {} hours {} mins and {} s'.format(durat_total_days,durat_total_hours,durat_total_mins,durat_total_secs))

    # display mean travel time
    durat_aver = float(df['Trip Duration'].mean())
    durat_aver_mins = int(durat_aver/60)
    durat_aver_secs = int(durat_aver%60)
    
    print('The average trip duration is: {} mins and {} s'.format(durat_aver_mins,durat_aver_secs))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    
    input('Start users stats calculations')
    
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    utype_count = df.groupby(['User Type'])['User Type'].count()
    print('Number of users by type:')
    for utype in utype_count.index:
        print('{}: {}'.format(str(utype), utype_count[utype]))
    
    # Display counts of gender
    if 'Gender' in df:
        gender_count = df.groupby(['Gender'])['Gender'].count()
        print('\nNumber of users by Gender:')    
        for gender in gender_count.index:
            print('{}: {}'.format(str(gender), gender_count[gender]))      

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        print('\nThe oldest user was born in {}'.format(int(df['Birth Year'].min())))
        print('The youngest user was born in {}'.format(int(df['Birth Year'].max())))
        print('The most common year of birth among users is {}'.format(int(df['Birth Year'].mode())))
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        ques = input('Do you want to see a sample of the analyzed data? (\'y\' for yes): ')
        if ques == 'y':
            i = 0
            while ques == 'y':
                j = i + 5
                if j > len(df):
                    j = len(df) + 1
                    print(df[i:j])
                    break
                else:
                    print(df[i:j])
                print('There are {} rows left'.format(len(df)-j))
                ques = input('\nDo you want to continue seeing more? (\'y\' for yes):\n')
                i += 5
                
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

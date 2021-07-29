import time
import datetime
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

def get_filters():
    """Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('-' * 40)
    print('Hello! Let\'s explore some US bikeshare data!\n')

    # Get user input for city (chicago, new york city, washington). Handle invalid inputs with while loop
    while True:
        city = input('Please choose a city name from Chicago, New York City or Washington: ').lower()
        if city not in CITY_DATA.keys():
            print('Choose a city as mentioned before please.')
        else:
            break

    # Get user input for month (all, january, february, ... , june). Handle invalid inputs with while loop
    given_months = ['january', 'february', 'march', 'april', 'may', 'june']
    while True:
        month = input(
            'Choose one of the following months please --> January, February, March, April, May, June: ').lower()
        if month not in given_months:
            print('Please choose one of the given months.')
        else:
            break

    # Get user input for day of week (all, monday, tuesday, ... sunday). Handle invalid inputs with while loop
    given_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    while True:
        day = input('Choose a day of the week or choose all days to view data from all days: ').lower()
        if day not in given_days:
            print('Check your writing please and try again.')
        else:
            break
    print('-' * 40)
    return city, month, day

def display_data(df):
    # set beginning and end of data to display
    begin_data = 0
    end_data = 5
    while True:
        show_data = input('\nWould you like to see 5 rows of individual travel data? Enter yes or no please.\n ')
        if show_data.lower() != 'yes':
            break
        else:
            print(df[df.columns[0:]].iloc[begin_data:end_data]) # iloc to access multiple numerical indices
            begin_data += 5
            end_data += 5

def load_data(city, month, day):
    """Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    if month != 'all':
        given_months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = given_months.index(month) + 1
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    # Displays statistics on the most frequent times of travel.

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most frequent month.
    most_frequent_month = df['month'].mode()[0]
    print('Most frequent month: ', most_frequent_month)

    # display the most frequent day of week.
    most_frequent_day = df['day_of_week'].mode()[0]
    print('Most frequent day: ', most_frequent_day)

    # display the most common start hour.
    df['hour'] = df['Start Time'].dt.hour
    most_frequent_start_hour = df['Start Time'].mode()[0]

    print('Most frequent start hour: ', most_frequent_start_hour)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def station_stats(df):
    # Displays statistics on the most popular stations and trip.

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station.
    most_frequent_start_station = df['Start Station'].mode()[0]
    print('Most frequent start station: ', most_frequent_start_station)

    # display most commonly used end station.
    most_frequent_end_station = df['End Station'].mode()[0]
    print('Most frequent end station:   ', most_frequent_end_station)

    # display most frequent combination of start station and end station trip.
    combi_start_end_station = df.groupby(['Start Station', 'End Station']).count().idxmax()[0]
    print('Most frequent combination of start and end stations:', combi_start_end_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def trip_duration_stats(df):
    # Displays statistics on the total and average trip duration.

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time showing hours, minutes and seconds.
    total_travel_time = df['Trip Duration'].sum()
    total_travel_time = time.strftime("%H:%M:%S", time.gmtime(total_travel_time))
    print('Total travel time: ', total_travel_time)

    # display mean travel time showing hours, minutes and seconds.
    mean_travel_time = df['Trip Duration'].mean()
    mean_travel_time = time.strftime("%H:%M:%S", time.gmtime(mean_travel_time))
    print('Mean travel time:  ', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def user_stats(df):
    # Displays statistics on bikeshare users.

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types.
    print('Number of user types: ')
    print(df['User Type'].value_counts())

    # Display counts of gender.
    if 'Gender' not in df.columns:  # Gender column not in file washington
        print('No gender info available.')
    else:
        print('Number of gender: ')
        print(df['Gender'].value_counts())

    # Display earliest(min), most recent(max), and most common year of birth(mode).
    if 'Birth Year' in df.columns:  # columns Birth Year not in everywhere file.
        min_birth_year = df['Birth Year'].min()
        print('Oldest person with year of birth: ', min_birth_year)
        max_birth_year = df['Birth Year'].max()
        print('Youngest person with year of birth: ', max_birth_year)
        most_common_year = df['Birth Year'].mode()[0]
        print('Most common year: ', most_common_year)
    else:
        print('Year of birth info not available.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
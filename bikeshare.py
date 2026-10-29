import time
import pandas as pd
import numpy as np

# Maps city names to their respective CSV file paths
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Prompts the user for three inputs:
      - city: one of chicago, new york city, or washington
      - month: one of january through june, or 'all' for no filter
      - day: a day of the week (e.g. monday), or 'all' for no filter

    All inputs are case-insensitive and validated in a loop until valid.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington)
    cities = ['chicago', 'new york city', 'washington']
    while True:
        city = input('\nWould you like to see data for Chicago, New York City, or Washington?\n').lower().strip()
        if city in cities:
            break
        print('That\'s not a valid city. Please enter Chicago, New York City, or Washington.')

    # get user input for month (all, january, february, ... , june)
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    while True:
        month = input('\nWhich month? all, January, February, March, April, May, or June?\n').lower().strip()
        if month in months:
            break
        print('Invalid month. Please try again.')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    while True:
        day = input('\nWhich day? all, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\n').lower().strip()
        if day in days:
            break
        print('Invalid day. Please try again.')

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Reads the CSV file for the given city, converts the 'Start Time' column to
    datetime, and extracts month, day of week, and hour as new columns. Then
    filters the DataFrame based on the provided month and day values.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter

    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

    # convert Start Time to datetime and extract useful columns
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if needed
    if month != 'all':
        month_list = ['january', 'february', 'march', 'april', 'may', 'june']
        month_num = month_list.index(month) + 1
        df = df[df['month'] == month_num]

    # filter by day if needed
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.

    Computes and prints:
      - The most common month (among filtered data)
      - The most common day of the week
      - The most common start hour

    Args:
        df - Pandas DataFrame containing bikeshare data

    Returns:
        None
    """
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    month_names = ['January', 'February', 'March', 'April', 'May', 'June']
    common_month = df['month'].mode()[0]
    print('Most Common Month:', month_names[common_month - 1])

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('Most Common Day of Week:', common_day)

    # display the most common start hour
    common_hour = df['hour'].mode()[0]
    print('Most Common Start Hour:', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.

    Computes and prints:
      - Most commonly used start station
      - Most commonly used end station
      - Most frequent combination of start and end station

    Args:
        df - Pandas DataFrame containing bikeshare data

    Returns:
        None
    """
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start = df['Start Station'].mode()[0]
    print('Most Common Start Station:', common_start)

    # display most commonly used end station
    common_end = df['End Station'].mode()[0]
    print('Most Common End Station:', common_end)

    # display most frequent combination of start station and end station trip
    df['trip'] = df['Start Station'] + ' -> ' + df['End Station']
    common_trip = df['trip'].mode()[0]
    print('Most Common Trip:', common_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.

    Computes total travel time and mean travel time from the
    'Trip Duration' column (values are in seconds).

    Args:
        df - Pandas DataFrame containing bikeshare data

    Returns:
        None
    """
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    total_hours = int(total_time // 3600)
    total_mins = int((total_time % 3600) // 60)
    print('Total Travel Time: {} hours and {} minutes'.format(total_hours, total_mins))

    # display mean travel time
    mean_time = df['Trip Duration'].mean()
    mean_mins = int(mean_time // 60)
    mean_secs = int(mean_time % 60)
    print('Mean Travel Time: {} minutes and {} seconds'.format(mean_mins, mean_secs))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """
    Displays statistics on bikeshare users.

    Computes and prints:
      - Counts of each user type (Subscriber, Customer, etc.)
      - Counts by gender (only available for Chicago and New York City)
      - Earliest, most recent, and most common birth year (not available for Washington)

    Args:
        df - Pandas DataFrame containing bikeshare data

    Returns:
        None
    """
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('User Types:\n', user_types.to_string())

    # Display counts of gender (not available for Washington)
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print('\nGender Counts:\n', gender_counts.to_string())
    else:
        print('\nGender data not available for this city.')

    # Display earliest, most recent, and most common year of birth (not available for Washington)
    if 'Birth Year' in df.columns:
        earliest = int(df['Birth Year'].min())
        most_recent = int(df['Birth Year'].max())
        most_common = int(df['Birth Year'].mode()[0])
        print('\nEarliest Birth Year:', earliest)
        print('Most Recent Birth Year:', most_recent)
        print('Most Common Birth Year:', most_common)
    else:
        print('Birth year data not available for this city.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(df):
    """
    Displays 5 rows of raw data at a time upon user request.

    Prompts the user repeatedly asking if they want to see 5 more rows.
    Continues until the user answers 'no' or there is no more data.

    Args:
        df - Pandas DataFrame containing bikeshare data

    Returns:
        None
    """
    i = 0
    while i < len(df):
        show = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n').lower().strip()
        if show == 'yes':
            print(df.iloc[i:i+5].to_string())
            i += 5
            if i >= len(df):
                print('\nNo more raw data to display.')
                break
        elif show == 'no':
            break
        else:
            print('Please enter yes or no.')


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

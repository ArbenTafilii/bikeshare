import time
import pandas as pd
import numpy as np

# Maps city names to their respective CSV file paths
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_valid_input(prompt, valid_options):
    """Prompts user until a valid option is entered. Returns the lowercased input."""
    while True:
        user_input = input(prompt).lower().strip()
        if user_input in valid_options:
            return user_input
        print('Invalid input. Please try again.')


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

    city = get_valid_input(
        '\nWould you like to see data for Chicago, New York City, or Washington?\n',
        list(CITY_DATA.keys())
    )

    month = get_valid_input(
        '\nWhich month? all, January, February, March, April, May, or June?\n',
        ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    )

    day = get_valid_input(
        '\nWhich day? all, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\n',
        ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    )

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

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        month_list = ['january', 'february', 'march', 'april', 'may', 'june']
        df = df[df['month'] == month_list.index(month) + 1]

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

    month_names = ['January', 'February', 'March', 'April', 'May', 'June']
    print('Most Common Month:', month_names[df['month'].mode()[0] - 1])
    print('Most Common Day of Week:', df['day_of_week'].mode()[0])
    print('Most Common Start Hour:', df['hour'].mode()[0])

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

    print('Most Common Start Station:', df['Start Station'].mode()[0])
    print('Most Common End Station:', df['End Station'].mode()[0])

    df['trip'] = df['Start Station'] + ' -> ' + df['End Station']
    print('Most Common Trip:', df['trip'].mode()[0])

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

    total_time = int(df['Trip Duration'].sum())
    print('Total Travel Time: {} hours and {} minutes'.format(total_time // 3600, (total_time % 3600) // 60))

    mean_time = int(df['Trip Duration'].mean())
    print('Mean Travel Time: {} minutes and {} seconds'.format(mean_time // 60, mean_time % 60))

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

    print('User Types:\n', df['User Type'].value_counts().to_string())

    if 'Gender' in df.columns:
        print('\nGender Counts:\n', df['Gender'].value_counts().to_string())
    else:
        print('\nGender data not available for this city.')

    if 'Birth Year' in df.columns:
        print('\nEarliest Birth Year:', int(df['Birth Year'].min()))
        print('Most Recent Birth Year:', int(df['Birth Year'].max()))
        print('Most Common Birth Year:', int(df['Birth Year'].mode()[0]))
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
        show = get_valid_input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n', ['yes', 'no'])
        if show == 'yes':
            print(df.iloc[i:i+5].to_string())
            i += 5
            if i >= len(df):
                print('\nNo more raw data to display.')
                break
        else:
            break


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

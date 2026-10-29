import time
import pandas as pd
import numpy as np

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
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    month_names = ['January', 'February', 'March', 'April', 'May', 'June']
    print('Most Common Month:', month_names[df['month'].mode()[0] - 1])
    print('Most Common Day of Week:', df['day_of_week'].mode()[0])
    print('Most Common Start Hour:', df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    print('Most Common Start Station:', df['Start Station'].mode()[0])
    print('Most Common End Station:', df['End Station'].mode()[0])

    df['trip'] = df['Start Station'] + ' -> ' + df['End Station']
    print('Most Common Trip:', df['trip'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_time = int(df['Trip Duration'].sum())
    print('Total Travel Time: {} hours and {} minutes'.format(total_time // 3600, (total_time % 3600) // 60))

    mean_time = int(df['Trip Duration'].mean())
    print('Mean Travel Time: {} minutes and {} seconds'.format(mean_time // 60, mean_time % 60))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

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
    """Displays 5 rows of raw data at a time upon user request."""

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

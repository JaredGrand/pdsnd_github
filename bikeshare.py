import time
import pandas as pd

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
    print('Hello! Let\'s explore some US bikeshare data!\n')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Would you like to explore Chicago, New York City, or Washington? ').lower()
    while city not in ['chicago', 'new york city', 'washington']:
        print("I'm sorry. I don't have that city in my database. Please check the options and spelling and try again.\n")
        city = input('Would you like to explore Chicago, New York City, or Washington? ').lower()
    print('\n')
    # get user input for month (all, january, february, ... , june)

    month = input('Would you like to see data from January, February, March, April, May, June, or all? ').lower()
    while month not in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
        print("I'm sorry. I don't have that month in my database. Please check the options and spelling and try again.\n")
        month = input('Would you like to see data from January, February, March, April, May, June, or all? ').lower()
    print('\n')
    # get user input for day of week (all, monday, tuesday, ... sunday)

    day = input('Would you like to see data from Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or all? ').lower()
    while day not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
        print("I'm sorry. That's not a valid day. Please check the options and spelling and try again.\n")
        day = input('Would you like to see data from Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or all? ').lower()

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
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    df.pop('month')
    df.pop('day_of_week')
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].mode()[0]
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    print('The most popular month is {}'.format(months[popular_month - 1]))

    # display the most common day of week
    df['day'] = df['Start Time'].dt.weekday_name
    popular_day = df['day'].mode()[0]
    print('The most popular day is {}'.format(popular_day))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('The most popular hour is {}'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    df.pop('day')
    df.pop('month')

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_ss = df['Start Station'].mode()[0]
    print('The most commonly used start station is {}'.format(popular_ss))

    # display most commonly used end station
    popular_es = df['End Station'].mode()[0]
    print('The most commonly used end station is {}'.format(popular_es))

    # display most frequent combination of start station and end station trip
    df['Routes'] = df['Start Station'] + ' to ' + df['End Station']
    popular_route = df['Routes'].mode()[0]
    print('The most common route is {}'.format(popular_route))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel = df['Trip Duration'].sum()
    print('The total travel time of all rides is {}'.format(total_travel))

    # display mean travel time
    mean_travel = df['Trip Duration'].mean()
    print('The average travel duration is {}'.format(mean_travel))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_count = {}
    for data in df['User Type']:
        user_count[data] = user_count.get(data, 0) + 1

    for key in user_count:
        print('There are {} {}s.'.format(user_count[key], key.lower()))

    # Display counts of gender
    try:
        gender_count = {}
        for data in df['Gender'].dropna():
            gender_count[data] = gender_count.get(data, 0) + 1

        for key in gender_count:
            print('There are {} {}s'.format(gender_count[key], key.lower()))
    except:
        print('There is no gender data for your selection.')


    # Display earliest, most recent, and most common year of birth
    try:
        earliest = int(df['Birth Year'].min())
        print('The earliest birth year listed is {}'.format(earliest))

        recent = int(df['Birth Year'].max())
        print('The most recent birth year listed is {}'.format(recent))

        most_common = int(df['Birth Year'].mode())
        print('The most common birth year listed is {}'.format(most_common))
    except:
        print('There is no year of birth data for your selection.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """Displays 5 individual trips at a time"""
    ans = input('Would you like to see individual trip data? Enter yes or no? ').lower()
    while ans not in ['yes', 'no']:
        ans = input("I'm sorry, I didn't catch that. Was it a yes or a no? ")
    # Cycle through the index of the datafame and display 5 lines at a time
    i = 0
    while ans == 'yes':
        for num in df.index[i:i+5]:
            print(df.loc[num])
            print('\n')
        ans = input("Would you like to see more? Enter yes or no? ")
        i += 5

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()

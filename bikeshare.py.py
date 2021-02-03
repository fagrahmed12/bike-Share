import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new York City': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

      Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # Ask user specify a city (chicago, new york city, washington). 
    while True:
        city = input("\nWhich city would you like to filter by?\nNew York City.\nChicago.\nWashington\n").strip().lower()
        if city not in ('new york city', 'chicago', 'washington'):
          print("Sorry, I didn't catch that. Try again.")
          continue
        else:
          break

    #   Asks user to specify a month to filter on, or choose all.
    while True:
            month = input("\nWhich month would you like to filter by? \nJanuary \nFebruary \nMarch \nApril \nMay \nJune \nor type 'all' if you do not have any preference?\n").strip().lower()
            if month not in ('january', 'february', 'march', 'april', 'may', 'june', 'all'):
              print("\nThat's invalid choice, please type a valid month name or all.")
              continue
            else:
             break


    # Asks user to specify a day of week, or choose all.
    while True:
          day = input("\nAre you looking for a specific day?\nplease choose one or all of these days: \n(Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or  'all'.)\n").strip().lower()
          if day not in ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all'):
            print("\nThat's invalid choice, please type a valid day name or all.")
            continue
          else:
            break

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
# load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
    # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    
    return df

 








def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    Most_common_month= df['month'].mode()[0]
    print('Most Common Month:', Most_common_month)


    # display the most common day of week
    Most_common_day= df['day_of_week'].mode()[0]
    print('Most Common day of week:', Most_common_day)


    # display the most common start hour
    df['Start_hour'] = df['Start Time'].dt.hour
    Most_common_hour = df['Start_hour'].mode()[0]
    print('Most Common Hour:', Most_common_hour)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)









def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    Most_Common_Start_Station = df['Start Station'].value_counts().idxmax()
    print("The most commonly used start station :", Most_Common_Start_Station)

    # display most commonly used end station
    Most_Common_End_Station = df['End Station'].value_counts().idxmax()
    print("The most commonly used end station :", Most_Common_End_Station)

    # display most frequent combination of start station and end station trip
    Combination_Station = df.groupby(['Start Station', 'End Station']).count()
    print('\nThe Most Commonly used combination of start station and end station trip:', Most_Common_Start_Station, " & ", Most_Common_End_Station)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)










def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    Total_Time=60*60*24
    Total_Travel_Time = df['Trip Duration'].sum()
    print('Total travel time:', Total_Travel_Time/Total_Time, " Days")

    # TO DO: display mean travel time
    Mean_Time=60
    Mean_Travel_Time = df['Trip Duration'].mean()
    print('Mean travel time:', Mean_Travel_Time/Mean_Time, " Minutes")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)







def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #  Display counts of user types
    user_types = df['User Type'].value_counts().to_frame()
    print('User types:\n', user_types)


    # Display counts of gender
    try:    
       gender_count = df['Gender'].value_counts().to_frame()
       print('Bike riders gender:\n' ,gender_count)
    except KeyError:
       print("\nGender Types:\nNo data available for this month.")

    # Display earliest, most recent, and most common year of birth
    try:
       Earliest_Year = df['Birth Year'].min()
       print('\nEarliest Year:', Earliest_Year)
       Most_Recent_Year = df['Birth Year'].max()
       print('\nMost Recent Year:', Most_Recent_Year)
       Most_Common_Year = df['Birth Year'].value_counts().idxmax()
       print('\nMost Common Year:', Most_Common_Year)
    except KeyError:
       print("\n\nSorry, No data available for this month.")


       print("\nThis took %s seconds." % (time.time() - start_time))
       print('-'*40)











def display_raw_data(city):
    """
    The fuction takes the city name from get_filters fuction as input 
    and returns the raw data of that city by chunks of 5 rows.
    Args:
        (str) city - name of the city to return the raw data.
    Returns:
        df - raw data of that city by chunks of 5 rows.
    """
    print('\nRaw data is available to check... \n')

    display_raw = input("you want to have a look on more raw data? Type Yes or No\n").strip().lower()
    
    while display_raw == 'yes':
          try:
          
             for chunk in pd.read_csv(CITY_DATA[city], chunksize=5):
                print(chunk) 
                # repeating the question
                display_raw = input("you want to have a look on more raw data? Type Yes or No\n").strip().lower()
                if display_raw != 'yes':
                    print('Thank You')
                    break
             break
          except KeyboardInterrupt:
            clear()
            print('Thank you.')







def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
if __name__ == '__main__':
      main()

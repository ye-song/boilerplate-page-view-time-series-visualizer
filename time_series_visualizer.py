import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col= ['date'])

# Clean data
#df = df.set_index('date')
df = df.loc[(df['value'] >= df['value'].quantile(0.025)) & 
    (df['value'] <= df['value'].quantile(0.975))]



def draw_line_plot():
    # Draw line plot (using matplotlib)
    
    fig, ax = plt.subplots(figsize=(15,8))
    ax.plot(df, color ='red')
    ax.set(
        xlabel = 'Date',
        ylabel = 'Page Views',
        title  = 'Daily freeCodeCamp Forum Page Views 5/2016-12/2019',
        xlim = ["2016-03-31", "2020-01-31"]
    )
    
    # Define the date format
    date_form = DateFormatter("20%y-%m")
    ax.xaxis.set_major_formatter(date_form)

    # Ensure a major tick for each week using (interval=1) 
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
    

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot

    df_bar = df.copy()
    df_bar.reset_index(inplace = True)
    df_bar['date'] = df_bar['date'].astype('str')
    df_bar[['year', 'month', 'day']] = df_bar.date.str.split('-',expand=True,)
    df_bar = df_bar.groupby(['year','month'], as_index= False)['value'].mean().rename(columns={'value':'ave_daily_views'})
    df_bar = df_bar.sort_values(['year','month'], ascending=True)
    
    df_bar['month'].replace({
        '01': 'January', 
        '02': 'February',
        '03': 'March',
        '04': 'April',
        '05': 'May',
        '06': 'June',
        '07': 'July',
        '08': 'August',
        '09': 'September',
        '10': 'October',
        '11': 'November',
        '12': 'December',
        }, inplace=True)
    
    order = ['January','February','March','April','May','June', 'July', 'August', 'September', 'October', 'November', 'December']

    # Changing colour scheme
    custom_palette = ["red", "orange", "yellow", "green","olive","cyan", "blue", "indigo","purple", "magenta", "violet", "pink"]
   
    # Draw bar plot (using Seaborn)
    
    fig, ax = plt.subplots()
    fig = sns.catplot(
    x = 'year',
    y = 'ave_daily_views',
    kind = 'bar',
    hue = 'month',
    hue_order = order,
    legend_out=False,
    data = df_bar,
    palette = custom_palette
    ).fig
    
    # Changing Seaborn Plot size
    fig.set_size_inches(15, 10)
   
    # Adding axis labels and legend
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.legend(loc = 'upper left', title='Months')
                 
    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    order = ['Jan','Feb','Mar','Apr','May','Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    # Draw box plots (using Seaborn)
    fig, ax = plt.subplots(1,2)
    sns.boxplot(
        ax = ax[0],
        x = 'year', 
        y = 'value', 
        data = df_box
        )
    ax[0].set_title('Year-wise Box Plot (Trend)')
    ax[0].set_xlabel('Year')
    ax[0].set_ylabel('Page Views')
    
    sns.boxplot(
        ax = ax[1],
        x = 'month',
        y ='value',
        data = df_box,
        order = order
    )
    ax[1].set_title('Month-wise Box Plot (Seasonality)')
    ax[1].set_xlabel('Month')
    ax[1].set_ylabel('Page Views')
    
    fig.set_size_inches(20, 8)


    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig


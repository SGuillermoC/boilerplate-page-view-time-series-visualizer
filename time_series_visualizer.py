import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', header=0, index_col='date',parse_dates=True)

# Clean data
df = df = df[(df['value'] > df['value'].quantile(0.025)) &
     (df['value'] < df['value'].quantile(0.975))]


def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(12,6),nrows=1,ncols=1)
    sns.lineplot(df,ax=ax)
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_ylim(auto=True)
    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig
  
def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar["Years"] = df_bar.index.year
    df_bar["Months"] = df_bar.index.month_name()
    df_bar = pd.DataFrame(df_bar.groupby(["Years", "Months"], sort=False)["value"].mean().round().astype(int))
    df_bar = df_bar.reset_index()
    missing_data = {
        "Years": [2016, 2016, 2016, 2016],
        "Months": ['January', 'February', 'March', 'April'],
        "Average Page Views": [0, 0, 0, 0]
    }

    df_bar = pd.concat([pd.DataFrame(missing_data), df_bar])
    # Draw bar plot
    fig, ax = plt.subplots(figsize=(12,6),nrows=1,ncols=1)
    sns.barplot(x=df_bar['Years'],y=df_bar['value'],hue=df_bar['Months'],ax=ax,palette='tab10')
    ax.set_xlabel("Years")
    ax.set_ylabel("Average Page Views")
    ax.set_ylim(auto=True)
    ax.legend(loc='upper left')
    



    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]


    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    df_box['month'] = pd.Categorical(df_box['month'], categories=months, ordered=True)
    df_box.sort_values('month',inplace=True)  


    # Draw box plots (using Seaborn)
    fig, ax = plt.subplots(1,2,figsize=(16,9))

    sns.boxplot(x=df_box['year'],y=df_box['value'],ax=ax[0])
    ax[0].set_title("Year-wise Box Plot (Trend)")
    ax[0].set_xlabel("Year")
    ax[0].set_ylabel("Page Views")
    sns.boxplot(x=df_box['month'],y=df_box['value'],ax=ax[1])
    ax[1].set_title("Month-wise Box Plot (Seasonality)")
    ax[1].set_xlabel("Month")
    ax[1].set_ylabel("Page Views")


    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
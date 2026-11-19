# Task A3 – Design the Analysis and Visualisation

## A3.1 Chart choices
- PM2.5 trend over a month: line chart, because date order and changes over time are visible.
- Station comparison: bar chart of mean PM2.5 per station, because categories are compared directly.
- Temperature versus PM2.5: scatter plot, because it reveals association, clusters and outliers between two numeric variables.
- Hours with the worst air: bar chart of average PM2.5 by hour, ordered by hour; a histogram is appropriate for the distribution of individual PM2.5 readings.

## A3.2 Daily summary table
Group by station and date and calculate minimum, maximum, mean and count of valid PM2.5 readings. SQLite `GROUP BY station_name, reading_date` produces the summary without transferring all raw rows into Python.

SQL aggregation scans the relevant n readings, typically O(n), while keeping database-side working state for groups. A Python loop over all rows is also O(n), but if all rows are fetched and retained it uses O(n) application memory; a streaming dictionary uses O(g) memory for g station/date groups.

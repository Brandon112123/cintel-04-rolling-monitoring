# Continuous Intelligence

This site provides documentation for this project.
Use the navigation to explore module-specific materials.

## How-To Guide

Many instructions are common to all our projects.

See
[⭐ **Workflow: Apply Example**](https://denisecase.github.io/pro-analytics-02/workflow-b-apply-example-project/)
to get these projects running on your machine.

## Project Documentation Pages (docs/)

- **Home** - this documentation landing page
- **Project Instructions** - instructions specific to this module
- **Your Files** - how to copy the example and create your version
- **Glossary** - project terms and concepts

## Additional Resources

- [Suggested Datasets](https://denisecase.github.io/pro-analytics-02/reference/datasets/cintel/)

## Custom Project

### Dataset
I used a weather dataset that records temperature over time. The file I used was `daily_max_temperatures.csv`. Each row shows one date and the temperature for that day. I chose this dataset because it works well with rolling monitoring and lets me apply the same idea from the original project to a different type of data.

### Signals
The main signal I created was a rolling mean for temperature. I used the `Temperature` column and created a new signal called `temperature_rolling_mean`. This helped smooth out the day to day changes and made the bigger trend easier to see.

### Experiments
For my experiment, I changed the project from system metrics to weather data. Instead of tracking requests, errors, and latency, I tracked temperature values. I also used a rolling window of 9 and added a chart so the project would create both a CSV file and a visual output.

### Results
The project ran successfully and created two artifacts. One was a CSV file named `rolling_weather_metrics.csv` and the other was a chart image named `rolling_weather_metrics.png`. The rolling mean made the temperature data look smoother and helped show the overall trend better than the raw daily values.

### Interpretation
This project showed me that rolling monitoring can be used for more than just system performance data. It can also help explain weather patterns over time. The main insight I gained was that rolling averages make noisy data easier to understand and can help people see trends more clearly when looking at large time series datasets.

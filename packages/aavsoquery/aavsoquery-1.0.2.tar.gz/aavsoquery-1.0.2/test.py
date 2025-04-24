from aavsoquery import AAVSODataFetcher, Plotter

fetcher = AAVSODataFetcher(
    star_name='U Scorpii',
    obs_types='all',
    num_results=100,
    pages=10
) #query by star's name (Example: T CrB), ability to fetch by a particular observer by obscode = 'Observer's code'


julian_dates, magnitudes = fetcher.fetch_and_parse_data(include_uncertain=False) # you can exclude uncertain values that begins with <
fetcher.save_to_csv(julian_dates,magnitudes,'yolo.csv')
if len(julian_dates) > 0 and len(magnitudes) > 0: #if data fetched then plot it
    plotter = Plotter(julian_dates, magnitudes)
    plotter.plot_light_curve(interval_hours=1, fit_model=False) #ability to fit a simple gaussian model, also defaults to mean hourly data if more datapoints present
else:
    print("No data available to plot.")
function updateData()
    %update confirmed cases
    block = urlread('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv');
    fid = fopen('confirmed.csv', 'wt');
    fwrite(fid, block);
    fclose(fid);

    %update deaths
    block = urlread('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv');
    fid = fopen('deaths.csv', 'wt');
    fwrite(fid, block);
    fclose(fid);

    %update recovered
    block = urlread('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv');
    fid = fopen('recovered.csv', 'wt');
    fwrite(fid, block);
    fclose(fid);

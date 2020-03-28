block = urlread('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv');
fid = fopen('YourFile.csv', 'wt');
fwrite(fid, block);
fclose(fid);

a(1,:)=fetchConfirmed('Portugal');
a(2,:)=fetchConfirmed('Spain');
a(3,:)=fetchConfirmed('Germany');
a(4,:)=fetchConfirmed('Italy');
a(5,:)=fetchConfirmed('Switzerland');

figure
hold on;
b={}
for k=1:1:5
    b{k}= medfilt1(diff(a(k,:))./a(k,2:length(a)),3);
    [~, aux]=max(b{k});
    b{k}=b{k}(aux:length(b{k}));
    plot(b{k});
    grid on
end

legend('Portugal', 'Spain', 'Germany (ignore)', 'Italy', 'Switzerland');
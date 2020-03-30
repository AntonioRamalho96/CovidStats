function deaths = fetchDeaths(CountryName)
    tbl=readtable('deaths.csv');
    index=find(strcmp(string(tbl{:,2}), CountryName));
    if(length(index) ~=1)
        if(length(index) ==0)
            disp('No matches for that couuntry...');
            deaths={};
        else
            disp('Multiple matches for that country...');
            deaths={};
        end
    else
        deaths = tbl{index,5:end};
    end
end
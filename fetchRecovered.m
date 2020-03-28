function recovered = fetchRecovered(CountryName)
    tbl=readtable('YourFile.csv');
    if(length(index) ~=1)
        if(length(index) ==0)
            disp('No matches for that couuntry...');
            recovered={};
        else
            disp('Multiple matches for that couuntry...');
            recovered={};
        end
    else
        recovered = tbl{index,5:end};
    end
end
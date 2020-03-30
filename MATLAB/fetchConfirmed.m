function confirmedCases = fetchConfirmed(CountryName)
    tbl=readtable('confirmed.csv');
    
    index=find(strcmp((tbl{:,2}), CountryName));
    if(length(index) ~=1)
        if(length(index) ==0)
            disp('No matches for that couuntry...');
            confirmedCases={};
        else
            disp('Multiple matches for that couuntry...');
            confirmedCases={};
        end
    else
        confirmedCases = tbl{index,5:end};
    end
end


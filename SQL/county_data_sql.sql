/* We need to combine information about U.S. counties from multiple different sources. Here's an overview of the 
tables we will work with:
 - povertyrates.csv: This table lists the poverty rate (in percentage) for each U.S. county from 2018-2020
 - unemployment.csv: This table lists the unemployment rate (in percentage) for each U.S. county from 2018-2020
 - county_neighbors.csv: For each U.S. county, this table lists all the counties that are adjacent to it.
 - medicaid.csv: This table lists the year in which each U.S. state expanded their Medicaid program under the Affordable Care Act
 (i.e., it tells us when expanded healthcare to low-income residents became available in each state). Some states have not expanded Medicaid, in which
 case the 'year' column is NULL.


/* SECTION 1: COMBINING POVERTY AND UNEMPLOYMENT RATES FOR EACH COUNTY */

/* 1a: You want a combined dataset that lists the poverty rate and unemployment rate for each U.S. county.
Let's start by doing an INNER JOIN between these tables - join them on their county code and year. Make sure the final
table includes all the columns from both tables, but make sure you don't have any duplicate columns.

HINT: Avoiding duplicate columns is pretty easy if you're using USING(), but if you're using ON with table aliases, you'll
need to specify which table each column is coming from.
*/

#Type query below:
select s1.*, s2.unemployment
from povertyrates as s1 inner join unemployment as s2
on s1.fips = s2.countyfips and s1.year = s2.year;

/*
You'll be using this joined table for the next few problems, so we will save it as a table that we can access in future queries!
Why not just save it as a 'view'? Well, 'views' are primarly designed for just that - VIEWING data. MySQL is VERY SLOW if you start joining views
together - so if you need to save a query result in a way that quickly lets you perform more JOINs later on, a table is a better solution.

Just paste the query you typed above below the following line, then run the script!
You can then reference 'joined' as you would any other table.
*/

CREATE TABLE joined
select s1.*, s2.unemployment
from povertyrates as s1 inner join unemployment as s2
on s1.fips = s2.countyfips and s1.year = s2.year;


/*1b : Let's figured out how many COUNTIES (not rows) we 'lost' by an inner join?
Respond to each question below.
*/

#Number of distinct counties in 'povertyrates' --> RESPONSE: 3194
#Number of distinct counties in 'unemployment' --> RESPONSE: 3221
#Number of distinct counties in inner join --> RESPONSE: 3143

#Type any SQL queries below
select count(distinct fips) from povertyrates;
select count(distinct countyfips) from unemployment;
select  count(distinct fips) from joined;

/* 1c : You should have found that you 'lost' about 50ish counties from the povertyrates table, and about 80ish counties from the 
unemployment table, when doing your inner join.

It might be okay that we lost data on certain counties - but hopefully for the counties we DO have, we'll have all three years of data
(2018, 2019, 2020). Is this true? Count how many rows your joined table has for each county (this will involve a subquery and GROUP BY!), and
sort the result by the number of rows per county, ascending. If we have a 'full' dataset, then ALL counties should have three rows each
(2018, 2019, 2020).
*/

#Type query below:
select fips, count(distinct year) as 'year' from joined group by fips order by year;


#Your query should show a small number of counties with fewer than three years of data.


/* 1d :  Often when working with time series data, it's best to have rows for each year of interest, even if that means having missing data in those rows.
So, it would be best if we had rows for 2018, 2019, and 2020 for ALL counties.

In this case, often the best approach is to use a CROSS JOIN to create all possible combinations of years/counties, then left-join our data
(poverty and unemployment rates) into that new table. And we'll have NULL values for any county/year combinations that we didn't have in the inner join!

Use a CROSS JOIN to create all possible county-year combinations from your inner joined table. You will be cross-joining two subqueries together:
 - A subquery that selects all DISTINCT fips codes AND state abbreviations from your joined table.
 - A subquery that selects all DISTINCT years from your joined table.

The resulting CROSS JOIN will have three columns: fips, state_abbr, and year.

Save this as a new table called 'county_year_combos'
*/

#Type query below (I've given you some syntax to get you started):
select distinct fips, state_abbr from joined;
select distinct year from joined;

select * from (select distinct fips, state_abbr from joined) as joined_1 cross join (select distinct year from joined) as joined_2;


#Copy/paste the query to create a new temporary table:
CREATE TABLE county_year_combos
select * from (select distinct fips, state_abbr from joined) as joined_1 cross join (select distinct year from joined) as joined_2;


/* 1e : Lastly, let's left-join the date from 'joined' (povrate, unemployment) to 'county_year_combos'.
The result will be very similar to 'joined', but it will have rows for all county/year combinations - even if data is missing from them.

A quick hint on how to handle the 'state_abbr' column, which appear in county_year_combos AND joined: You can either include it in USING(), 
or you can simply specify which table it comes from in the SELECT statement. If you don't do either of these, SQL will throw an error because it's 
not sure where to look for this column!

Order the final result by fips, then by year. Save this result as a new table called 'joined_all'.
*/
#?????????????????????????????????????????
#Type query below:
select * from county_year_combos left join joined using(year,fips, state_abbr) order by fips, year;

#Copy/paste query to create new table 'joined_all':
CREATE TABLE joined_all
select * from county_year_combos left join joined using(year,fips, state_abbr) order by fips, year;

select count(*) from joined_all;

#If you want, you can run the code below to see how data is missing for the county/year combinations that didn't exist in 'joined'.
select * from joined_all where unemployment is null;
select * from joined_all where povrate is null;

/* SECTION 2: APPENDING STATE MEDICAID INFORMATION */

/* 2a: One important characteristic economists consider when analyzing county data is whether their state has expanded Medicaid, when is when states
increase their spending on Medicaid (health insurance for low-income residents) and in doing so receive increased federal funding.

If we're tracking the economic health of each county, we may want to know whether each county had Medicaid expanded for each year in our dataset (2018-2020).

To start off, print our all columns from the 'Medicaid' table:
*/

#Type query below:
select * from medicaid;

#Note that this table contains the year in which each state expanded Medicaid - and is NULL for states that haven't expanded yet.


/* 2b: Let's append the column 'medicaid_year' to our 'joined_final' table, using a LEFT JOIN. This will tell us, for each county, the year in which
its STATE expanded Medicaid. You WON'T be joining on 'year' here - just joining on the state that each county is in!
*/

#Type query below:
select joined_all.*, medicaid.medicaid_year from joined_all left join medicaid on medicaid.Abbr = joined_all.state_abbr;



/* 2c : Re-run the same query, but select one more column: year >= medicaid_year.

This is a simple comparison of whether each row's 'year' is greater than or equal to the year in which
that county's state expanded Medicaid; it will be '1' for county/year combinations
where Medicaid has been expanded, and '0' if it hasn't been expanded yet
(it will be NULL for states that haven't expanded Medicaid, but we'll 
discuss how to deal with that later with the CASE function).

Name this new column 'expanded', and save the result as a new table: joined_all_medicaid.
*/

#Type query below:
select joined_all.*, medicaid.medicaid_year, year >= medicaid_year as 'expanded' from joined_all left join medicaid on medicaid.Abbr = joined_all.state_abbr order by expanded;

#Copy/paste query to create new table 'joined_all_medicaid':
CREATE TABLE joined_all_medicaid
select joined_all.*, medicaid.medicaid_year, year >= medicaid_year as 'expanded' from joined_all left join medicaid on medicaid.Abbr = joined_all.state_abbr order by expanded;



/* SECTION 3: APPENDING INFORMATION ABOUT ADJACENT COUNTIES */

/*Lastly, we may want to compare each county's economic characteristics to those of its surrounding counties.
You have a table called 'county_neighbors', which, for each county, lists the counties that are adjacent to it.
*/

/* 3a: In the 'county_neighbors' table, you'll notice that each county is listed as being adjacent to itself.
Let's get rid of these rows so they don't
affect our results. Filter the table to rows where 'fips' does not equal 'adj_fips'.

Save the result as a new table 'county_neighbors_filtered.'
*/

#Type query below
select * from county_neighbors where fips != adj_fips;

#Copy/paste query to create new table 'county_neighbors_filtered':
CREATE TABLE county_neighbors_filtered
select * from county_neighbors where fips != adj_fips;


/* 3b: This last query will be a bit challenging - consider this a 'final test' of how well you've mastered joins in this class!

For each county in 'joined_all_medicaid', we need to add two additional columns: 'avg_adj_povrate' and 'avg_adj_unemployed.'
These columns will show the average poverty and unemployment rates (across 2018-2020) for the counties that are ADJACENT to each county, which could help
us identify which counties have stronger versus weaker economies than the regions they are in.

For the sake of simplicity, we will NOT worry about different years in this query - we will just use each county's
average poverty rate and unemployed rate, which means that the final values in 'avg_adj_povrate' and 'avg_adj_unemployed' won't change between
2018, 2019, and 2020.

There are multiple ways to go about this, but here is what I would suggest:
 - We first need to get the AVERAGE poverty rate and unemployment rate for each county, which you can do with a GROUP BY on 'joined' or 'joined_all'.
 - Append that average employment and poverty rate information (from 'joined' or 'joined all') to the county_neighbors_filtered dataset
   (based on the adj_fips column). Now, for each county, this table will show the counties adjacent to it AND their average poverty rate and unemployment rate.
 - Group county_neighbors_filtered by county ('fips') to get the average 'adjacent-county' poverty and unemployment rates for each county.
 - Lastly, join that grouping result to 'joined_all_medicaid'. Be sure to properly name the new columns!

Since this step will involve multiple joins, you can save the intermediate steps as new tables, OR just use subqueries.
Just be sure to include all your code below so I can follow your process!
*/ 

#Type queries below:
select fips, avg(povrate) as 'avg_pov', avg(unemployment) as 'avg_unem' from joined_all_medicaid group by fips;

create table county_neightbors_data
select * from county_neighbors_filtered 
left join (select fips as 'fips_original', avg(povrate) as 'avg_pov', avg(unemployment) as 'avg_unem' from joined_all_medicaid group by fips) as s1
on county_neighbors_filtered.adj_fips = s1.fips_original;

select fips, avg(avg_pov) as 'avg_adj_pov', avg(avg_unem) as ' avg_adj_unem' from county_neightbors_data group by fips;

select * from joined_all_medicaid 
left join (select fips, avg(avg_pov) as 'avg_adj_pov', avg(avg_unem) as ' avg_adj_unem' from county_neightbors_data group by fips) as s2
using(fips);


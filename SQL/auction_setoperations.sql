/* We just uploaded one table with all four years of charity auction data, for simplicity - but this
exercise will assume that each year's auction data is stored in a separate file. Run the code below to split
this data into four files. */
select * from auctiondata;

create table auction2019
select bidder_id, spend_2019 as 'spend' from auctiondata where spend_2019 is not NULL;

create table auction2020
select bidder_id, spend_2020 as 'spend' from auctiondata where spend_2020 is not NULL; 

create table auction2021
select bidder_id, spend_2021 as 'spend' from auctiondata where spend_2021 is not NULL;

create table auction2022
select bidder_id, spend_2022 as 'spend' from auctiondata where spend_2022 is not NULL;

/* Let's start by comparing the lists of attendees to each other.

Which bidders were new to this year's auction (i.e., only attended in 2022)? */

#ideally would use EXCEPT / MINUS
select bidder_id from auction2022;

#Lets get list of ALL bidders 2019-2021, and compare against them
select bidder_id from auction2021
union
select bidder_id from auction2020
union
select bidder_id from auction2019;

select bidder_id from auction2022 where bidder_id not in 
(select bidder_id from auction2021
union
select bidder_id from auction2020
union
select bidder_id from auction2019);

/* Imagine we want to identify these bidders in the auction2022 table as 'First-time' attendees. Let's use CASE and SELECT to create a new
column auction2022 called 'Status', which will say 'First-time bidder' for first-time attendees and 'Return bidder' for those that have attended the
charity auction before.
*/
select *,
case when bidder_id not in 
(select bidder_id from auction2021
union
select bidder_id from auction2020
union
select bidder_id from auction2019) then 'First-time bidder'
else 'Return bidder' end as 'Status'
from auction2022 order by Status;

# Or you could use
select *,
case when bidder_id in 
(select bidder_id from auction2021
union
select bidder_id from auction2020
union
select bidder_id from auction2019) then 'Return bidder'
else 'First-time budder' end as 'Status'
from auction2022;

/* For each return bidder, we might want to know the most recent auction that they attended (2018, 2019, or 2021). For first-time bidders,
we can just have this column be NULL. Let's add a new column 'last_auction' to auction2022.

For this, think about how we might do this manually. We would scan the list of bidders and first see if they were in the '2021' table. If so,
we'd list 2021 as their most recent auction. Otherwise, we'd move on to the 2020 table. We can do the same thing with a CASE function!
*/
#have to do this in order from 2021 to 2019 from front to back, first to last so you want it to go over the first part and if still not satisfied then go to the next part
select *,
case when bidder_id in (select bidder_id from auction2021) then 2021
when bidder_id in (select bidder_id from auction2020) then 2020
when bidder_id in (select bidder_id from auction2019) then 2019
else Null end as 'last_auction'
from auction2022 order by last_auction;

/* Let's move on from assessing each bidder's history, and move on to combining data across auction years.

When combining data from tables like this, we have two options: A 'wide' format (where each year's spend becomes its own column) and a
'long' format (where each year's spend is its own row). 

Let's create a 'wide' version of this dataset, by using UNION to create a 'master list' of all bidder numbers then left-joining our spending columns to it.
This will give us the same result as 'full joining' all the tables...but MySQL doesn't support full joins!

Order this view by bidder_id.
*/
select * from auction2022;

# to combine in 'wide' format, first need liast of ALL attendees to form first column
select bidder_id, auction2019.spend as 'spend2019', 
auction2020.spend as 'spend2020',
auction2021.spend as 'spend2021',
auction2022.spend as 'spend2022'
from 
(select bidder_id from auction2019
union
select bidder_id from auction2020
union
select bidder_id from auction2021
union
select bidder_id from auction2022
order by bidder_id) as bidders

left join auction2019 using(bidder_id)
left join auction2020 using(bidder_id)
left join auction2021 using(bidder_id)
left join auction2022 using(bidder_id)
;

/* Now, let's 'stack' all four years of data into a long-format dataset. We'll save this as a new view called 'auctionall'.
Before we combine the tables, we will need to add a 'year' column to each table to keep track of which rows came from which table!

Order the results by bidder_id, then year. */
#this is only possible when tables have the same number of columns and same data types.

select *, 2019 as 'year' from auction2019
union
select *, 2020 as 'year' from auction2020
union
select *, 2021 as 'year' from auction2021
union
select *, 2022 as 'year' from auction2022
order by bidder_id, year;


/* Using this auction all view, let's add a column called 'spend_level' which takes on the following values:
 - 'low' for spends less than 300
 - 'medium' for spends between 300 and 700
 - 'high' for spends above 700
*/
create table auction_all
select *, 2019 as 'year' from auction2019
union
select *, 2020 as 'year' from auction2020
union
select *, 2021 as 'year' from auction2021
union
select *, 2022 as 'year' from auction2022
order by bidder_id, year;

select *, 
case when spend < 200 then 'low'
when spend >= 300 and spend <= 700 then 'medium' #spend between 300 and 700
else 'high' end as 'spend_level' #else will catch nulls but in this data we don't have any nulls
from auction_all;



/* Last query! Remember our 'status' column earlier where we wanted to see if someone was a first-time or returning bidder.
Let's add that column to 'auctionall'. It will be more complicated because, for each year, we need to check all prior years'
bidder numbers - but we can do this with a case function! */

select *,
case when year = 2022 and bidder_id in (select bidder_id from auction_all where year < 2022) then 'Return'
when year = 2021 and bidder_id in (select bidder_id from auction_all where year < 2021) then 'Return'
when year = 2020 and bidder_id in (select bidder_id from auction_all where year < 2020) then 'Return'
when year = 2019 and bidder_id in (select bidder_id from auction_all where year < 2019) then 'Return'
else 'first-time' end as 'Status'
from auction_all;

#subquery for all auctions before 2020
#(select bidder_id from auctionall where year < 2020)

#subquery for all auctions before 2021
#(select bidder_id from auctionall where year < 2021)

#subquery for all auctions before 2022
#(select bidder_id from auctionall where year < 2022)




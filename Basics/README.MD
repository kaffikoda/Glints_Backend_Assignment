**Methods of making the api calls:-**
-

First of all fill the required detail in the **.env** file as instructed. The packages used for running these scripts are mentioned in the **requirements.txt** file, install them in your environment before running running the scripts.

- For searching the names of restaurants on a particular datetime you need to enter the url as
**restaurants?datetime=dd-mm-yyyy H:M"**. Thing to remember is that there should be a space between the date and time.

- For getting the top **y** restaurants which has greater than or less than **x** dishes in a given price range.
There are two types of urls that can written to get the results. First one is:- **restaurants?top=y&greater_than=x&price_range=lower_price-higher_price**. 
In place of y put the value y, i.e number of top restaurants you want to see. In place of x put the value x, i.e minimum number of dishes required to be in the given
price range. Through this url we get top y restaurants which have more than x dishes in the given price range. Second type of url is:-
**restaurants?top=y&lesser_than=x&price_range=lower_price-higher_price**. In place of y put the value y, i.e number of top restaurants you want to see. In place of x put the value x, i.e at most number of dishes required to be in the given.
Through this url we get top y restaurants which have less than x dishes in the given price range. Display of top y restaurants is done in descending order of the cash balance.

- For getting relevant restaurants according to the search term you need to write the url request as:- **relevant_restaurants?name=search_term**.
In place of search term you have to write your search term. First of all those restaurants are fetched which has the search term present in their name, then their ordering
is done on the basis of **edit distance** i.e how much minimum operations (insertion of character or deletion of character or replacement of character) is required to
convert the search term to the restaurants name. Lesser the edit distance more relevant it is to the search term.

- For getting relevant dishes according to the search term you need to write the url request as:- **relevant_dishes?name=search_term**.
In place of search term you have to write your search term. First of all those dishes are fetched which has the search term present in their name, then their ordering
is done on the basis of **edit distance** i.e how much minimum operations (insertion of character or deletion of character or replacement of character) is required to
convert the search term to the dish's name. Lesser the edit distance more relevant it is to the search term.

- For doing an atomic transaction the url should be in the **place_order?user_id=X&dish_name=Y&restaurant_name=Z**. In place of X enter the valid user id which can be seen in the **customer_id** column of
**customer_details** table. In place of Y enter the dish name you are looking for and in place of Z enter the restaurant name from where you want to order. If invalid user_id is entered, meaning
the user details is not there in the **customer_details** table then transaction will not take place. If the the dish is not present in that particular restaurant then transaction will not take place. Make
sure that the dish you are looking for is present in the restaurant from where you want to order and the person's from whose user_id order is going to be placed
should have sufficient cash balance to place the order, meaning cash balance should be greater than equal to the cost of the dish. If these condition satisfies then an atomic transaction will
take place.

 

 
 
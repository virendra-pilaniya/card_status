Problem Statement - 

Need an internal API that would return the status of a user’s card. We need a service that would combine the data from our partner companies and return the current status of a card when queried for by a team mate.

Solution - 

Created two endpoints - (get_card_status/, load_card_data/)
load_card_data - By hitting this api, we are iterating through all the CSV files and storing the data in the Database, with the help of Django ORM.
I have created two models - (Card, CardEvent) which gonna store the details.
Now with the help of get_card_status, we can get the staus of a card as of now.

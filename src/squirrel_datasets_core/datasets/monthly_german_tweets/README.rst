.. list-table::
    :header-rows: 1

    *   - pretty_name
        - Monthly German Tweets
    *   - annotations_creators
        -
    *   - language_creators
        -
    *   - languages
        - 
    *   - licenses
        - 
    *   - multilinguality
        -
    *   - size_categories
        - 10M<n100M
    *   - source_datasets
        -
    *   - task_categories
        - 
    *   - task_ids
        -
    *   - paperswithcode_id
        -
    

Dataset Description
###################

* Homepage: `Monthly German Tweets <https://zenodo.org/record/3633935#.Yh48C1vMJk2>`_
* Licenses: `Attribution 4.0 International <https://creativecommons.org/licenses/by/4.0/legalcode>`_

Dataset Summary
***************

Monthly records for Tweets in German.

Download and prepare data
*************************

Download the data directly from `zenodo <https://zenodo.org/record/3633935#.Yh48e1vMJk3>`_, extract one or multiple zip files of several months. 
Replace {PATH_TO_DATA} below with the location of a folder containing all gz files for the selected months. Use the following code to load the data:

.. code-block:: python

    from squirrel_datasets_core.datasets.monthly_german_tweets import MonthlyGermanTweetsDriver
    iter = MonthlyGermanTweetsDriver("{PATH_TO_DATA}").get_iter()


Dataset Structure
###################

Data Instances
**************

Two samples from the dataset are provided below:

.. code-block::

    {
        'type': 'retweet', 
        'id': '1113903993632231424', 
        'user': '596726209', 
        'created_at': '2019-04-04T20:39:42+00:00', 
        'recorded_at': '2019-04-04T20:39:47.201235+00:00', 
        'source': '<a href="http://twitter.com/download/android" rel="nofollow">Twitter for Android</a>', 
        'retweets': 0, 
        'favourites': 0, 
        'lang': 'de', 
        'hashtags': [], 
        'urls': [], 
        'mentions': ['glsbank'], 
        'mentioned_ids': ['14941624'], 
        'refers_to': '1113486158938476544'
    }

    {
        'type': 'reply', 
        'id': '1115215310540496898', 
        'user': '2970777982', 
        'created_at': '2019-04-08T11:30:24+00:00', 
        'recorded_at': '2019-04-08T11:30:29.550608+00:00', 
        'source': '<a href="http://twitter.com" rel="nofollow">Twitter Web Client</a>', 
        'retweets': 0, 
        'favourites': 0, 
        'lang': 'de', 
        'hashtags': [], 
        'urls': [], 
        'mentions': ['greenpeace_de', 'AndiScheuer', 'AufbruchFahrrad', 'wegeheld', 'RegineGuenther', 'Mobility_TSP', 'VCDeV', 'FahrradClub', 'staedtetag', 'womeninmobility', 'radentscheid'], 
        'mentioned_ids': ['8447362', '50315139', '984739159792410625', '2377228105', '335887533', '499786104', '285054185', '33557760', '1229615683', '3307970055', '4438154961'], 
        'text': '@greenpeace_de @AndiScheuer @AufbruchFahrrad @wegeheld @RegineGuenther @Mobility_TSP @VCDeV @FahrradClub @staedtetag @womeninmobility @radentscheid AN ALLE: Ein "E" hinter der Zahl auf dem Kennzeichen steht für Elektro!', 
        'refers_to': '1115188095761174529'}
    }

Dataset Schema
**************

- `text`: Contains the text of the tweet. Not included for all types (i.e. retweets).

Data Splits
***********

+---------------------+------------+
|   name              |            |
+---------------------+------------+
|german-tweets        |>5M p month |
+---------------------+------------+

.. list-table::
    :header-rows: 1
    
    *   - Attribute
        - Value
    *   - pretty_name
        - Adult income
    *   - annotations_creators
        -
    *   - language_creators
        -
    *   - languages
        - 
    *   - licenses
        - unknown
    *   - multilinguality
        -
    *   - size_categories
        - 10k<n<100k
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

* Paper: `Scaling Up the Accuracy of Naive-Bayes Classifiers: a Decision-Tree Hybrid <http://robotics.stanford.edu/~ronnyk/nbtree.pdf>`_
* Licenses: Unknown

Dataset Summary
***************

Tabular data containing Adult housing prices from 1996 originated by the US census bureau. Also see this `description <http://www.cs.toronto.edu/~delve/data/adult/adultDetail.html>`_

Download and prepare data
*************************

The dataset can be loaded directly via the squirrel Catalog API. 
Make sure that squirrel-dataset-core is installed via pip, which will register this dataset.
Use the following code to load the data:

.. code-block:: python

    from squirrel.catalog import Catalog
    plugin_catalog = Catalog.from_plugins()
    it = plugin_catalog["adult_income"].get_driver().get_iter(split="train")

Dataset Structure
###################

Data Instances
**************

A sample from the training set is provided below:

.. code-block::

    {
        'age': 1,
        'workclass': 'Private',
        'fnlwgt': 45781,
        'education': 'Masters',
        'education-num': 14,
        'marital-status': 'Never-married',
        'occupation': 'Prof-specialty',
        'relationship': 'Not-in-family',
        'race': 'White',
        'sex': 'Female',
        'capitalgain': 4,
        'capitalloss': 0,
        'hoursperweek': 3,
        'native-country': 'United-States',
        'class': '>50K'
    }

Dataset Schema
**************

Contains 16 features. 

Data Splits
***********

+------------+------+
|   name     |      |
+------------+------+
|Adult income|48,842|
+------------+------+
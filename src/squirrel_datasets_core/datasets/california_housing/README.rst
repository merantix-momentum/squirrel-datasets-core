.. list-table::
    :header-rows: 1
    
    *   - Attribute
        - Value
    *   - pretty_name
        - California Housing
    *   - annotations_creators
        -
    *   - language_creators
        -
    *   - languages
        - 
    *   - licenses
        - CC0
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

* Paper: `Sparse spatial autoregressions <https://www.sciencedirect.com/science/article/abs/pii/S016771529600140X>`_
* Licenses: `CC0 <https://creativecommons.org/publicdomain/zero/1.0/>`_
 
Dataset Summary
***************

Tabular data containing California housing prices from the 1990 census. Also see this `Kaggle description <https://www.kaggle.com/datasets/camnugent/california-housing-prices>`_

Download and prepare data
*************************

The dataset can be loaded directly via the squirrel Catalog API. 
Make sure that squirrel-dataset-core is installed via pip, which will register this dataset.
Use the following code to load the data:

.. code-block:: python

    from squirrel.catalog import Catalog

    plugin_catalog = Catalog.from_plugins()
    it = plugin_catalog["california_housing"].get_driver().get_iter()

Dataset Structure
###################

Data Instances
**************

A sample from the training set is provided below:

.. code-block::

    {
        'longitude': '-122.300000',
        'latitude': 37.81,
        'housingMedianAge': 52.0,
        'totalRooms': 1224.0,
        'totalBedrooms': 237.0,
        'population': 521.0,
        'households': 159.0,
        'medianIncome': 1.191,
        'medianHouseValue': 76100.0
    }

Dataset Schema
**************

All features are continuous floats
 
Data Splits
***********

+------------------+------+
|   name           |      |
+------------------+------+
|California housing|20,640|
+------------------+------+
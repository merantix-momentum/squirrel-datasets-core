.. list-table::
    :header-rows: 1
    
    *   - Attribute
        - Value
    *   - pretty_name
        - Automated Deep Learning
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

* Paper: `Analysis of the AutoML Challenge Series 2015–2018 <https://link.springer.com/chapter/10.1007/978-3-030-05318-5_10>`_
* Relevant Links:
    - `Data <https://automl.chalearn.org/data>`_
    - `Challenge webpage <https://automl.chalearn.org/home>`_
* Licenses: Unknown

Dataset Summary
***************

Tabular data containing float elements.

Download and prepare data
*************************

The dataset can be loaded directly via the squirrel Catalog API. 
Make sure that squirrel-dataset-core is installed via pip, which will register this dataset.
Use the following code to load the data:

.. code-block:: python

    from squirrel.catalog import Catalog
    plugin_catalog = Catalog.from_plugins()
    it = plugin_catalog["helena"].get_driver().get_iter(split="train")

.. code-block:: python

    from squirrel.catalog import Catalog
    plugin_catalog = Catalog.from_plugins()
    it = plugin_catalog["jannis"].get_driver().get_iter(split="train")

Dataset Structure
###################

Data Instances
**************

A sample from the Helena training set is provided below:

.. code-block::

    {
        'features': [
            0.200384,
            0.660417,
            0.4375,
            0.38136,
            0.531051,
            0.543844,
            0.378399,
            0.025277,
            0.306467,
            123.23,
            105.248,
            95.8235,
            51.416,
            50.8848,
            47.8058,
            0.735954,
            0.876967,
            1.2111,
            69.2957,
            3.7954,
            5.33528,
            12.7654,
            2.49029,
            4.30002,
            0.590964,
            -0.0334237,
            0.394317
        ],
        'class': 9
    }

Dataset Schema
**************

All features are continuous floats. There are in total 100 classes to predict. Test and validation data do not contain class labels

Data Splits
***********

.. list-table::
    :header-rows: 1

    *   - name
        - samples
    *   - Helena train
        - 65,196
    *   - Helena test
        - 18,628
    *   - Helena valid
        - 9,314
    *   - Jannis train
        - 83,733
    *   - Jannis test
        - 9,851
    *   - Jannis valid
        - 4,926
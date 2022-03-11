.. list-table::
    :header-rows: 1

    *   - pretty_name
        - Conceptual Captions
    *   - annotations_creators
        -
    *   - language_creators
        -
    *   - languages
        - 
    *   - licenses
        - custom
    *   - multilinguality
        -
    *   - size_categories
        - 10M<n<100M
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

* Paper: `Conceptual Captions Paper <https://arxiv.org/abs/2102.08981>`_
* Licenses: `Attribution <https://github.com/google-research-datasets/conceptual-12m/blob/main/LICENSE>`_
 
Dataset Summary
***************

Pairs of images and captions.

Download and prepare data
*************************

The dataset can be loaded directly via the squirrel Catalog API. 
Make sure that squirrel-dataset-core is installed via pip, which will register this dataset.
Use the following code to load the data:

.. code-block:: python

    from squirrel.catalog import Catalog

    plugin_catalog = Catalog.from_plugins()
    it = plugin_catalog["conceptual-captions-12m"].get_driver().get_iter()

Dataset Structure
###################

Data Instances
**************

A sample from the training set is provided below:

.. code-block::

    {
        'url': 'https://i.pinimg.com...', 
        'error': False, 
        'image': array(...)
        'caption': 'Peterbilt 359 custom built show me how to find this Large Cars kits...'
    }

Dataset Schema
**************

- `error`: True if there was an http error accessing the data.
 
Data Splits
***********

+--------------+-----+
|   name       |     |
+--------------+-----+
|CC12M         |12M  |
+--------------+-----+

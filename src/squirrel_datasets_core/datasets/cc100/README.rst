.. list-table::
    :header-rows: 1

    *   - pretty_name
        - CC 100
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
        - 
    *   - source_datasets
        -
    *   - task_categories
        - 
    *   - task_ids
        -
    *   - paperswithcode_id
        - cc100
    

Dataset Description
###################

* Homepage: `CC 100 <https://data.statmt.org/cc-100/>`_
 
Dataset Summary
***************

Raw text data for 100+ different languages.

Download and prepare data
*************************

The dataset can be loaded directly via the squirrel Catalog API. 
Make sure that squirrel-dataset-core is installed via pip, which will register this dataset.
Visit the homepage `<https://data.statmt.org/cc-100/>`_ for all the available languages.
Use the following code to load the data:

.. code-block:: python

    from squirrel.catalog import Catalog
    plugin_catalog = Catalog.from_plugins()

    it_af = plugin_catalog["cc100"].get_driver().select("gd").get_iter()

Dataset Structure
###################

Data Instances
**************

A sample from the training set is provided below:

.. code-block::

    {
        'text': 'Èireannaich air an sguad ainmeachadh...', 
    }

Dataset Schema
**************

- `text`: Contains the raw text without annotations.
 
Data Splits
***********

Visit the `homepage <https://data.statmt.org/cc-100/>`_ for a list of all splits.
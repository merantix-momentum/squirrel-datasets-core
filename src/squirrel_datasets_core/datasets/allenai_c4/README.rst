.. list-table::
    :header-rows: 1

    *   - pretty_name
        - Allenai C4
    *   - annotations_creators
        -
    *   - language_creators
        -
    *   - languages
        - 
    *   - licenses
        - ODC-By
    *   - multilinguality
        - 
    *   - size_categories
        - 1B<n<10B
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

* Homepage: `Allenai C4 <https://github.com/allenai/allennlp/discussions/5056>`_
* Licenses: `Open Data Commons Attribution License (ODC-By) v1.0 <https://opendatacommons.org/licenses/by/1-0/>`_
 
Dataset Summary
***************

Raw text data in 101 different languages.

Download and prepare data
*************************

The dataset can be loaded directly via the squirrel Catalog API. 
Make sure that squirrel-dataset-core is installed via pip, which will register this dataset.
Visit the TensorFlow site `<https://www.tensorflow.org/datasets/catalog/c4>`_ for all the available languages.
Use the following code to load the data:

.. code-block:: python

    from squirrel.catalog import Catalog
    plugin_catalog = Catalog.from_plugins()

    # For each of the 101 languages there is a train and valid split
    it_af_val = plugin_catalog["c4"].get_driver().select("af", "valid").get_iter()

Dataset Structure
###################

Data Instances
**************

A sample from the training set is provided below:

.. code-block::

    {
        'text': 'Stehe vielleicht kurz vorm Wechsel, ein paar Frage...', 
        'timestamp': '2018-12-16T09:17:27Z', 
        'url': 'http://www.pokertips.org/forums/showthread.php?t=49769&page=3'
    }

Dataset Schema
**************

- `text`: Contains the raw text without annotations.
 
Data Splits
***********

Visit the tensorflow site `<https://www.tensorflow.org/datasets/catalog/c4>`_ for a list of all splits and number of examples.
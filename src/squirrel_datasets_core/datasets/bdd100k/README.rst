.. list-table::
    :header-rows: 1

    *   - pretty_name
        - BDD100K Dataset
    *   - annotations_creators
        -
    *   - language_creators
        -
    *   - languages
        -
    *   - licenses
        - BSD 3-Clause License
    *   - multilinguality
        -
    *   - size_categories
        - 1K<n<10K
    *   - source_datasets
        -
    *   - task_categories
        - semantic-segmentation
    *   - task_ids
        -
    *   - paperswithcode_id
        - bdd100k


Dataset Description
###################

* Homepage: `Berkeley Deep Drive Semantic Segmentation (BDD100K) dataset <https://www.bdd100k.com/>`_
* Licenses: `BSD 3-Clause License <https://doc.bdd100k.com/license.html#license>`_

Dataset Summary
***************

BDD100K:  A Diverse Driving Dataset for Heterogeneous Multitask Learning

Download and prepare data
*************************

Login or register at this `website <https://bdd-data.berkeley.edu/>`_, download the `segmentation` and `10K Images` parts and extract them.
Make sure to copy both the `images` folder as well as the `labels` folder in the same directory and use that below.
Replace {PATH_TO_DATA} below with the location of the BDD100k folder. Use the following code to load it:

.. code-block:: python

    from squirrel_datasets_core.datasets.bdd100k import BDD100KDriver
    iter_train = BDD100KDriver("{PATH_TO_DATA}").get_iter("train")
    iter_val = BDD100KDriver("{PATH_TO_DATA}").get_iter("val")
    iter_test = BDD100KDriver("{PATH_TO_DATA}").get_iter("test")


Dataset Structure
###################

Data Instances
**************

A sample from the training set is provided below:

.. code-block::

    {
        'image_url': '{PATH_TO_DATA}/train/0016E5_07920.png',
        'label_url': '{PATH_TO_DATA}/trainannot/0016E5_07920.png',
        'split': 'train'
        'image': array(...)
        'label': array(...)
    }


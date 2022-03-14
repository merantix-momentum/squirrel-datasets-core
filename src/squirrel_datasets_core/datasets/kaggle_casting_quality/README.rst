.. list-table::
    :header-rows: 1

    *   - pretty_name
        - Kaggle Casting Quality
    *   - annotations_creators
        -
    *   - language_creators
        -
    *   - languages
        - []
    *   - licenses
        - CC BY-NC-ND 4.0
    *   - multilinguality
        -
    *   - size_categories
        - 1K<n<10K
    *   - source_datasets
        -
    *   - task_categories
        - image-classification
    *   - task_ids
        -
    *   - paperswithcode_id
        -
    
Dataset Description
###################

* Homepage: `Casting Product Quality <https://www.kaggle.com/ravirajsinh45/real-life-industrial-dataset-of-casting-product>`_
* Licenses: `Attribution-NonCommercial-NoDerivatives 4.0 International <https://creativecommons.org/licenses/by-nc-nd/4.0/>`_
 
Dataset Summary
***************

Dataset for the automatic identification of casting defects.

Download and prepare data
*************************

Download the data directly from `Kaggle <https://www.kaggle.com/ravirajsinh45/real-life-industrial-dataset-of-casting-product>`_ and extract it. Replace {PATH_TO_DATA} below with the location of the data. Use the following code to load it:

.. code-block:: python

    from squirrel_datasets_core.datasets.kaggle_casting_quality.driver \ 
        import RawKaggleCastingQualityDriver
    iter_train = RawKaggleCastingQualityDriver("{PATH_TO_DATA}/casting_data/casting_data")\
        .get_iter("train")
    iter_test = RawKaggleCastingQualityDriver("{PATH_TO_DATA}/casting_data/casting_data")\
        .get_iter("test")


Dataset Structure
###################

Data Instances
**************

A sample from the training set is provided below:

.. code-block::

    {
        'url': '{PATH_TO_DATA}/casting_data/casting_data/test/ok_front/cast_ok_0_9996.jpeg', 
        'label': 1, 
        'image': array(...)
    }

Dataset Schema
**************

- `img`: A numpy array containing the 300x300 RGB image.
- `label`: `1` for ok front and `0` for defect front.
 
Data Splits
***********

+--------------+-----+----+
|   name       |train|test|
+--------------+-----+----+
|kaggle-casting|6633 |715 | 
+--------------+-----+----+

..
    Dataset Creation
    ################

    Curation Rationale
    ******************

    [More Information Needed]
    
    Source Data
    ***********

    Initial Data Collection and Normalization

    [More Information Needed]
    
    Annotations
    ***********

    Annotation process
    
    [More Information Needed]
    
    Who are the annotators?
    
    [More Information Needed]
    
    Personal and Sensitive Information
    **********************************

    [More Information Needed]
    
    Considerations for Using the Data
    ####################################

    Social Impact of Dataset
    **********************************

    [More Information Needed]
    
    Discussion of Biases
    **********************************

    [More Information Needed]
    
    Other Known Limitations
    **********************************

    [More Information Needed]
    
    Citation Information
    **********************************

    [More Information Needed]

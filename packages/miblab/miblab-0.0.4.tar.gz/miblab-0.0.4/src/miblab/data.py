import os

try:
    import requests
    import_error = False
except:
    import_error = True

# Zenodo DOI of the repository
# DOIs need to be updated when new versions are created
DOI = {
    'MRR': "15285017",      # v0.0.3
    'TRISTAN': "15285027"   # v0.0.1
}

# miblab datasets
DATASETS = {
    'KRUK.dmr.zip': {'doi': DOI['MRR']},
    'tristan_humans_healthy_ciclosporin.dmr.zip': {'doi': DOI['MRR']},
    'tristan_humans_healthy_controls_leeds.dmr.zip': {'doi': DOI['MRR']},
    'tristan_humans_healthy_controls_sheffield.dmr.zip': {'doi': DOI['MRR']},
    'tristan_humans_healthy_metformin.dmr.zip': {'doi': DOI['MRR']},
    'tristan_humans_healthy_rifampicin.dmr.zip': {'doi': DOI['MRR']},
    'tristan_humans_patients_rifampicin.dmr.zip': {'doi': DOI['MRR']},
    'tristan_rats_healthy_multiple_dosing.dmr.zip': {'doi': DOI['MRR']},
    'tristan_rats_healthy_reproducibility.dmr.zip': {'doi': DOI['MRR']},
    'tristan_rats_healthy_six_drugs.dmr.zip': {'doi': DOI['MRR']},
}


def zenodo_fetch(dataset:str, folder:str, doi:str=None, filename:str=None):
    """Download a dataset from Zenodo

    Args:
        dataset (str): Name of the dataset
        folder (str): Local folder where the result is to be saved
        doi (str, optional): Digital object identifier (DOI) of the 
          Zenodo repository where the dataset is uploaded. If this 
          is not provided, the function will look for the dataset in
          miblab's own Zenodo repositories.
        filename (str, optional): Filename of the downloaded dataset. 
          If this is not provided, then *dataset* is used as filename.

    Raises:
        NotImplementedError: If miblab is not installed with the data
          option
        requests.exceptions.ConnectionError: If the connection to 
          Zenodo cannot be made.

    Returns:
        str: Full path to the downloaded datafile.
    """
    if import_error:
        raise NotImplementedError(
            'Please install miblab as pip install miblab[data]'
            'to use this function.'
        )
    
    # Get DOI
    if doi is None:
        if dataset in DATASETS:
            doi = DATASETS[dataset]['doi']
        else:
            raise ValueError(
                f"{dataset} does not exist in one of the miblab "
                f"repositories on Zenodo. If you want to fetch " 
                f"a dataset in an external Zenodo repository, please "
                f"provide the doi of the repository."
            )
    
    # Dataset download link
    file_url = "https://zenodo.org/records/" + doi + "/files/" + dataset

    # Make the request and check for connection error
    try:
        file_response = requests.get(file_url) 
    except requests.exceptions.ConnectionError as err:
        raise requests.exceptions.ConnectionError(
            f"\n\n"
            f"A connection error occurred trying to download {dataset} "
            f"from Zenodo. This usually happens if you are offline."
            f"The detailed error message is here: {err}"
        ) 
    
    # Check for other errors
    file_response.raise_for_status()

    # Create the folder if needed
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Save the file locally 
    if filename is None:
        file = os.path.join(folder, dataset)
    else:
        file = os.path.join(folder, filename)

    if os.path.exists(filename):
        raise ValueError(
            f"Cannot write to {filename}. The file already exists. "
            f"Please provide another filename or folder."
        )
        
    with open(file, 'wb') as f:
        f.write(file_response.content)

    return file
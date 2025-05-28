# Procyclingstats Photoquiz

This project automates playing the Photoquiz game on [ProCyclingStats](https://www.procyclingstats.com/quiz.php?s=photo-quiz) by identifying cyclists from their photos. 

## Prerequisites

- Python 3.8+
- `pip`
- Internet access (for crawling and downloading models)
- Compatible OS with [InsightFace](https://github.com/deepinsight/insightface) and OpenCV-Python

## Virtual Environment Setup

To avoid conflicts with other Python projects, it's recommended to use a virtual environment. You can create and activate a virtual environment using the following commands:

```bash
python3 -m venv venv-photoquiz
source venv-photoquiz/bin/activate
pip install -U pip
pip install -r requirements.txt
```

## Crawling Photos
To crawl photos from ProCyclingStats, run the following command:

```bash
python3 source/mugshot_crawler.py
```

This will create a folder containing all the mugshots of cyclists in the `data/mugshots` directory.

You then need to process these images to create a dataset before training the model. This can be done using the `file_prepreprocessing.py`script:

```bash
python3 source/file_preprocessing.py
```

## Creating the embeddings

In this project, we use the [InsightFace](https://github.com/deepinsight/insightface) library which provides pre-trained models for face detection and recognition. To create embeddings for the mugshots, run:

```bash
python3 source/embeddings.py
```

This will generate embeddings for all the mugshots and save them in the `cyclist_embeddings.npy` file in the data folder.

## Using the Model

To use the model for identifying cyclists from photos, you can run the `photoquiz.py` script. This script will load the embeddings and allow you to play the Photoquiz game by identifying cyclists from their photos.

For that you need to specify to Open-CV where to look for cyclists, I recommend to use only a part of your screen, this can be tuned in the `photoquiz.py` script. The script will automatically detect cyclists and write their names in the quiz. Be sure to click the quiz box in the 2 seconds after pressing `enter` in the terminal, otherwise it will press the names into thin air.

```bash
python3 source/photoquiz.py
```

## Other usage

The script can also be used outside the quiz to identify cyclists from photos.
# Spheroid 3D nucleus segmentation library written in Python

3D Spheroid nucleus segmentation software written in Python. You can easily run and get the volume, label, centroid of the nucleus in the spheroid and many more.

# How to use

What you need is

- Python Environment (Python 3.9.0 or higher)
- 3D image of a spheroid (usually .tif)

## Install

1. Install Python 3.9.0 or higher
2. Clone this repository
3. In the directory, run the following command to install required dependencies

```
pip3 install -r requirements.txt
```

## Set settings.json

see `settings_example.json`

1. You need to set at least these properties to run the segmentation

- `"img_path": ".../spheroid.tif"`, Input 3D image, make sure it is single-channel 3D nuclei image (.tif).
- `"output_dir": ".../output"`, Output directory to save the segmentation results.

2. After you set the values, rename `settings_example.json` to `settings.json`.

## Run

In the directory, run

```
python3 main.py
```

## See the Result

Generated files are like these.

<img width="605" alt="Screen Shot 2023-04-03 at 11 25 51" src="https://user-images.githubusercontent.com/39676181/229397675-2ba47320-c272-4a66-9f98-ff7c95e73581.png">

You can see the results in your output_dir. It contains `.pkl` file for later your analysis. The `.pkl` file can be loaded using Python pickle library.
It contains properties that you set in the `settings.json` for each nucleus segmented in the image. Also, the `settings.json` is saved to check what parameters you used in the analysis. `.npy` file is a segmented 3D image in `numpy` format, each nucleus region is annotated as different integers. The `.csv` file is not needed if you use `.pkl` file, as it is more handy for Python. But in case you don't use Python for post processing, you can use `.csv`.

```json
  "properties": [
    "area",
    "centroid",
    "axis_major_length",
    "axis_minor_length",
    "image",
    "inertia_tensor_eigvals",
    "moments_central"
  ],
```

For example, by using `pandas.read_pickle()`, you can get this segmentation results.

<img width="1174" alt="Screen Shot 2023-04-03 at 11 21 50" src="https://user-images.githubusercontent.com/39676181/229397269-ef6e4ed7-7ff5-4e25-b20e-c5ac62b39748.png">

## Debug

In `settings.json`, you can set `debug: true` and you can visualize the segmentation process step by step like below using `napari` library. For more info, please have a look at https://napari.org/stable/.


<img width="1680" alt="Screen Shot 2023-04-03 at 11 31 05" src="https://user-images.githubusercontent.com/39676181/229398400-92bf10c6-c63a-4970-be05-571d76603531.png">


## Troubleshooting

### not working when debug is true

run

```
brew install PyQt
```

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

You can see the results in your output_dir. It contains `.pkl` file for later your analysis. The `.pkl` file can be loaded using Python pickle library.
It contains properties that you set in the `settings.json` for each nucleus segmented in the image.

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



## Troubleshooting

### not working when debug is true

run

```
brew install PyQt
```

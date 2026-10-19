# fractal_render

## Project structure

```text
fractal_render/
├── main.py                 # Main file to run
├── modules/
│   ├── api.py              # OpenAPI HTTP endpoint
│   └── processor.py        # Shared image-processing function
├── tests/
│   └── test_processor.py   # Local processing tests
├── input_images/           # Source images; sample.png is the tracked example
└── output/
    ├── images/             # Rendered image files
    └── gifs/               # Rendered GIF files
```

Run `py -m pip install -r requirements.txt` to install image conversion and API
dependencies. For local processing, put images in `input_images/` and run
`py main.py`. Choose an input file and PNG, JPEG, or GIF as the output format;
results are saved under `output/images/` or `output/gifs/`. The algorithm is
currently a pass-through placeholder. GIF animation is retained when saving
as GIF; conversion from an animated GIF to PNG or JPEG uses its first frame.

To serve the same processor over HTTP, run `py main.py --serve`. The interactive
OpenAPI documentation is available at
`http://127.0.0.1:8000/docs`, and `POST /process` accepts an image upload.

Run tests with `py -m unittest discover -s tests`.
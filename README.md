# fractal_render

## Project structure

```text
fractal_render/
├── main.py                 # Main file to run
├── modules/
│   └── api_client.py       # JSON API requests
├── tests/
│   └── test_api_client.py  # API client tests
├── input_images/           # Source images; sample.png is the tracked example
└── output/
    ├── images/             # Rendered image files
    └── gifs/               # Rendered GIF files
```

Run the project with `python main.py`. To make a JSON API request, pass a URL
with `python main.py --api-url https://example.com/data`.

Run tests with `python -m unittest discover -s tests`.
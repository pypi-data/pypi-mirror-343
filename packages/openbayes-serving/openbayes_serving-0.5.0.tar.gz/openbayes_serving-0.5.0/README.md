# Python OpenBayes Serving

## Debugger Web UI

Start a web server:

```bash
python exception.py
```

Open a new shell session. Fire a request with error:

```bash
curl -XPOST localhost:25252
```

Compare with Werkzeug Debugger:

```bash
python werkzeug_demo.py
```

Then open `http://localhost:23333/` in your browser.

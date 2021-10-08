release: python -m pip install -e .
web: gunicorn --worker-class eventlet -w 1 test_gallery.auto_advance:app
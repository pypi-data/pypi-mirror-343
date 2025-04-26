from flask import Flask
import inspect
import sys

try:
    # Try direct import
    from api import app
    print('Available routes:')
    for rule in app.url_map.iter_rules():
        print(f'  {rule.endpoint} -> {rule.rule}')
except Exception as e1:
    print(f"Error with direct import: {e1}")
    try:
        # Try importing directly from the file
        import importlib.util
        spec = importlib.util.spec_from_file_location("api", "./api.py")
        api_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(api_module)
        
        app = api_module.app
        print('\nAvailable routes:')
        for rule in app.url_map.iter_rules():
            print(f'  {rule.endpoint} -> {rule.rule}')
    except Exception as e2:
        print(f"Error with file import: {e2}") 
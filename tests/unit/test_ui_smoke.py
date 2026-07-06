"""
Smoke tests for the Streamlit UI.
Verifies that the app renders without syntax errors or unhandled exceptions.
"""
import pytest
from streamlit.testing.v1 import AppTest

def test_ui_renders_successfully():
    """
    Test that the Streamlit app loads and renders the main components.
    """
    import os
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    app_path = os.path.join(project_root, "app", "ui", "app.py")
    app = AppTest.from_file(app_path)
    app.run()
    
    assert not app.exception

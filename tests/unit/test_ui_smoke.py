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
    app = AppTest.from_file("app/ui/app.py")
    app.run()
    
    assert not app.exception
    assert "ThinkFlow Studio" in app.title[0].value
    
    # Check that text area and run button are rendered
    assert len(app.text_area) > 0
    assert len(app.button) > 0
    assert app.button[0].label == "Run Analysis"

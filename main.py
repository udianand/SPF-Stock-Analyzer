
import os
import sys

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Run the Streamlit app
if __name__ == "__main__":
    os.system("streamlit run app.py")

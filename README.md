# :bar_chart: Volume Visualizer

An app that teaches users via animation how to calculate the volume of a solid created by revolving a function about an axis.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://volume-visualizer.streamlit.app/)

### How to run it on your own machine

Some steps taken from [Streamlit docs](https://docs.streamlit.io/get-started/installation/command-line)

1. Create a virtual environment

   ```
   python -m venv .venv
   ```

2. Activate your environment

   ```
   # Windows command prompt
   .venv\Scripts\activate.bat

   # Windows PowerShell
   .venv\Scripts\Activate.ps1

   # macOS and Linux
   source .venv/bin/activate
   ```

3. Install [Manim](https://docs.manim.community/en/stable/installation.html)

4. Get a TeX distribution such as [MiKTeX](https://miktex.org/download)
   (Windows users - add the directory containing latex.exe to PATH)

5. Install the requirements

   ```
   pip install -r requirements.txt
   ```

6. Run the app

   ```
   streamlit run streamlit_app.py
   ```

If pycairo fails to install, follow the installation steps [here](https://pycairo.readthedocs.io/en/latest/getting_started.html)

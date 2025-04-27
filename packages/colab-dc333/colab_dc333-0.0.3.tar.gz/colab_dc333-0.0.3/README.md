# Install
pip install colab-dc333

# How to use
>>> from colab_dc333 import nvidia
>>> nvidia.update_12_4()



To update pypi
increment version in pyproject.toml 
>python -m build 
>python3 -m twine upload --repository pypi dist/*

activate a venv with twine installed 


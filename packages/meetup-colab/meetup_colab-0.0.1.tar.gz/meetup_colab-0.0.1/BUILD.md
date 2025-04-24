Build instructions


# should create dist/ with a tar.gz and egg file
python -m build
# should upload assuming .pypirc is configured with token  
python -m twine upload --repository pypi dist/* 



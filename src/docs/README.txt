# Generate rst documents - autodoc
sphinx-apidoc --force --separate -o .\api ..

# Build HTML page
sphinx-build -b html . ..\data\www\documentation

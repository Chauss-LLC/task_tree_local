# Linters and code checkers

Here are linters and code checkers that we use for developing the product.

Before pushing to `master` branch or before creating a pull request, please, perform the next steps:

1. From the repository directory create a virtual environment for linters. 
```
python3 -m venv ./venv
. venv/bin/activate
```
2. Install linters to your environment:
```
pip install -r linters/linters_requirements.txt
```
3. Run the shell script to ensure that your code is 'ok':
```
chmod +x linters/linters_run.sh
./linters/linters_run.sh $(git ls-files '*.py')
```
4. When you done, you can delete trash files:
```
deactivate
rm -r venv
``` 
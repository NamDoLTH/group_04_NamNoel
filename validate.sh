# script that validates if the project code is up to
# the standard proposed in the course

# to be used if you use Linux or macOS
# in the shell, with your virtual environment activated, run:
# source validate.sh

flake8 ./codeapp
flake=$?

pylint -s n ./codeapp
pyl=$?

black ./codeapp --check
blc=$?

mypy ./codeapp
mp=$?

isort ./codeapp --check-only --diff
is=$?

coverage run -m pytest --log-cli-level="CRITICAL"
coverage report
cov=$?

# printing output
if [ $flake -eq 0 ]
then
    echo "Flake8\tPass"
else
    echo "Flake8\tFail"
fi

if [ $pyl -eq 0 ]
then
    echo "Pylint\tPass"
else
    echo "Pylint\tFail"
fi

if [ $blc -eq 0 ]
then
    echo "Black\tPass"
else
    echo "Black\tFail"
fi

if [ $mp -eq 0 ]
then
    echo "Mypy\tPass"
else
    echo "Mypy\tFail"
fi

if [ $is -eq 0 ]
then
    echo "isort\tPass"
else
    echo "isort\tFail"
fi

if [ $cov -eq 0 ]
then
    echo "Tests\tPass"
else
    echo "Tests\tFail"
fi
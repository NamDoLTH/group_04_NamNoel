# script that validates if the project code is up to
# the standard proposed in the course

# to be used if you use Windows
# in the PowerShell, run:
# .\validate.ps1

# run flake8
flake8 ./codeapp
$flake = $?

# run pylint
pylint -s n ./codeapp
$pyl = $?

# run black
black ./codeapp --check
$blc = $?

# run mypy
mypy ./codeapp
$mp = $?

# run isort
isort ./codeapp --check-only --diff
$is = $?

# run tests and code coverage
coverage run -m pytest --log-cli-level="CRITICAL"
$test = $?
coverage report
$cov = $?

# printing output
if ( $flake ) {
    Write-Output "Flake8`tPass"
} else {
    Write-Output "Flake8`tFail"
}

if ( $pyl ) {
    Write-Output "Pylint`tPass"
} else {
    Write-Output "Pylint`tFail"
}

if ( $blc ) {
    Write-Output "Black`tPass"
} else {
    Write-Output "Black`tFail"
}

if ( $mp ) {
    Write-Output "Mypy`tPass"
} else {
    Write-Output "Mypy`tFail"
}

if ( $is ) {
    Write-Output "isort`tPass"
} else {
    Write-Output "isort`tFail"
}

if ( $test -and $cov ) {
    Write-Output "Tests`tPass"
} else {
    Write-Output "Tests`tFail"
}

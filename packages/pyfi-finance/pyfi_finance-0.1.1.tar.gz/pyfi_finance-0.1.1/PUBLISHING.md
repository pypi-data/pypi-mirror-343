# Publishing to PyPI

This document provides instructions for publishing the `pyfi-finance` package to PyPI.

## Pre-Publishing Checklist

Before publishing your package to PyPI, make sure to verify:

1. All tests pass
2. Documentation is up-to-date
3. Version number has been incremented in `__init__.py`
4. Command-line tools are working correctly:
   ```bash
   pip install .
   compound-interest --principal 1000 --rate 0.05 --time 5
   option-price --stock-price 100 --strike-price 95 --time 0.5 --rate 0.02 --volatility 0.25
   portfolio-optimize --returns 0.05 0.1 0.15 --cov-matrix 0.04 0.02 0.01 0.02 0.09 0.03 0.01 0.03 0.16
   ```

## Option 1: Using Environment Variables

You can set environment variables to automate the authentication process with twine.

### In PowerShell (temporary, for current session only):

```powershell
$env:TWINE_USERNAME = "your_username"
$env:TWINE_PASSWORD = "your_password_or_token"

# Then run twine
twine upload dist/*
```

### In PowerShell (persistent, for your user account):

```powershell
[Environment]::SetEnvironmentVariable("TWINE_USERNAME", "your_username", "User")
[Environment]::SetEnvironmentVariable("TWINE_PASSWORD", "your_password_or_token", "User")
```

### In CMD (temporary, for current session only):

```cmd
set TWINE_USERNAME=your_username
set TWINE_PASSWORD=your_password_or_token

REM Then run twine
twine upload dist/*
```

### In CMD (persistent, for your user account):

```cmd
setx TWINE_USERNAME "your_username"
setx TWINE_PASSWORD "your_password_or_token"
```

## Option 2: Using .pypirc File

Create a `.pypirc` file in your home directory (`%USERPROFILE%` on Windows, `~` on Unix-like systems).

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = your_username
password = your_password_or_token

[testpypi]
repository = https://test.pypi.org/legacy/
username = your_username
password = your_password_or_token
```

Then use the repository name when uploading:

```bash
twine upload --repository pypi dist/*
# or for TestPyPI
twine upload --repository testpypi dist/*
```

## Security Considerations

1. It's recommended to use an API token instead of your actual password.
2. When using environment variables, be careful not to expose them in scripts that might be shared.
3. The `.pypirc` file should have restricted permissions (e.g., `chmod 600 ~/.pypirc` on Unix-like systems).
4. Never commit credentials to version control systems.

## Using API Tokens (Recommended)

1. Log in to your PyPI account
2. Go to Account Settings → API tokens
3. Create a new token (you can scope it to a specific project)
4. Use this token as your password when uploading

## Automation Scripts

Three automation scripts are provided:

1. `publish_with_env.ps1` - Uses environment variables, with prompts
2. `publish_with_pypirc.ps1` - Uses .pypirc file, with prompts
3. `publish_auto.ps1` - Fully automated with hardcoded credentials (edit before using)

Example usage for `publish_auto.ps1`:

```powershell
# For TestPyPI
./publish_auto.ps1 test

# For PyPI
./publish_auto.ps1 prod
```

## Verifying Your Published Package

After publishing, verify your package works correctly by installing it from PyPI:

```bash
# For TestPyPI
pip install --index-url https://test.pypi.org/simple/ pyfi-finance

# For PyPI
pip install --upgrade pyfi-finance
```

Then test that command-line tools work properly:

```bash
compound-interest --help
option-price --help
portfolio-optimize --help
``` 
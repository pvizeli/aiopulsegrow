# Release Instructions

This document describes how to release a new version of aiopulsegrow to PyPI.

## Prerequisites

1. Ensure you have maintainer access to the PyPI project
2. All tests are passing on the main branch
3. CHANGELOG has been updated with new version details
4. Version number has been updated in `pyproject.toml`

## Release Process

The package uses GitHub Actions to automatically build and publish to PyPI when a new release is created.

### Steps to Release

1. **Update Version Number**

   Edit `pyproject.toml` and update the version:
   ```toml
   version = "0.2.0"  # Update to new version
   ```

2. **Update Version in __init__.py**

   Edit `aiopulsegrow/__init__.py`:
   ```python
   __version__ = "0.2.0"  # Update to match pyproject.toml
   ```

3. **Commit Changes**
   ```bash
   git add pyproject.toml aiopulsegrow/__init__.py
   git commit -m "Bump version to 0.2.0"
   git push origin main
   ```

4. **Create Git Tag**
   ```bash
   git tag -a v0.2.0 -m "Release version 0.2.0"
   git push origin v0.2.0
   ```

5. **Create GitHub Release**

   Go to GitHub and create a new release:
   - Click "Releases" → "Draft a new release"
   - Choose the tag you just created (v0.2.0)
   - Set release title: "v0.2.0"
   - Add release notes describing changes
   - Click "Publish release"

6. **Automated Publishing**

   Once the release is published, GitHub Actions will automatically:
   - Run all tests
   - Build the package (wheel and sdist)
   - Publish to PyPI
   - Publish to TestPyPI (optional)

## Manual Publishing (if needed)

If you need to publish manually:

1. **Build the package**
   ```bash
   pip install build twine
   python -m build
   ```

2. **Check the distribution**
   ```bash
   twine check dist/*
   ```

3. **Upload to TestPyPI (optional)**
   ```bash
   twine upload --repository testpypi dist/*
   ```

4. **Upload to PyPI**
   ```bash
   twine upload dist/*
   ```

## PyPI Configuration

### First-time Setup

For the automated GitHub Actions workflow to work, you need to configure PyPI publishing:

1. **Enable Trusted Publishing on PyPI**
   - Go to https://pypi.org/manage/account/publishing/
   - Add a new publisher
   - Set publisher name: `yourusername/aiopulsegrow`
   - Set workflow name: `publish.yml`
   - Set environment name: `pypi`

2. **Configure GitHub Environments**
   - Go to repository Settings → Environments
   - Create environment: `pypi`
   - Create environment: `testpypi` (optional)

## Versioning

This project follows [Semantic Versioning](https://semver.org/):

- **MAJOR** version (1.0.0): Incompatible API changes
- **MINOR** version (0.1.0): Add functionality in a backwards compatible manner
- **PATCH** version (0.0.1): Backwards compatible bug fixes

## Checklist Before Release

- [ ] All tests pass locally
- [ ] All tests pass on CI
- [ ] Version number updated in `pyproject.toml`
- [ ] Version number updated in `__init__.py`
- [ ] CHANGELOG updated (if you have one)
- [ ] Documentation is up to date
- [ ] All commits are on main branch
- [ ] Git tag created
- [ ] GitHub release created

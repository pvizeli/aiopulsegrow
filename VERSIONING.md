# Versioning

This project uses **automatic semantic versioning** based on git tags. The version is not hardcoded in the codebase but determined dynamically during the build process.

## How It Works

We use [setuptools-scm](https://github.com/pypa/setuptools-scm) to automatically determine the version from git tags:

- **With tags**: Version comes from the latest git tag (e.g., `v0.1.0` or `0.1.0` → `0.1.0`)
- **Without tags**: Fallback to `0.0.0.dev0` during development

## Creating a Release

To release a new version:

1. **Create and push a git tag**:
   ```bash
   # With 'v' prefix (recommended)
   git tag v0.1.0
   git push origin v0.1.0

   # Or without 'v' prefix (also works)
   git tag 0.1.0
   git push origin 0.1.0
   ```

2. **Create a GitHub Release**:
   - Go to GitHub → Releases → Create a new release
   - Choose the tag you just created
   - GitHub Actions will automatically build and publish to PyPI

## Version Format

Use semantic versioning format: `X.Y.Z` (optionally with `v` prefix)

- `v0.1.0` or `0.1.0` - Initial release
- `v0.2.0` or `0.2.0` - Minor version with new features
- `v0.2.1` or `0.2.1` - Patch version with bug fixes
- `v1.0.0` or `1.0.0` - Major release

Both formats work - choose whichever you prefer!

## Development Versions

During development (no tags), the version is `0.0.0.dev0`. This ensures development installations don't conflict with released versions.

## CI/CD Integration

The GitHub Actions workflows automatically:
- Determine the version from the git tag
- Build the package with the correct version
- Publish to PyPI when a release is created

No manual version updates needed!

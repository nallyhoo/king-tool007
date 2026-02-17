
# Release Checklist

This checklist should be followed for every production release.

## Pre-Release

- [ ] All new features have been tested on the staging environment.
- [ ] All critical bugs have been fixed.
- [ ] The `develop` branch has been merged into the `main` branch.
- [ ] A new version tag has been created in Git (e.g., `v1.2.0`).
- [ ] Release notes have been drafted.

## Release

- [ ] The `main` branch has been pushed to GitHub, triggering the production deployment workflow.
- [ ] The production deployment has completed successfully.
- [ ] Smoke tests have been performed on the production environment.

## Post-Release

- [ ] The new version has been announced to users (if applicable).
- [ ] The performance of the new release is being monitored.
- [ ] The release notes have been published.

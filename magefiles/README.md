# ansible-collection-workstation/magefiles

`magefiles` provides utilities that would normally be managed
and executed with a `Makefile`. Instead of being written in the make language,
magefiles are crafted in Go and leverage the [Mage](https://magefile.org/) library.

---

## Table of contents

- [Functions](#functions)
- [Contributing](#contributing)
- [License](#license)

---

## Functions

### CreateRelease()

```go
CreateRelease() error
```

CreateRelease creates a release on GitHub.

**Parameters:**

version: A string representing the version to use for the release.

Example usage:

```bash
NEXT_VERSION=1.0.0 mage createrelease
```

**Returns:**

error: An error if any issue occurs while trying to create the release.

---

### GenChangeLog()

```go
GenChangeLog() error
```

GenChangeLog generates the changelog used by Ansible Galaxy.

Example usage:

```bash
mage genchangelog
```

**Returns:**

error: An error if any issue occurs while trying to generate the changelog.

---

### GenerateMagePackageDocs()

```go
GenerateMagePackageDocs() error
```

GenerateMagePackageDocs creates documentation for the various packages
in the project.

Example usage:

```go
mage generatemagepackagedocs
```

**Returns:**

error: An error if any issue occurs during documentation generation.

---

### InstallDeps()

```go
InstallDeps() error
```

InstallDeps installs the Go dependencies necessary for developing
on the project.

Example usage:

```go
mage installdeps
```

**Returns:**

error: An error if any issue occurs while trying to
install the dependencies.

---

### LintAnsible()

```go
LintAnsible() error
```

LintAnsible runs the ansible-lint linter.

Example usage:

```bash
mage lintansible
```

**Returns:**

error: An error if any issue occurs while trying to run the linter.

---

### RunMoleculeTests()

```go
RunMoleculeTests() error
```

RunMoleculeTests runs the molecule tests.

Example usage:

```bash
mage runmoleculetests
```

**Returns:**

error: An error if any issue occurs while trying to run the tests.

---

### RunPreCommit()

```go
RunPreCommit() error
```

RunPreCommit updates, clears, and executes all pre-commit hooks
locally. The function follows a three-step process:

First, it updates the pre-commit hooks.
Next, it clears the pre-commit cache to ensure a clean environment.
Lastly, it executes all pre-commit hooks locally.

Example usage:

```go
mage runprecommit
```

**Returns:**

error: An error if any issue occurs at any of the three stages
of the process.

---

## Contributing

Pull requests are welcome. For major changes,
please open an issue first to discuss what
you would like to change.

---

## License

This project is licensed under the MIT
License - see the [LICENSE](../LICENSE)
file for details.

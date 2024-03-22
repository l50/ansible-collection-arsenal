//go:build mage
// +build mage

package main

import (
	"fmt"
	"log/slog"
	"os"
	"os/exec"
	"path/filepath"

	"github.com/fatih/color"
	"github.com/l50/goutils/v2/git"
	log "github.com/l50/goutils/v2/logging"
	"github.com/l50/goutils/v2/sys"
	"github.com/spf13/afero"
)

var repoRoot string

func init() {
	var err error
	repoRoot, err = git.RepoRoot()
	if err != nil {
		fmt.Fprintf(os.Stderr, "failed to get repo root: %v", err)
		os.Exit(1)
	}
}

// RunMoleculeTests runs the molecule tests.
//
// Example usage:
//
// ```bash
// mage runmoleculetests
// ```
//
// **Returns:**
//
// error: An error if any issue occurs while trying to run the tests.
func RunMoleculeTests() error {
	fs := afero.NewOsFs()
	rolesDir := "roles"

	roles, err := afero.ReadDir(fs, rolesDir)
	if err != nil {
		return fmt.Errorf("failed to list roles: %v", err)
	}

	logsDir := filepath.Join(repoRoot, "logs")
	cfgPath := filepath.Join(repoRoot, "ansible.cfg")
	os.Setenv("ANSIBLE_CONFIG", cfgPath)

	if err := fs.MkdirAll(logsDir, 0755); err != nil {
		return fmt.Errorf("failed to create logs directory: %v", err)
	}

	// Configure logger
	logCfg := log.LogConfig{
		Fs:         afero.NewOsFs(),
		LogPath:    filepath.Join(logsDir, "molecule_tests.log"),
		Level:      slog.LevelInfo,
		OutputType: log.ColorOutput,
		LogToDisk:  true,
	}

	Logger, err := log.InitLogging(&logCfg)
	if err != nil {
		return fmt.Errorf("failed to configure logger: %v", err)
	}

	// Set the global logger
	log.GlobalLogger = Logger

	errCh := make(chan error, len(roles))

	for _, role := range roles {
		if !role.IsDir() {
			continue
		}

		rolePath := filepath.Join(rolesDir, role.Name())
		log.L().Printf("Running molecule tests for the %s role\n", role.Name())

		cmd := exec.Command("molecule", "test")
		cmd.Dir = rolePath // Set the working directory for the command

		log.L().Printf("Executing command: %v in directory: %s\n", cmd.Args, cmd.Dir)

		output, err := cmd.CombinedOutput()
		if err != nil {
			errCh <- fmt.Errorf("failed to run molecule tests for role %s: %v. Output: %s",
				role.Name(), err, string(output))
		}
	}

	close(errCh)

	var errors []error
	for err := range errCh {
		errors = append(errors, err)
	}

	// Summarize the test results
	if len(errors) > 0 {
		log.L().Printf("Molecule tests failed for %d role(s).", len(errors))
		for _, err := range errors {
			log.L().Error(err)
		}
		return fmt.Errorf("encountered errors: %v", errors)
	} else {
		log.L().Printf("Molecule tests passed for %d/%d role(s).", len(roles), len(roles))
	}

	return nil
}

// LintAnsible runs the ansible-lint linter.
//
// Example usage:
//
// ```bash
// mage lintansible
// ```
//
// **Returns:**
//
// error: An error if any issue occurs while trying to run the linter.
func LintAnsible() error {
	cmds := []string{
		"ansible-lint",
		"--force-color",
		"-c",
		".hooks/linters/ansible-lint.yaml",
	}

	fmt.Println(color.YellowString("Running ansible-lint."))
	if _, err := sys.RunCommand(cmds[0], cmds[1:]...); err != nil {
		return fmt.Errorf(color.RedString("failed to run ansible-lint: %v", err))
	}

	return nil
}

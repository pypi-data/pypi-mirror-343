# Scrapbook

- Scrapbook is a way to journal your goals, challenges, solutions and more, on a daily basis, which I guess is aimed to simplify tracking what you do everyday (kinda like note taking really)
- I wanted a simple way of logging what I do everyday on my terminal (without really installing/opening other note taking apps), hence the script.

## Preface

This project is a work-in-progress and should be considered experimental. It is being actively developed and refined as I learn.

**Current Status**

- The project is incomplete and lacks many essential features.
- Some implementations may not be optimal or fully tested.
- Code quality and best practices may vary due to ongoing learning.

## Functionality:

- Generates markdown doc of everyday notes.
- Simple structure.
- Easy way to filter through your notes everyday using unix tools.

## Installation

Installing is as simple as:

```bash
pip install scrapbooking-cli
```

Invoke using `sb`:

```bash
sb
```

### Config-based approach

When `scraps-cli` is installed for the first time, `scraps-cli` searches for a config file in your current directory named `scrapbook_config.yaml`. If one is not found in your current directoy, a default config is used/created (if the default is not found either).

The default config uses the following structure and is created in the `~/.config/` directory:

```yaml
headings:
  tasks: "Tasks"
  challenges: "Challenges"
  solutions: "Solutions"
  decisions_made: "Decisions Made"
  learnings: "Learnings"
  next_steps: "Next Steps"
  additional_notes: "Additional Notes"
  conclusion: "conclusion"
```

You are free to modify the headings according to what you see fit, add or remove etc.

The order of precedence is:
- Search in current directory for a config file. If found, use this.
- If config file not found in current directory, fallback to using the default config.
- If default config not found, create one.

# AIGauntlet
A pip-installable library to locally run a gauntlet test on your AI agent or system.

## Installation

```bash
pip install aigauntlet
```

## Quick Start

```python
from aigauntlet import QuickPrivacyTrial

# Create and run a privacy trial
trial = QuickPrivacyTrial(agent_function=your_agent_function)
results = trial.run()
```

## Features

- Evaluate AI agent privacy protections
- Test agent responses to various prompts
- Generate detailed reports on agent performance

## Requirements

- Python 3.12+
- Dependencies are automatically installed with pip

## License

This project is licensed under the terms of the license included in the repository.

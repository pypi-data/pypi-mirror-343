# 🤖 Generate Custom Prompts

A small toolkit to collect code from local directories and automatically generate ChatGPT prompts.

---

## 📁 Contents

- **copy-jh-clipboard.py**  
  Copies files or entire directories (recursive) to the clipboard or stdout, with banner headers and indentation.

- **gen-jh-prompt.py**  
  Reads the clipboard output and builds a ChatGPT prompt based on templates defined in `.jhpromptconfig`.

---

## 🚀 Installation

1. Ensure you have Python 3.7 or higher.
2. Install package:
   ```bash
   pip install jh-prompt-gen

---
## ⚙️ Configuration & Ignore

If a `.jhpromptconfig` or `.jhclipignore` file exists in the target directory, it will be automatically applied when running the tool. To specify a different config or ignore file, use the `-c` (`--config-file`) or `-I` (`--ignore-file`) options respectively.

---

## 🔒 Privacy & Security

For security reasons, you can target only specific subdirectories; this prevents accidental exposure of root-level or sensitive files. Use ignore patterns in `.jhclipignore` to exclude sensitive files (e.g., credentials, logs, personal data) from being sent to the AI.

---


## 📝 Example `.jhclipignore`

```gitignore
.jh*
.DS_Store
.git/
frontend/node_modules/
frontend/dist/
frontend/package-lock.json
frontend/public/rootCA.pem
```

### 🔍 How `.jhclipignore` works

- Follows Git’s ignore semantics (glob patterns).  
- Lines without a trailing slash match files anywhere (`.DS_Store` matches any file named `.DS_Store`).  
- Patterns ending with `/` only match directories and their contents (`.git/` excludes the `.git` folder).  
- Wildcards (`*`) match zero or more characters (`.jh*` matches `.jhclipignore`, `.jhpromptconfig`, etc.).

---

## ⚙️ Example `.jhpromptconfig`

```ini
persona="You are a React developer."
project="My Project"

sophisticated_prompt="""
{persona}. Optimize my {project}. Please make it even better using advanced patterns.

My code:
{code}

New Feature: {feature}
"""

default_prompt_pattern="""
{persona}. Optimize my {project}.

My code:
{code}

New Feature: {feature}
"""
```

### 🔍 How `.jhpromptconfig` works

- **Single-line entries**: `KEY=value` sets simple variables (e.g. `persona`, `project`).  
- **Multi-line templates**: `KEY="""..."""` allows you to define named prompt templates containing `{placeholders}`.  
- **Default template**: the `default_prompt_pattern` key is used when you don’t specify a template name.  
- **Named templates**: any other key (e.g. `sophisticated_prompt`) can be selected via the `--pattern` option in `gen-jh-prompt.py`.  
- **Placeholders**: `{code}` inserts captured code, `{feature}` inserts your feature description, and you can add any custom placeholders and override them with `-f KEY=VALUE`.


---
## ⚡️ Usage 
### 💬 Generate Custom Prompt with project code to clipboard

#### Default prompt template: "default_prompt_pattern"
`jh-gen-prompt.py ./src "Add authentication"`

#### Named template from .jhpromptconfig
`jh-gen-prompt.py ./src "Add authentication" -p sophisticated_prompt`

### 📋 Copy only code to clipboard

#### Default ignore rules
`jh-copy-clipboard.py ./src`

#### Custom ignore patterns and explicit ignore file
`jh-copy-clipboard.py ./src -i '*.pyc' -i 'node_modules/' -I .jhclipignore`

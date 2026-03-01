# CLAUDE.md — FastAPI Cookiecutter Template

## What This Is

This is a **Cookiecutter template**, not a Python application. You cannot run or test it directly — it generates projects via `cookiecutter .`.

## Repository Layout

```
cookiecutter.json                          # All template prompts + defaults
hooks/post_gen_project.py                  # Runs after generation: secrets + conditional file removal
{{cookiecutter.project_slug}}/             # The template directory (Jinja2-processed)
docs/                                      # Design docs and plans
```

## Key Architecture

- **`cookiecutter.json`** — Defines all 18 user prompts. Choices use lists (first item = default). Derived values use Jinja2 expressions.
- **`{{cookiecutter.project_slug}}/`** — Every file inside is processed by Jinja2 during generation. The directory name itself becomes the project slug.
- **`hooks/post_gen_project.py`** — Post-generation hook that: (1) generates cryptographic secrets for env files, (2) removes files for disabled optional features.

## Jinja2 Gotchas

### No f-strings with template variables
Python f-strings use `{}` which conflicts with Jinja2's `{{ }}`. Use string concatenation instead:
```python
# WRONG — Jinja2 will try to evaluate the f-string braces
url = f"https://{{ cookiecutter.domain_name }}/api"

# RIGHT — use concatenation
url = "https://" + "{{ cookiecutter.domain_name }}" + "/api"

# ALSO RIGHT — plain Jinja2 substitution (no f-string)
url = "https://{{ cookiecutter.domain_name }}/api"
```

### Template directory vs template variable
- **Directory name**: `{{cookiecutter.project_slug}}` (no spaces) — this is the literal folder name
- **Inside files**: `{{ cookiecutter.project_slug }}` (with spaces) — this is Jinja2 syntax that gets replaced

### Conditional blocks
Use Jinja2 `{% if %}` to conditionally include code blocks within files:
```python
{% if cookiecutter.use_celery == "y" %}
from .celery_app import celery
{% endif %}
```

## Conditional Features

Features are made optional via two mechanisms:

1. **Jinja2 conditionals in file contents** — wraps imports, config blocks, service definitions
2. **`post_gen_project.py` file removal** — deletes entire files for disabled features

| Feature | Files Removed When Disabled |
|---------|---------------------------|
| `use_celery != "y"` | `celery_app.py`, `auth/tasks.py` |
| `use_sentry != "y"` | `core/sentry.py` |
| `cloud_storage == "None"` | `core/storage.py` |
| `ci_tool != "GitHub Actions"` | `.github/` directory |
| `ci_tool != "GitLab CI"` | `.gitlab-ci.yml` |
| `use_pre_commit != "y"` | `.pre-commit-config.yaml` |
| `license == "Proprietary"` | `LICENSE` |

## Testing Changes

After modifying templates, verify by generating a project:

```bash
# Generate with defaults
cookiecutter . --no-input -o /tmp/test

# Validate generated Python files parse correctly
cd /tmp/test/my_fastapi_project
python -c "
import ast, glob
for f in glob.glob('src/**/*.py', recursive=True):
    ast.parse(open(f).read())
    print(f'OK: {f}')
"

# Validate Docker Compose files
docker compose -f docker-compose.local.yml config
docker compose -f docker-compose.production.yml config
```

To test with non-default options:
```bash
cookiecutter . --no-input -o /tmp/test_no_celery use_celery=n
cookiecutter . --no-input -o /tmp/test_no_extras use_celery=n use_sentry=n cloud_storage=None ci_tool=None
```

## Common Tasks

- **Add a new cookiecutter option**: Add to `cookiecutter.json`, use in templates with `{{ cookiecutter.option_name }}`, handle in `post_gen_project.py` if files need conditional removal.
- **Add a new file to the template**: Place it inside `{{cookiecutter.project_slug}}/`. If it's conditional, add removal logic to `post_gen_project.py`.
- **Modify Docker services**: Edit `docker-compose.local.yml` and/or `docker-compose.production.yml`. Use Jinja2 conditionals for optional services.

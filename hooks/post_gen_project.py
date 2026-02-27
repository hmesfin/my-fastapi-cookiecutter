"""Post-generation hook: removes unused files and generates secrets."""

import os
import secrets
import shutil

PROJECT_DIR = os.path.realpath(os.path.curdir)


def remove_file(filepath: str) -> None:
  path = os.path.join(PROJECT_DIR, filepath)
  if os.path.isfile(path):
    os.remove(path)


def remove_dir(dirpath: str) -> None:
  path = os.path.join(PROJECT_DIR, dirpath)
  if os.path.isdir(path):
    shutil.rmtree(path)


def generate_secret(length: int = 64) -> str:
  return secrets.token_urlsafe(length)


def replace_in_file(filepath: str, old: str, new: str) -> None:
  path = os.path.join(PROJECT_DIR, filepath)
  if not os.path.isfile(path):
    return
  with open(path) as f:
    content = f.read()
  content = content.replace(old, new)
  with open(path, "w") as f:
    f.write(content)


# Generate secrets
secret_key = generate_secret(64)
postgres_password = generate_secret(32)

# Write secrets into env files
for env_dir in [".envs/.local", ".envs/.production"]:
  replace_in_file(
    os.path.join(env_dir, ".app"),
    "!!!SET BY POST_GEN_HOOK!!!",
    secret_key,
  )
  replace_in_file(
    os.path.join(env_dir, ".postgres"),
    "!!!SET BY POST_GEN_HOOK!!!",
    postgres_password,
  )

# Conditional file removal
if "{{ cookiecutter.use_celery }}" != "y":
  remove_file("src/{{ cookiecutter.project_slug }}/celery_app.py")
  remove_file("src/{{ cookiecutter.project_slug }}/auth/tasks.py")

if "{{ cookiecutter.use_sentry }}" != "y":
  remove_file("src/{{ cookiecutter.project_slug }}/core/sentry.py")

if "{{ cookiecutter.cloud_storage }}" == "None":
  remove_file("src/{{ cookiecutter.project_slug }}/core/storage.py")

if "{{ cookiecutter.ci_tool }}" != "GitHub Actions":
  remove_dir(".github")

if "{{ cookiecutter.ci_tool }}" != "GitLab CI":
  remove_file(".gitlab-ci.yml")

if "{{ cookiecutter.use_pre_commit }}" != "y":
  remove_file(".pre-commit-config.yaml")

if "{{ cookiecutter.use_mailpit }}" != "y":
  # Mailpit references are handled via Jinja2 conditionals in compose files
  pass

if "{{ cookiecutter.license }}" == "Proprietary":
  remove_file("LICENSE")

print("Project generated successfully!")
print(f"  cd {{ cookiecutter.project_slug }}")
print("  docker compose -f docker-compose.local.yml up --build")

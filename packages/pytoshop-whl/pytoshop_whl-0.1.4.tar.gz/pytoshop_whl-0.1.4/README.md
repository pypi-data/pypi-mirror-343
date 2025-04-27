## build

```shell
uv sync --only-dev
uv run cibuildwheel --output-dir wheelhouse --only cp310-win_amd64
uv run cibuildwheel --output-dir wheelhouse --only cp310-manylinux_x86_64
```

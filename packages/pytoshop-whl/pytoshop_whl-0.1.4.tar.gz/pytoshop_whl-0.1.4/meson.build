project(
  'pytoshop-whl',
  # ===
  'c',
  'cython',
  # ===
  version: '0.1',
  meson_version: '>= 1.3',
  default_options: [
    'cython_args=-3',
    'c_std=c99',
    'buildtype=debugoptimized',
  ]
)

fs = import('fs')
py = import('python').find_installation(pure: false)

py_dep = py.dependency()

subdir('pytoshop')

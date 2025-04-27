py.extension_module(
  'packbits',
  'packbits.pyx',
  c_args: [],
  dependencies: [py_dep],
  install: true,
  install_dir: py.get_install_dir() / 'pytoshop',
)

# インストールする際のソースコードの指定 ビルド済み配布物に含める場合に必要
py.install_sources(
  [
    '__init__.py',
    'blending_range.py',
    'codecs.py',
    'color_mode.py',
    'core.py',
    'docs.py',
    'enums.py',
    'image_data.py',
    'image_resources.py',
    'layers.py',
    'packbits.pyi',
    'path.py',
    'tagged_block.py',
    'util.py'
  ],
  subdir: 'pytoshop',  # インストールする際のディレクトリパス
)

subdir('user')


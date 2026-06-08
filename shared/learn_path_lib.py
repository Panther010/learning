from pathlib import Path

path = Path(__file__)

print(path)
print(path.name)
print(path.stem)
print(path.suffix)
print(path.parent)
print(path.parent.parent)

# checking path exists or not
p = Path('C:/Users/Bakul')/ 'Downloads' / 'Task'/ 'Task'/'CLAUDE.md'
print(p.exists())
print(p.is_file())
print(p.is_dir())
print(p.resolve())
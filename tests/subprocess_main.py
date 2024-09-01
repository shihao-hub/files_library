import subprocess

process = subprocess.Popen(
    ["python", "subprocess_child_script.py"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
)

print(*[e.decode("utf-8") for e in process.communicate(input=b"Hello")], sep="\n")

import json
import os
import sys

data = '{"nama": "Fakhry", "nilai": 88}'
mahasiswa = json.loads(data)


def tampil(m):
    print("Nama:", m["nama"])
    print("Nilai:", m["nilai"])


tampil(mahasiswa)
print(sys.version_info.major, os.name)

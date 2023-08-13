import json


with open('github_analysis.json') as f:
    d = json.load(f)

    all = len(d)
    gradle = 0
    maven = 0
    bundle = 0
    for i in d:
        if d[i]['gradle']:
            gradle+=1

        if d[i]['maven']:
            maven+=1

        if d[i]['bundler']:
            bundle+=1

    print(f"Gradle: {gradle}/{all}")
    print(f"Maven: {maven}/{all}")
    print(f"Bundler: {bundle}/{all}")
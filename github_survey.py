import json

# Authentication is defined via github.Auth
from github import Auth
from github import Github

# using an access token
auth = Auth.Token("token")

# First create a Github instance:

# Public Web Github
g = Github(auth=auth)

repos = g.search_repositories("language:java", sort="stars")
result_repos = {}
i = 0
num_repos = 6000

for repo in repos[:num_repos]:

    # get language list with lines of code
    languages = repo.get_languages()
    i+=1

    if ('JavaScript' in languages and languages['JavaScript'] >= 100) or ('TypeScript' in languages and languages['TypeScript'] >=100):

        print(f"Java + JS repo found: {repo.url}")
        repo_stats = {}
        repo_stats['gradle'] = False
        repo_stats['maven'] = False
        repo_stats['bundler'] = False

        # check build tool
        try:
            contents = repo.get_contents("gradlew")
            repo_stats['gradle'] = True
        except:
            pass

        if not repo_stats['gradle']:
            try:
                contents = repo.get_contents("build.gradle")
                repo_stats['gradle'] = True
            except:
                pass

        if not repo_stats['gradle']:
            try:
                contents = repo.get_contents("gradle.properties")
                repo_stats['gradle'] = True
            except:
                pass

        if not repo_stats['gradle']:
            try:
                contents = repo.get_contents("build.gradle.kts")
                repo_stats['gradle'] = True
            except:
                pass

        try:
            contents = repo.get_contents("mvnw")
            repo_stats['maven'] = True
        except:
            pass

        if not repo_stats['maven']:
            try:
                contents = repo.get_contents("pom.xml")
                repo_stats['maven'] = True
            except:
                pass

        # check for bundler/transpiler
        if not repo_stats['bundler']:
            try:
                contents = repo.get_contents("webpack.config.js")
                repo_stats['bundler'] = True
            except:
                pass

        if not repo_stats['bundler']:
            try:
                contents = repo.get_contents("parcel.json")
                repo_stats['bundler'] = True
            except:
                pass

        if not repo_stats['bundler']:
            try:
                contents = repo.get_contents("rollup.config.js")
                repo_stats['bundler'] = True
            except:
                pass

        if not repo_stats['bundler']:
            try:
                contents = repo.get_contents("snowpack.config.js")
                repo_stats['bundler'] = True
            except:
                pass

        if not repo_stats['bundler']:
            try:
                contents = repo.get_contents("vite.config.js")
                repo_stats['bundler'] = True
            except:
                pass

        if not repo_stats['bundler']:
            try:
                contents = repo.get_contents("fuse.js")
                repo_stats['bundler'] = True
            except:
                pass

        if not repo_stats['bundler']:
            try:
                contents = repo.get_contents("tsconfig.json")
                repo_stats['bundler'] = True
            except:
                pass

        if not repo_stats['bundler']:
            try:
                contents = repo.get_contents("babel.config.js")
                repo_stats['bundler'] = True
            except:
                pass

        result_repos[repo.url] = repo_stats

print(f"Found: {len(result_repos)}/{i}")

# save data
with open("github_analysis.json", "w") as result_file:
    json.dump(result_repos, result_file)

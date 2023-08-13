import json
import requests

# The API endpoint
url = "https://server.url/api/v8.7/"

session_cookies = {'teamscale-session-8080': 'username:key'}

project = 'project_name'

data = {}

# log file
log = open("log.txt", "w")


# simple method to return leaf node containing all methods of the provided file
def walk_tree(subtree, path):
    path_segments = path.split("/")
    current_path = ""

    for segment in path_segments:
        current_path += segment
        found = False

        # find correct sub-branch
        for child in subtree['children']:
            if child['uniformPath'] == current_path:
                subtree = child
                found = True
                break

        if not found:
            return "NA"

        current_path += "/"

    return subtree

# issue TGA export from Teamscale
with open('issues-teamscale-tga.json') as f:
    d = json.load(f)

    for idx, issue in enumerate(d):
        issueID = issue['Issue ID']

        # A GET request to the API
        response = requests.get(url + "projects/" + project + "/issues/" + issueID + "/affected-files",
                                cookies=session_cookies)

        if response.status_code != 200:
            log.write(issueID + " failed: +" + response.text)
            print(response.text)
            continue

        java = False
        js = False

        response_json = response.json()

        # check if ticket affects both java and js files
        for element in response_json:
            if js and java:
                break
            if element['uniformPath'].endswith(".java"):
                log.write(issueID + ": --- java file found: " + element['uniformPath'] + "\n")
                print(issueID + ": --- java file found: " + element['uniformPath'])
                java = True
            elif element['uniformPath'].endswith((".js", ".ts", ".tsx")):
                log.write(issueID + ": --- js file found: " + element['uniformPath'] + "\n")
                print(issueID + ": --- js file found: " + element['uniformPath'])
                js = True

        log.write(issueID + " has java + js: " + str((java and js)) + "\n")
        print(issueID + " has java + js: " + str((java and js)))

        # GET test-gap treemap with tga data
        treemap = requests.get(
            f"{url}projects/{project}/test-gaps/treemap?exclude-unchanged-methods=true&issue-id={issueID}&all"
            f"-partitions=true", cookies=session_cookies)

        if treemap.status_code != 200:
            log.write(issueID + " failed: +" + response.text)
            print(response.text)
            continue

        treemap_json = treemap.json()

        java_gap = False
        js_gap = False

        if 'children' in treemap_json['treemap']:

            for element in response_json:

                treemap_element = walk_tree(treemap_json['treemap'], element['uniformPath'])
                if treemap_element == 'NA':
                    continue

                # check if there is any test gap in a files method
                for method in treemap_element['children']:
                    if (method['state'] == 'UNTESTED_ADDITION' or method['state'] == 'UNTESTED_CHANGE') and element[
                        'uniformPath'].endswith(".java"):
                        log.write(issueID + ": --- java testgap found: " + element['uniformPath'] + ":" + method[
                            'methodName'] + "\n")
                        print(issueID + ": --- java testgap found: " + element['uniformPath'] + ":" + method[
                            'methodName'])
                        java_gap = True
                    elif (method['state'] == 'UNTESTED_ADDITION' or method['state'] == 'UNTESTED_CHANGE') and element[
                        'uniformPath'].endswith((".js", ".ts", ".tsx")):
                        log.write(issueID + ": --- js testgap found: " + element['uniformPath'] + ":" + method[
                            'methodName'] + "\n")
                        print(
                            issueID + ": --- js testgap found: " + element['uniformPath'] + ":" + method['methodName'])
                        js_gap = True
                if js_gap and java_gap:
                    break

        log.write(issueID + " has java + js test-gaps: " + str((java_gap and js_gap)) + "\n")
        log.write("------------------------ \n")
        log.write("------------------------ \n")
        print(issueID + " has java + js test-gaps: " + str((java_gap and js_gap)))
        print("Issue " + str(idx) + " of " + str(len(d)))

        # store test gap data
        data[issueID] = {'java': java, 'js': js, 'java_gap': java_gap, 'js_gap': js_gap}

with open("issue_data.json", "w") as result_file:
    json.dump(data, result_file)

log.close()

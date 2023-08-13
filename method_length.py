import json
import requests
import re

# The teamscale API endpoint
url = "https://cqse.teamscale.dev/api/v8.7/"

# session cookie, from a browser session used to make api calls
session_cookies = {'teamscale-session-8080': 'username:key'}

project = 'project-name'


# simple method to return all leaf nodes = methods of the treemap
def get_leaf_nodes(treemap):
    leafs = []

    def _get_leaf_nodes(node):
        if node is not None:
            if 'children' not in node:
                leafs.append(node)
            else:
                for n in node['children']:
                    _get_leaf_nodes(n)

    _get_leaf_nodes(treemap)
    return leafs


# get testgap-method data from <API endpoint>/projects/<projectName>/test-gaps.csv
# the data is structured as a map from <filename + methodName> to mathodData
with open("testgaps.csv") as fp:
    headers = next(fp).rstrip().split(';')
    testGaps_list = [dict(zip(headers, line.rstrip().split(';'))) for line in fp]
    testGaps_dict = {f"{entry['Uniform Path']}:{entry['Method Name']}": entry for entry in testGaps_list}

# mat from methods to test-gap line number
methods_with_testGaps = {}

# issue TGA data exported from teamscale (incudes issue with test-gap percentage)
with open('issues-teamscale-tga.json') as f:
    d = json.load(f)

for issue in d:
    issueID = issue['Issue ID']
    print(issueID)

    # GET test-gap treemap with tga data
    treemap = requests.get(
        f"{url}projects/{project}/test-gaps/treemap?exclude-unchanged-methods=true&issue-id={issueID}&all"
        f"-partitions=true", cookies=session_cookies)

    if treemap.status_code != 200:
        print(treemap.text)
        continue

    treemap_json = treemap.json()

    # skip emty treemaps
    if 'children' in treemap_json['treemap']:

        leaf_nodes = get_leaf_nodes(treemap_json['treemap'])
        for method in leaf_nodes:

            # check for testgaps in the javaScript/typeScript methods
            if (method['state'] == 'UNTESTED_ADDITION' or method['state'] == 'UNTESTED_CHANGE') and method[
                'uniformPath'].endswith((".js", ".ts", ".tsx")):

                method_path = f"{method['uniformPath']}:{method['methodName']}"

                try:
                    method_data = testGaps_dict[method_path]
                except:
                    continue
                method_region = method_data['Method Region Lines']

                # get method length from line numbers
                numbers = re.findall(r'\d+', method_region)

                method_length = int(numbers[1]) - int(numbers[0])
                if method_path not in methods_with_testGaps:
                    methods_with_testGaps[method_path] = method_length

# save method data
with open("method_length.json", "w") as result_file:
    json.dump(methods_with_testGaps, result_file)

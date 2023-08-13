# thesis_scripts
A collection of python scripts used in my thesis:

method_length.py:

Retrieves the method length from teamscale, using the provided list of issues and saves the aggregated results in method_length.json

method_length_analysis.py:

Uses the aggregated data from method_length.py and plots the length of methods in ascending order.

github_survey.py:

Retrieves data for 6000 Java github repositories and searches for key configuration files. Results are saved to github_analysis.json

github_analysis.py:

Aggregates the data from github_survey.py and prints the number of repositories for each category.

issue_survey.py:

Uses issues-teamscale-tga.json file exported from Teamscale and requests detailed TGA data, for each issue to find out whether a ticket includes Java and JavaScript files. And whether they include Java and JavaScript Test-Gaps. Results are saved in issue_data.json

issue_analysis.py:

Prints the number of combinations of issue metrics: {is java present}, {js present}, {has java_gap}, {has js_gap}. Issue data is read from issue_data.json, created by issue_survey.py.
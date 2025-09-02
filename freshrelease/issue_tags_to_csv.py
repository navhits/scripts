"""
List issues from Freshrelease and export the tags to CSV.
Requires Freshrelease SDK.
"""
import logging
import re
import csv
from freshrelease_sdk.Session import Session
from freshrelease_sdk.Instance import Instance
from freshrelease_sdk.Filter import Operator, FilterSet


FR_URL = "https://<freshrelease-url>"
FR_API_KEY = "<freshrelease-api-key>"

logging.basicConfig(level=logging.INFO)

session = Session(freshrelease_token=FR_API_KEY,
                  freshrelease_url=FR_URL, enable_cache=False)

instance = Instance(freshrelease_session=session)


filter_set = FilterSet(per_page=250, include={'tags'})

# Filter out issues with tags like this. For example: Coverity issues
filter_set.create_filter('tags', Operator.IS_IN, ['Coverity'])

repos = list()
# In case a specific pattern needs to be filtered then use regex
pattern = r"fresh.*\/.*" # Regex to match github repo in format <org>/<repo>
for page in instance.list_issues(filter_set=filter_set):
    for issue in page:
        for tag in issue.tags:
            if re.match(pattern, tag):
                entry = [tag, issue.key[0:issue.key.rindex("-")]]
                if entry not in repos:
                    repos+= [entry]

with open('repos.csv', mode='w', encoding='utf-8') as f:
    csv_writer = csv.writer(f, delimiter=',')
    csv_writer.writerow(['Repository', 'Freshrelease Project Key'])
    for repo in repos:
        csv_writer.writerow(repo)

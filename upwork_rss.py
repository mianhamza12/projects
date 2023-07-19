import feedparser
from bs4 import BeautifulSoup
import re

url = "https://www.upwork.com/ab/feed/jobs/rss?q=django&sort=recency&category2_uid=531770282580668421%2C531770282580668419%2C531770282580668418&paging=0%3B10&api_params=1&securityToken=744c05986f0656e00113dec6d4943ad992559d63b66ea25536c09a8861070e7ce51b72acd4e7034d45557e0eeb06d871f287562b9bc3023e97e6005a674b4b9c&userUid=1531232597027590144&orgUid=1531232597027590145"
feed = feedparser.parse(url)

# Iterate over the entries and extract information
for entry in feed.entries:
    title = entry.title
    print("Job_Title:", title)

    # Remove HTML tags from the summary
    summary_text = BeautifulSoup(entry.summary, "html.parser").get_text()
    print("Job_Description:", summary_text)

    # Here parse a value against Country
    match = re.search(r'Country: (.+)', summary_text)
    if match:
        country = match.group(1)
        print("Country:", country)
    else:
        None

    # Here parse a value against Skills
    match = re.search(r'Skills:(.+)', summary_text)
    if match:
        skills = match.group(1).strip()
        skills_list = [skill.strip() for skill in skills.split(',')]
        print("Skills:", skills_list)
    else:
        print("Skills: N/A")

    # Here parse a value against Category
    match = re.search(r'Category:(.+?)Skills', summary_text)
    if match:
        category = match.group(1).strip()
        print("Category:", category)
    else:
        print("N/A")
    # Here parse a value against Hourly range
    match = re.search(r'Hourly Range: \$([\d\.]+)-\$([\d\.]+)', summary_text)
    if match:
        minimum_range = match.group(1).strip()
        maximum_range = match.group(2).strip()
        print("Hourly_Range_Minimum:", minimum_range)
        print("Hourly_Range_Maximum:", maximum_range)
    else:
        None



    print("Job Link:", entry.link)
    print("Job Published Date:", entry.published)
    print("------------")


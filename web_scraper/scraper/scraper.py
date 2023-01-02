import bs4 as beautiful_soup
import requests

page = requests.get(
    "https://uk.indeed.com/jobs?q=&l=Berkhamsted%2C+Hertfordshire&from=searchOnHP&vjk=edc330f2dc5f7f73"
)

print(page.status_code)

from bs4 import BeautifulSoup
import requests
import re
import pandas as pd


urls =['https://github.com/basedosdados/pipelines/milestone/1',
'https://github.com/basedosdados/pipelines/milestone/2',
'https://github.com/basedosdados/website/milestone/2',
'https://github.com/basedosdados/pipelines/milestone/3'
]

titles=[]
due_dates=[]
progs=[]
objetivos=[]
dods=[]

for url in urls:
    response = requests.get(url)
    html=response.content
    soup = BeautifulSoup(html, 'html.parser')
    divs = soup.find_all("div", {"class": ["mb-3","mt-0"]})
    raw = re.sub(r'\n+',' ', divs[6].text).split('New issue')[1].strip()

    title = re.match(r'.*(?=Due)', raw).group().strip()
    due_date=re.findall(r'[A-Z][a-z]+\s+\d{1,2},\s+\d{4}', raw)[0].strip()
    progress=re.findall(r'\d+%', raw)[0].strip()

    titles.append(title)
    due_dates.append(due_date)
    progs.append(progress)

data = {
    "milestone":titles,
    "deadline":due_dates,
    'progress':progs
}

df=pd.DataFrame(data)

df.sort_values('progress', ascending=False, inplace=True)

print(df)

text=f'# Milestones Infra\n\n\n{df.to_markdown(index=False)}'


with open('README.md', 'w') as f:
    f.write(text)


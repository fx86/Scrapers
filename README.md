Bunch of scrapers written with scrapy.

Run like:

scrapy crawl imdb -o FILENAME.json


IMDb scraper results in malformed JSON. Following steps would be needed to clean it up into CSV format:
```
### remove first character "[" from file
sed -i ''  's/^.\{1\}//' FILENAME.json

# remove last character "]" from file
sed -i '$ s/.$//' FILENAME.json

# following code is in Python
temp = open(FILENAME.json).read()
temp = temp.split('\n')

df = []
for i, d in enumerate(temp):
    try:
        df.append(json.loads(temp[i].strip(',')))
    except Exception:
        print "Exception : ]["
        if '][' in d:
            df.extend(map(lambda v: json.loads(v.strip(',')), d.split('][')))

data = pd.concat([pd.DataFrame.from_dict(i, orient='index').T for i in df])
data = data.reset_index(drop=True)

data['rating'] = data['rating'].fillna(pd.np.NaN)
data['rating'] = data['rating'].replace('Awaiting enough ratings - click stars to rate', pd.np.NaN)
data['Votes'] = data['rating'].apply(lambda v: re.findall('[\d+\,]+ votes', v)[0] if isinstance(v, unicode) else 0)
data['rating'] = data['rating'].apply(lambda v: re.findall('[\d+\.]+', v)[0] if isinstance(v, unicode) else 0)
data.to_csv("one_lakh_movies.csv", index=False)```

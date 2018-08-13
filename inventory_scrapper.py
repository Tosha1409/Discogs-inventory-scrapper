import sys, discogs_client, csv
from discogs_client.exceptions import HTTPError

#settings and identification
csvfile='discogs.csv'
picturesfolder='photos/'
d = discogs_client.Client('ExampleApplication/0.1', user_token="put your tokken")
me = d.identity()

#requesting inventory
results = me.inventory

#making CSV file forming first line
writer = csv.writer(open(csvfile, 'w'), delimiter ='\t', quotechar=None)
writer.writerow(('artist', 'title', 'form', 'link', 'label', 'picture', 'picturelink', 'scondition', 'mcondition', 'price'))

#parsing all items "for sale"
for items in results:
	if items.status == "For Sale":
		#parsing artist 
		artist = ''
		for artists in items.release.artists: 
			if artist=='': artist = (artists.name.encode('ascii','ignore')).decode()
			else: artist = artist +'/'+ (artists.name.encode('ascii','ignore')).decode()
		#parsing release format
		try: format = items.release.formats[0]['name']+' '+' '.join(items.release.formats[0]['descriptions'])+' '+items.release.formats[0]['text']+'!!!'
		except: 
			try: format = items.release.formats[0]['name']+' '+' '.join(items.release.formats[0]['descriptions'])
			except: format = items.release.formats[0]['name']
		link = 'https://www.discogs.com/sell/item/'+str(items.id)
		#parsing label
		label=''
		for rawdata in items.release.labels: label=label+str(rawdata.name)+'/'
		label=label[:-1]
		#parsing and downloading first image
		try:
			image = items.release.images[0]['uri']
			content, resp = d._fetcher.fetch(None, 'GET', image, headers={'User-agent': d.user_agent})
			picture=(image.split('/')[-1]).split('.')[0]+'.jpg' 
			with open(picturesfolder+picture, 'wb') as fh:
				fh.write(content)
		except: image =''
		#parsing to csv and report to screen
		writer.writerow(
			((str(artist).encode('ascii','ignore')).decode(), (str(items.release.title).encode('ascii','ignore')).decode(), (str(format).encode('ascii','ignore')).decode(), link, (str(label).encode('ascii','ignore')).decode(), picture, image, items.sleeve_condition, items.condition, str(items.price.value))
			)
		print ('Parsing -'+(str(artist).encode('ascii','ignore')).decode()+' '+(str(items.release.title).encode('ascii','ignore')).decode())
print ('Finished!')
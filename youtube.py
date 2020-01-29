from flask import Flask,render_template,request
import requests

app=Flask(__name__)
YOUTUBE_API_KEY='AIzaSyB-SdpK9_G8sWkIWUAFVtIu0cESw5cyPFA'


@app.route("/",methods=['GET','POST'])
def index():
	search_url='https://www.googleapis.com/youtube/v3/search'
	video_url='https://www.googleapis.com/youtube/v3/videos'
	videos=[]

	try:
		if request.method=='POST':
			search_params={
			'key':'AIzaSyB-SdpK9_G8sWkIWUAFVtIu0cESw5cyPFA',
			'q':request.form.get('query'),
			'part':'snippet',
			'maxResults':10,
			'type':'video'}

			r=requests.get(search_url,params=search_params)
			results=r.json()['items']
			video_ids=[]
			
			for result in results:
				video_ids.append(result['id']['videoId'])

			video_params={
			'key':'AIzaSyB-SdpK9_G8sWkIWUAFVtIu0cESw5cyPFA',
			'id':','.join(video_ids),
			'part':'snippet,contentDetails',
			'maxResults':10
			}
			r=requests.get(video_url,params=video_params)
			results=r.json()['items']

			
			for result in results:
				video_data={
				'id':result['id'],
				'url':f'https://www.youtube.com/watch?v={result["id"]}',
				'thumbnail':result['snippet']['thumbnails']['high']['url'],
				'duration':result['contentDetails']['duration'],
				'title':result['snippet']['title']
				}
				videos.append(video_data)

				if request.form.get('submit')=='lucky':
					return f"https://www.youtube.com/watch?v={results[0]}" 
		return render_template("index.html",videos=videos,x=1)
	except:
		videos=[]
		return render_template("index.html",videos=videos,x=0)


if __name__ == '__main__': 
	app.run(debug=True)
	
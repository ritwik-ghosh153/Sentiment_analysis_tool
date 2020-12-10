from tkinter import *
from tkinter import messagebox
import json
from tkinter.filedialog import askopenfilename
import tweepy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

file = open('credentials.json')
creds = json.load(file)
file.close()

def sentiment_scores(sentence):
  
    # Create a SentimentIntensityAnalyzer object.
    sid_obj = SentimentIntensityAnalyzer()
  
    # polarity_scores method of SentimentIntensityAnalyzer
    # oject gives a sentiment dictionary.
    # which contains pos, neg, neu, and compound scores.
    sentiment_dict = sid_obj.polarity_scores(sentence)
    
    result={}
    
    result['neg_rating']=str('{0:.3g}'.format(sentiment_dict['neg']*100))
    result['neu_rating']=str('{0:.3g}'.format(sentiment_dict['neu']*100))
    result['pos_rating']=str('{0:.3g}'.format(sentiment_dict['pos']*100))
    result['comp_rating']=str('{0:.3g}'.format(sentiment_dict['compound']*100))
  
  
    # decide sentiment as positive, negative and neutral
    if sentiment_dict['compound'] >= 0.05 :
        result['res']="Positive"
  
    elif sentiment_dict['compound'] <= - 0.05 :
        result['res']="Negative"
  
    else :
        result['res']="Neutral"
    
    if sentiment_dict['compound']< limit.get()/100:
        result['verd']="The sentence is not recommended to be posted"
        
    else:
        result['verd']="The sentence is recommended to be posted"
    return result

def remove_media():
	media_val.set("")
	hasMedia.set("False")
	media_path.set("")

def fetch_media():
	formats=['jpg','jpeg','png','gif','webp']
	media_path.set(askopenfilename())
	filename=media_path.get().split('/')[-1]
	if not filename.isspace() and len(filename) != 0:
		if filename.split(".")[-1].lower() in formats:
			media_val.set("Media: "+filename)
			hasMedia.set("True")
		else:
			messagebox.showwarning("Warning", "Unsupported media format! Must be JPG, PNG, GIF or WEBP", parent=window)
			media_path.set("")
			media_val.set("")
			hasMedia.set("False")
	else:
		media_path.set("")
		media_val.set("")
		hasMedia.set("False")

def analyse():
		
		sentence=text.get("1.0",END)
		res=(sentiment_scores(sentence))
		
		if not sentence.isspace() and len(sentence) != 0:
		
			pos_val.set(res['pos_rating']+"%")

			neu_val.set(res['neu_rating']+"%")

			neg_val.set(res['neg_rating']+"%")

			comp_val.set(res['comp_rating']+"%")

			res_val.set("The text was overall rated as "+res['res']+".")
			
			verd_val.set(res['verd'])

			hexcode= '#%02x%02x%02x' % (int(float(res['neg_rating'])/100*255),int(float(res['pos_rating'])/100*255),int(float(res['neu_rating'])/100*255))
			
			if hexcode == "#000000":
				hexcode = "#ffffff"
			col_label.configure(bg=hexcode)
		
		else:
			pos_val.set("")

			neu_val.set("")

			neg_val.set("")

			comp_val.set("")

			res_val.set("")
			
			verd_val.set("")
			
			col_label.configure(bg='#ffffff')


def post():
	sentence=text.get("1.0",END)
	if len(sentence) > 280:
		messagebox.showwarning("Warning", "Text must be up to 280 characters to post on Twitter!", parent=window)
	elif sentence.isspace() or len(sentence) == 0:
		messagebox.showwarning("Warning", "No message to post!", parent=window)
	else:
		choice=messagebox.askquestion("Asking confirmation", "Are you sure you want to post this on Twitter?", parent=window)
		if choice == "yes":
			try:
				consumer_key = creds["consumer_key"]
				consumer_secret =creds["consumer_secret"]
				access_token =creds["access_token"]
				access_token_secret =creds["access_token_secret"]
				# authentication of consumer key and secret
				auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
				# Authentication of access token and secret
				auth.set_access_token(access_token, access_token_secret)
				api = tweepy.API(auth)
				if hasMedia.get()=="True":
					api.update_with_media(media_path.get(), sentence)

				else:
					api.update_status(status=sentence)

				text.delete(1.0, END)
				pos_val.set("")
				neu_val.set("")
				neg_val.set("")
				comp_val.set("")
				res_val.set("")
				col_label.configure(bg="#ffffff")
				verd_val.set("")
				media_val.set("")
				hasMedia.set("False")
				media_path.set("")

			except:
				messagebox.showerror("showerror", "Something went wrong!", parent=window)
			else:
				messagebox.showinfo("Info", "Successfully posted on Twitter!", parent=window)


window=Tk()
window.title("Sentiment Analyser Tool")
window.resizable(False,False)

content=StringVar()

#text area
text=Text(window, borderwidth = 3, relief=RAISED, wrap=WORD)
text.grid(row=0, column=0, columnspan=2, rowspan=15, padx=20)

#analyse button
b1=Button(window, text="Analyse", command=analyse)
b1.grid(row=20, column=0, padx=20, pady=10)

#posting on twitter button
b2=Button(window, text="Post on Twitter", command=post)
b2.grid(row=20, column=1)

#add media button
add_media=Button(window, text="Add media", command=fetch_media)
add_media.grid(row=20, column=4)

#remove media button
rm_media=Button(window, text="Remove media", command=remove_media)
rm_media.grid(row=20, column=5)


#positive colour and score labels
pos_val=StringVar()
label=Label(window, height=1, width=2, relief=RAISED,bg='green')
label.grid(row=2, column=3, padx=15)
label=Label(window, text="Positive:", height=1)
label.grid(row=2, column=4)
pos_label=Label(window, textvariable=pos_val, height=1, width=5, relief=RAISED)
pos_label.grid(row=2, column=5)

#neutral colour and score labels
neu_val=StringVar()
label=Label(window, height=1, width=2, relief=RAISED,bg='blue')
label.grid(row=3, column=3)
label=Label(window, text="Neutral:", height=1)
label.grid(row=3, column=4)
neu_label=Label(window, textvariable=neu_val, height=1, width=5, relief=RAISED)
neu_label.grid(row=3, column=5)

#negative colour and score labels
neg_val=StringVar()
label=Label(window, height=1, width=2, relief=RAISED,bg='red')
label.grid(row=4, column=3)
label=Label(window, text="Negative:", height=1)
label.grid(row=4, column=4)
neg_label=Label(window, textvariable=neg_val, height=1, width=5, relief=RAISED)
neg_label.grid(row=4, column=5)

#compound score label
col=StringVar()
if col.get()==None or col.get()=="":
    col.set("#ffffff")
comp_val=StringVar()
label=Label(window, text="Compound:", height=1)
label.grid(row=5, column=4)
comp_label=Label(window, textvariable=comp_val, height=1, width=5, relief=RAISED)
comp_label.grid(row=5, column=5)

#Sentiment visualisation colour
label=Label(window, text="Sentiment\nvisualisation:", height=2)
label.grid(row=7, column=4)
col_label=Label(window, height=2, width=5, relief=RAISED,bg=col.get())
col_label.grid(row=7, column=5)

#result label
res_val=StringVar()
res_label=Label(window, textvariable=res_val, height=2, width=35)
res_label.grid(row=9, column=4, columnspan=2)

#limit slider
limit=DoubleVar()
limit.set(0)
label=Label(window, text="Set sentiment\nscore limit:", height=2)
label.grid(row=11, column=4,)
lim_scale=Scale(window, variable = limit, from_ = -100, to = 100, orient = HORIZONTAL, sliderlength=10)
lim_scale.grid(row=11, column=5)

#verdict label
verd_val=StringVar()
verd_label=Label(window, textvariable=verd_val, height=2, width=40)
verd_label.grid(row=13, column=4, columnspan=2)


hasMedia = StringVar()
hasMedia.set("False")
media_path=StringVar()
media_path.set("")
#media path label
media_val=StringVar()
media_label=Label(window, textvariable=media_val, height=2, width=40, wraplength = 300)
media_label.grid(row=14, column=4, columnspan=2)

window.mainloop()

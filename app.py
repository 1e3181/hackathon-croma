import os
import sys
import markdown
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup


def twebsitetotext(s):
    r = requests.get(s)
    soup = BeautifulSoup(r.text, "html.parser")
    return (soup.text)
def downloadpdf(s, i):
    url = s
    r = requests.get(url, stream=True)
    with open(f'temp{i}.pdf', 'wb') as fd:
        for chunk in r.iter_content(2000):
            fd.write(chunk)
def write(d):
    with open('out2.md', 'a') as f:
        f.write(d)
        f.write("\n")
    f.close()

text = []
genai.configure(api_key='AIzaSyD7SqpaUtvq05aV58R1lyA5-QsARwWdkHk')
model = genai.GenerativeModel("gemini-1.5-flash")



f = open('index.html', 'w')



chat = model.start_chat()
from bs4 import BeautifulSoup
import requests

search = 'latest newws about reliance digital'
url = 'https://www.google.com/search'

headers = {
	'Accept' : '*/*',
	'Accept-Language': 'en-US,en;q=0.5',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82',
}
parameters = {'q': search}

content = requests.get(url, headers = headers, params = parameters).text
soup = BeautifulSoup(content, 'html.parser')

search = soup.find(id = 'search')
first_link = search.find('a')
print("Getting news articles....")
t = twebsitetotext(first_link['href'])
t2 = twebsitetotext('https://www.livemint.com/topic/reliance-digital')
response = chat.send_message(f"Using this source: {t} and {t2}, Generate a summary on recent activities of reliance digitals")
n1 = response.text  

content = requests.get("https://www.google.com/search?q=bajaj+electricals+news+today", headers = headers, params = parameters).text
soup = BeautifulSoup(content, 'html.parser')

t = twebsitetotext(first_link['href'])
t2 = twebsitetotext('https://economictimes.indiatimes.com/bajaj-electricals-ltd/stocksupdate/companyid-13978.cms')
response = chat.send_message(f"Using this source: {t} and {t2}, Generate a summary on recent activities of bajaj electricals")
n2 = response.text


t = twebsitetotext("https://www.livemint.com/market/market-stats/stocks-aditya-vision-share-price-nse-bse-s0000805")
t2 = twebsitetotext('https://economictimes.indiatimes.com/markets/stocks/news/ashish-kacholia-backed-aditya-vision-announces-record-date-for-110-stock-split/articleshow/112498084.cms')
response = chat.send_message(f"Using this source: {t} and {t2}, Generate a summary on recent activities of adithya vision")
n3 = response.text

with open('index.html', 'a') as f:
    f.write('<link rel="stylesheet" href="style.css">')
    f.write("<h1>Reliance digital</h1>")
    f.write(markdown.markdown(n1, extensions=['markdown.extensions.tables']))
    f.write("<h1>Bajaj electronics</h1>")
    f.write(markdown.markdown(n2, extensions=['markdown.extensions.tables']))
    f.write("<h1>Adithya vision</h1>")
    try:
        f.write(markdown.markdown(n3, extensions=['markdown.extensions.tables']))
    except:
        pass
    f.close()
print("Done")

print("Webscraping...")
for i in open('links.txt', 'r').readlines():
    text.append(twebsitetotext(i))

text.append(twebsitetotext('https://economictimes.indiatimes.com/markets/expert-view/expecting-one-of-the-best-years-due-to-strong-consumer-spending-nilesh-gupta-vijay-sales/articleshow/110869447.cms?from=mdr'))
print("done")

print("Generating the context(this might take a while)..")
response = chat.send_message("USE THIS AS CONTEXT FOR THE REMAINDER OF THE CHAT:Croma is India's first and most trusted large format specialist retail store focused on Electronic and Appliances. Founded in 2006, Croma caters to everyone’s multi-brand digital gadgets and home electronic needs. Croma offers a world-class ambiance and a seamless omnichannel experience to shop in-store, online at www.croma.com,and through the Tata Neu App. Croma is looking to understand its competitive landscape better, especially with omnichannel electronics retailers in the organised sector. One of the ways of doing so is through competitive intelligence scanning through data in the public domain. There is potential to enhance the coverage, depth of insights and time taken to cull the insights through recent advances in Generative AI.")
response = chat.send_message("Croma has competitors like Reliance digital,Vijay sales,Aditya vision,Poojara,Bajaj electronics and many others")

for i in text:
    chat.send_message(f"use the following context along with the previous one: {i}")

for  i in range(2):
    pdf = genai.upload_file(f"temp{i+1}.pdf")
    model.generate_content(["use the following context and remember it along with the previous one: ", pdf])

print("done")

# Channels
print("Looking up for different buisness channels")
response = chat.send_message("What are the channels in which croma's competitors sell products(online, store, B2B).")
with open("index.html", "a") as f:
    f.write(markdown.markdown(response.text[response.text.index('*'):], extensions=['markdown.extensions.tables']))

for _ in range(2):
    chat.history.pop()
print("done")

print("Looking up for product potfolio")
response = chat.send_message("Give a brief summary on the Product portfolio(categories, category mix, assortment size and type, private labels, etc.) for each of the competitors along with 3 extra competitors not mentioned here, remove any extra information that is not relevant to the content. Do not given any note at the end")
for _ in range(2):
    chat.history.pop()
with open("index.html", "a") as f:
    f.write(markdown.markdown(response.text[response.text.index('*'):], extensions=['markdown.extensions.tables']))
print("Done")

print("Lokking up for marketing strategies online")
response = chat.send_message("Differentiate the Marketing strategy and media presence between croma and its competitors")
with open("index.html", "a") as f:
    f.write(markdown.markdown(response.text[response.text.index('*'):], extensions=['markdown.extensions.tables']))
for _ in range(2):
    chat.history.pop()
print("Done")

print("Looking up for financing data..")
response = chat.send_message("Discuss the affordibility offerings for croma and its competitors like financing,exchange etc... elaborately, in bulletins(do not mention the word bulletin)")
with open("index.html", "a") as f:
    f.write(markdown.markdown(response.text[response.text.index('*'):], extensions=['markdown.extensions.tables']))
for _ in range(2):
    chat.history.pop()
print("Done")

print("Looking up for delivery data..")
v1 = twebsitetotext('https://www.croma.com/lp-express-delivery ')
v2 = twebsitetotext('https://www.croma.com/shipping-information ')
v3 = twebsitetotext('https://www.reliancedigital.in/content/shipping-and-delivery-policy')
v4 = twebsitetotext('https://www.bajajelectronics.com/delivery-of-policy')
v5 = twebsitetotext('https://www.poojaratele.com/shipping-policy/')
chat.send_message(f"consider this data for the next quesiton for croma : {v1} {v2}")
chat.send_message(f"consider this data for the next quesiton for reliance : {v3} {v4}")
chat.send_message(f"consider this data for the next quesiton for bajaj : {v4}")
chat.send_message(f"consider this data for the next quesiton for pooja : {v5}")


response = chat.send_message("compare the delivery promises of croma with reliance, vijay and bajaj from given data. do not ask question bck and do not reply")
with open("index.html", "a") as f:
    try:
        f.write("<h2>Delivery promises</h2>")
        f.write(markdown.markdown(response.text[response.text.index('*'):], extensions=['markdown.extensions.tables']))
    except:
        f.write("<h2>Delivery promises</h2>")
        f.write(markdown.markdown(response.text, extensions=['markdown.extensions.tables']))
for _ in range(10):
    chat.history.pop()
print("done")

print("Calculating the number of stores throughout the states(this might take a while)..")
r = requests.get('https://www.sbicard.com/sbi-card-en/assets/docs/html/personal/offers/croma-store.html')
chat.send_message(f'Use this html page and answer the following questions: {r.text}')
response = chat.send_message("display the number of croma stores state wise in a table, heading is 'number of croma stores in major cities among the states in India' and print the heading with the table nothing else")
with open("index.html", "a") as f:
    try:
        f.write(markdown.markdown(response.text[response.text.index('*'):], extensions=['markdown.extensions.tables']))
    except:
        f.write(markdown.markdown(response.text, extensions=['markdown.extensions.tables']))

r = requests.get('https://www.sbicard.com/sbi-card-en/assets/docs/html/personal/offers/reliance-digital-list.html')
chat.send_message(f'Use this html page and answer the following questions: {r.text}')
response = chat.send_message("display the number of reliance stores state wise in a table, heading is 'number of reliance stores in major cities among the states in India' and print the heading with the table nothing else")
for _ in range(4):
    chat.history.pop()
with open("index.html", "a") as f:
    f.write(markdown.markdown(response.text[response.text.index('*'):], extensions=['markdown.extensions.tables']))

downloadpdf('https://www.sbicard.com/sbi-card-en/assets/media/images/personal/offers/categories/shopping/bajaj-electronics/store-list-bajaj-electronics.pdf', 3)
sample_pdf = genai.upload_file("temp3.pdf")
response = model.generate_content(["Using the address, find in which state the store is located and Display the number of bajaj electronics stores state wise in a table.Set the title to 'Number of bajaj electronics stores in major cities among the cities in india'.Include nothing else", sample_pdf])
with open("index.html", "a") as f:
    f.write(markdown.markdown(response.text[response.text.index('*'):], extensions=['markdown.extensions.tables']))

for _ in range(2):
    chat.history.pop()
print("Done")

print("Looking up sizes of the stores")
response = chat.send_message("Discuss size of stores with area in sqft in tabular form with approximate store size along with not mentioned competitors")
for _ in range(2):
    chat.history.pop()
with open("index.html", "a") as f:
    f.write(markdown.markdown(response.text[response.text.index('*'):], extensions=['markdown.extensions.tables']))
print("Done")

print("Checking up future plans..")
response = chat.send_message("describe the future plans of the afforementioned companies(along with similar not mentioned competitors) summarized summary summary")
with open("index.html", "a") as f:
    f.write(markdown.markdown(response.text[response.text.index('*'):], extensions=['markdown.extensions.tables']))
for _ in range(2):
    chat.history.pop()
print("Done")

print("Calculating the amount of people working")
response = chat.send_message("discuss the approximate amount of people working in the fornt end and back end of each of these companies(provide approximate numbers of people per store) with croma")
with open("index.html", "a") as f:
    f.write(markdown.markdown(response.text[response.text.index('*'):], extensions=['markdown.extensions.tables']))
for i in range(2*1):    
    chat.history.pop()
print("Done")

print("Looking up for reviews online...")
r1 = twebsitetotext('https://www.justdial.com/Chennai/Reliance-Digital-Opposite-Muneeswaran-Temple-Ponnamallee-Kattupakkam/044PXX44-XX44-160809105526-X2N5_BZDET/reviews')
r2 = twebsitetotext('https://www.justdial.com/Vellore/Reliance-Digital-Opposite-Aascars-Cinemas-Katpadi/9999P8252-8252-160128144427-V8Y7_BZDET/reviews')
r3 = twebsitetotext('https://www.justdial.com/Kolkata/Croma-Marriott-Fairfield-Rajarhat-New-Town-Action-Area-1/033PXX33-XX33-200117151243-L3I4_BZDET/reviews')
r4 = twebsitetotext('https://www.justdial.com/Chennai/Croma-Opposite-Joy-Alukkas-and-Vasanth-Co-T-Nagar/044PXX44-XX44-091013162123-T5I1_BZDET?trkid=&term=&ncatid=10148025&area=&search=Popular%20Croma%20in%20Chennai&mncatname=Croma&abd_btn=&abd_heading=&bd=1&')
r5 = twebsitetotext('https://www.justdial.com/Delhi/Vijay-Sales-Near-3C-Cinema-Central-Market-Lajpat-Nagar-2/011PXX11-XX11-100302100451-F8D8_BZDET/reviews')
print("Processing reviews")


chat.send_message(f"Consider the following two data for customer reviews for croma {r3} {r4}")
chat.send_message(f"Consider the following two data for customer reviews for relience digital:{r1} and {r2}")
chat.send_message(f"Condider the following data for vijay sales: {r5}")
__import__('time').sleep(5)


response = chat.send_message("Compare the customer reviews from given data and return how is the customer feedback between croma and competitors. tabulate the result. Avoid giving any response messages at the start and the end.Give possible imporvements for croma")

for i in range(2*1): 
    chat.history.pop()
with open("index.html", "a") as f:
    f.write(markdown.markdown(response.text[response.text.index('*'):], extensions=['markdown.extensions.tables']))
print("done")
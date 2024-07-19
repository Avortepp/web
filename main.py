from flask import Flask, request, render_template, jsonify
import requests
from bs4 import BeautifulSoup
import csv

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    url = f'https://www.google.com/search?q={query}'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    results = []
    for g in soup.find_all('div', class_='tF2Cxc'):
        title_tag = g.find('h3')
        link_tag = g.find('a')
        description_tag = g.find('div', class_='IsZvec')

        title = title_tag.text if title_tag else 'No title'
        link = link_tag['href'] if link_tag else 'No link'
        description = description_tag.text if description_tag else 'No description'

        results.append({'title': title, 'link': link, 'description': description})

    save_results_to_csv(results, 'results.csv')

    return render_template('results.html', results=results)

def save_results_to_csv(results, filename):
    if results:
        keys = results[0].keys()
        with open(filename, 'w', newline='', encoding='utf-8') as output_file:
            dict_writer = csv.DictWriter(output_file, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(results)

if __name__ == '__main__':
    app.run(debug=True)
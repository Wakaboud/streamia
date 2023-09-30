from django.shortcuts import render
from django.http import HttpResponseRedirect
import openai
import re
import requests

# Fonction pour récupérer l'affiche d'un film en utilisant l'API TMDB
def get_movie_poster(movie_title):
    # Remplacez "YOUR_API_KEY" par votre propre clé API TMDB.
    api_key = "951a01b4acb30a8ec7c4ce4cb6f87911"
    base_url = f"https://api.themoviedb.org/3/search/movie"
    
    # Paramètres de la requête
    params = {
        "api_key": api_key,
        "query": movie_title
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code == 200 and data["total_results"] > 0:
            # Obtenez l'ID du premier film de la réponse
            movie_id = data["results"][0]["id"]

            # Obtenez les détails du film à partir de son ID
            details_url = f"https://api.themoviedb.org/3/movie/{movie_id}"
            params["append_to_response"] = "images"
            response = requests.get(details_url, params=params)
            details_data = response.json()

            if response.status_code == 200:
                poster_path = details_data["poster_path"]
                base_image_url = "https://image.tmdb.org/t/p/original/"
                poster_url = base_image_url + poster_path
                return poster_url
            else:
                return "Aucun résultat trouvé pour ce film."

    except Exception as e:
        return str(e)

# Configurez votre clé API OpenAI ici
openai.api_key = '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'

def recommend_movies(request):
    if request.method == 'POST':
        prompt = request.POST['prompt']
        
        # Appel à l'API OpenAI pour générer des recommandations de films en fonction du prompt
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Utilisez le modèle GPT-3.5 Turbo
            messages=[
                {"role": "system", "content": 
                 """
                 Vous êtes un super assistant qui recommande des films, des séries et des animes. 
                 Vous devez recommander 5 œuvres similaires à celles mentionnées dans le message avec une description. 
                 Les recommandations doivent suivre le même format que l'exemple suivant : 
                 1. Battle Royale - Dans un futur dystopique, un groupe d'adolescents est contraint de participer à un jeu mortel où ils doivent se battre à mort jusqu'à ce qu'il n'en reste plus qu'un. Ce thriller japonais intense est rempli de suspense, d'action et de dilemmes moraux.

                 """
                 },
                {"role": "user", "content": prompt},
            ],
        )

        # Récupérez la réponse générée par l'API
        recommended_movies = response.choices[0].message["content"]
        print(recommended_movies)

        lines = recommended_movies.split('\n')

# Créez un dictionnaire pour stocker les titres et les descriptions
        films = {}
        recommended_movies = []
        # Parcourez chaque ligne et extrayez les informations
        for line in lines:
            line = line.strip()
            if line:
                match = re.match(r'(\d+)\.\s+(.*?)\s+-\s+(.*)', line)
                if match:
                    titre = match.group(2)
                    description = match.group(3)

                    # Effectuez une requête à l'API TMDb pour rechercher le film par titre
                    print(titre)
                    poster_url = get_movie_poster(titre)

                    # Ajoutez des informations complémentaires ici
                    films = {
                        'titre': titre,
                        'description': description,
                        'affiche': poster_url,  # Remplacez par l'URL réelle de l'affiche
                    }
                    recommended_movies.append(films)

        # Affichez le dictionnaire résultant
        print(recommended_movies)
        # Passez les données nettoyées à la page de résultats
        if recommended_movies:
            return render(request, 'watchia/results.html', {'recommended_movies': recommended_movies})
        else:
            return render(request, 'watchia/noresults.html')
    return render(request, 'watchia/index.html')
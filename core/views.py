from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
# Para inicio de sesion con Google y Facebook
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from dj_rest_auth.serializers import JWTSerializer

# Create your views here.
@api_view(["GET"])
@permission_classes([IsAuthenticated])  # 🔥 Protege la vista con autenticación
def auth_status(request):
    user = request.user
    groups = list(user.groups.values_list("name", flat=True))  # Obtiene los nombres de los grupos
    
    return Response({
        "isAuthenticated": True,
        "username": user.username,
        "groups": groups,  # Devuelve los grupos
    })

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    serializer_class = JWTSerializer  # Para usar JWT

class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
    serializer_class = JWTSerializer  # Para usar JWT

####################################################################################################
##################################### Spotify API ##################################################
####################################################################################################
import requests
from django.core.cache import cache
from django.conf import settings

def get_spotify_token():
    # Intentar obtener el token desde la caché
    token = cache.get("spotify_token")
    if token:
        return token

    url = "https://accounts.spotify.com/api/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {"grant_type": "client_credentials"}
    
    try:
        response = requests.post(url, headers=headers, data=data, auth=(settings.SPOTIFY_CLIENT_ID, settings.SPOTIFY_CLIENT_SECRET))
        response.raise_for_status()
        token = response.json().get("access_token")
        # Cachear el token (por ejemplo, por 3600 segundos)
        cache.set("spotify_token", token, timeout=3600)
        return token
    except requests.RequestException as e:
        # Loguear el error o manejarlo de forma adecuada
        print("Error al obtener el token de Spotify:", e)
        return None

import random
from django.http import JsonResponse, HttpResponseServerError

import random
import requests
from django.http import JsonResponse, HttpResponseServerError

def get_popular_shows(request):
    token = get_spotify_token()
    print("TOKEN ->", token)
    if not token:
        return HttpResponseServerError("No se pudo obtener el token de Spotify.")

    headers = {"Authorization": f"Bearer {token}"}
    playlist_id = "6WoGUl6bGHmCDpW9OxfYZK"  # Reemplaza con el ID real de la playlist
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        playlist_data = response.json()
        
        
        # Verificar si la playlist tiene tracks
        if 'tracks' in playlist_data and 'items' in playlist_data['tracks']:
            tracks = playlist_data['tracks']['items']
            print("Total de tracks en la playlist:", len(tracks))
            
            # Si hay menos de 3 canciones, devolver todas; sino, seleccionar 3 al azar
            selected_tracks = tracks if len(tracks) < 3 else random.sample(tracks, 3)

            
            # Extraer la información relevante de cada track
            result = {
                "tracks": [
                    {
                        "name": track['track']['name'],
                        "artist": ", ".join([artist['name'] for artist in track['track']['artists']]),
                        "album": track['track']['album']['name'],
                        "image_url": track['track']['album']['images'][0]['url'] if track['track']['album']['images'] else None
                    }
                    for track in selected_tracks
                ]
            }
            return JsonResponse(result)
        else:
            print("No se encontraron tracks en la playlist")
            return HttpResponseServerError("No se encontraron tracks en la playlist.")
            
    except requests.RequestException as e:
        print("Error al obtener los tracks de Spotify:", e)
        return HttpResponseServerError("Error al obtener los datos de Spotify.")
    
####################################################################################################
##################################### NEW API ##################################################
####################################################################################################

@api_view(['GET'])
def get_news(request):
    # Configura la URL y los parámetros de la petición a NewsAPI
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "country": "us",      # Noticias de Argentina
        "apiKey": settings.NEWS_API_KEY
    }
    
    # Realiza la petición a NewsAPI
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        # Opcional: procesa los datos para devolver solo la información necesaria
        articles = data.get("articles", [])
        # Por ejemplo, extraer solo algunos campos:
        processed_articles = [
            {
                "title": article.get("title"),
                "description": article.get("description"),
                "url": article.get("url"),
                "urlToImage": article.get("urlToImage"),
                "source": article.get("source", {}).get("name")
            }
            for article in articles
        ]
        return Response({"articles": processed_articles})
    else:
        return Response({"error": "Error al obtener las noticias"}, status=response.status_code)
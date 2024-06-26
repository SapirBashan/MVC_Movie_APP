# TaskModel.py
import requests

class TodoModel:
    def __init__(self):
        pass
    
    #post
    def addMovie(self, movie_data):
        formatted_data = {
            "title": movie_data['title'],
            "year": movie_data['year'],
            "imdbID": movie_data['imdbID'],
            "rated": movie_data['rated'],
            "type": movie_data['type'],
            "poster": movie_data['poster'],
            "plot": movie_data['plot'],
            "imdbRating": movie_data['imdbRating']
        }
        #verify=False is used to ignore the SSL certificate verification
        #the SSL certificate verification is a mechinisam that allows the client to verify the server's identity
        #the server sends the client a certificate to verify its identity
        #the client checks the certificate against a list of trusted certificates
        #if the certificate is trusted, the client sends a message to the server
        response = requests.post(f'https://localhost:7276/api/MovieValue', json=formatted_data, verify=False)
        return response.status_code == 201  # Check for the correct status code for creation

    #delete
    def removeMovie(self, movie_name):
        response = requests.delete(f'https://localhost:7276/api/MovieValue/{movie_name}', verify=False)
        return response.status_code == 200

    #fetch from API
    def fetchMovieData(self, movie_name):
        response = requests.get(f'https://localhost:7276/Omdb/{movie_name}', verify=False)
        if response.status_code == 200:
            return response.json()
        else:
            return None
        
    #get /Get All
    def GetAllMovies(self):
        response = requests.get(f'https://localhost:7276/api/MovieValue', verify=False)
        if response.status_code == 200:
            return response.json()
        else:
            return None
        
    #Get /Get by Title
    def GetMovieByTitle(self, movie_name):
        response = requests.get(f'https://localhost:7276/api/MovieValue/{movie_name}', verify=False)
        if response.status_code == 200:
            return response.json()
        else:
            return None
        
    #Get /Get the movie recommendation based on the movie name from the API
    #this is the API call for the Chat GPT-3-Ultra - https://localhost:7276/api/movieRecommendation?question={movie_name}
    #this is the API call for the Chat GPT-Devincie - https://localhost:7276/GetMovieSuggestions?movies={movie_name}
    def GetMovieRecommendation(self, ModelName, movie_Title):
        if(ModelName == "GPT-3-Ultra"):
            response = requests.get(f'https://localhost:7276/api/movieRecommendation?question={movie_Title}', verify=False)
            if response.status_code == 200:
                if response.text == "":
                    return "No movie recommendation found"
                return response.text
            else:
                return None
        elif(ModelName == "GPT-Devincie"):
            response = requests.get(f'https://localhost:7276/GetMovieSuggestions?movies={movie_Title}', verify=False)
            if response.status_code == 200:
                if response.text == "":
                    return "No movie recommendation found"
                return response.text
            else:
                return None
        else:
            return None
        
    # PUT
    def updateComment(self, title, comment,movie_data):
        url = f'https://localhost:7276/api/MovieValue?title={title}'
        headers = {
            'accept': '*/*',
            'Content-Type': 'application/json'
        }
        data = f'"{comment}"'
        response = requests.put(url, headers=headers, data=data, verify=False)
        return response.status_code == 200  # Check for the correct status code for successful update


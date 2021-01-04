from flask import Flask, render_template, request
from requests_oauthlib import OAuth1Session
import os

def create_app():
    app = Flask(__name__)
    twitter_latest_tweets_url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
    # get credentials for authorization from .env file
    oauth = OAuth1Session(os.environ["CONSUMER_API_KEY"],
                        client_secret=os.environ["CONSUMER_API_SECRET_KEY"],
                        resource_owner_key=os.environ["ACCESS_TOKEN"],
                        resource_owner_secret=os.environ["ACCESS_TOKEN_SECRET"],
                        signature_type="auth_header")
                        
    @app.route("/", methods=["POST", "GET"])
    def index():
        # reset variables
        username = ""
        error_message = None
        latest_tweets = None
        if request.method == "POST":
            username = request.form["username"]
            # get latest tweets
            tweets_response = getLatestTweets(username)
            if isinstance(tweets_response, dict):
                error_message = tweets_response["error"]
            else:
                latest_tweets = tweets_response
        return render_template("index.html", latestTweets=latest_tweets, errorMessage=error_message)

    def getLatestTweets(username):
        payload = {"screen_name": username, "count": 10}
        try:
            # make api call and get response
            response = oauth.get(twitter_latest_tweets_url, params=payload)
            response_data = response.json()
            # if response has error
            if response.status_code != 200:
                if "error" in response_data:
                    return {"error": response_data["error"]}
                if "errors" in response_data:
                    return {"error": response_data["errors"][0]["message"]}
            # if response is "OK"
            result = []
            for data in response_data:
                result.append({"created_at": data["created_at"], "text": data["text"]})
            return result
        # if there is an exception
        except Exception as e:
            app.logger.error(e)
            return {"error": e}
    return app

if __name__ == "__main__":
    app = create_app()
    app.run()

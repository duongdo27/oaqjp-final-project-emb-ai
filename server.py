"""
Emotion Detection Server
"""

from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detector

app = Flask("Emotion Detection")

@app.route('/emotionDetector', methods=["GET"])
def emotion_analysis() -> str:
    """ Analyze text and return emotion detection (analysis result) """
    text_to_analyze = request.args["textToAnalyze"]
    analysis_result = emotion_detector(text_to_analyze)

    # Required output format:
    # For the given statement, the system response is '<emotion1>': <score1>,
    # '<emotion2>': <score2>, '<emotionN>': <scoreN>. The dominant emotion is <emotion>.
    #
    # Required output format when dominant_emotion == None:
    # Invalid text! Please try again.
    if analysis_result["dominant_emotion"] is None:
        response = "Invalid text! Please try again!"
    else:
        response = "For the given statement, the system response is"

        for key, value in analysis_result.items():
            # dominant emotion is mentioned separately as its own sentence.
            if key != "dominant_emotion":
                response += f" '{key}': {value},"
        # Replace last comma with point. If index is -1, no commas found.
        last_comma_index = response.rfind(",")
        if last_comma_index != -1:
            response = response[:last_comma_index] + '.' + response[last_comma_index + 1:]
        response += f" The dominant emotion is {analysis_result['dominant_emotion']}."
    return response

@app.route("/")
def render_index_page():
    ''' This function initiates the rendering of the main application
        page over the Flask channel
    '''
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

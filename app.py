from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

# Get the absolute path to the data.csv file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'data.csv')

@app.route('/api/analysis')
def get_analysis():
    try:
        # Check if file exists
        if not os.path.exists(DATA_FILE):
            return jsonify({'error': 'Data file not found'}), 404

        # Read the CSV file
        df = pd.read_csv(DATA_FILE)
        
        # Calculate intensity analysis
        intensity_stats = {
            'averageIntensity': float(df['intensity'].mean()),
            'maxIntensity': float(df['intensity'].max()),
            'minIntensity': float(df['intensity'].min()),
            'intensityDistribution': [
                {'label': 'Low', 'value': int(len(df[df['intensity'] < 3]))},
                {'label': 'Medium', 'value': int(len(df[(df['intensity'] >= 3) & (df['intensity'] < 7)]))},
                {'label': 'High', 'value': int(len(df[df['intensity'] >= 7]))}
            ]
        }
        
        # Calculate relevance analysis
        relevance_stats = {
            'averageRelevance': float(df['relevance'].mean()),
            'maxRelevance': float(df['relevance'].max()),
            'minRelevance': float(df['relevance'].min()),
            'relevanceDistribution': [
                {'label': 'Low', 'value': int(len(df[df['relevance'] < 3]))},
                {'label': 'Medium', 'value': int(len(df[(df['relevance'] >= 3) & (df['relevance'] < 7)]))},
                {'label': 'High', 'value': int(len(df[df['relevance'] >= 7]))}
            ]
        }
        
        # Calculate topic distribution
        topic_counts = df['topic'].value_counts()
        topic_stats = {
            'totalTopics': int(len(topic_counts)),
            'mostCommonTopic': str(topic_counts.index[0]),
            'topicCoverage': float((len(topic_counts) / len(df)) * 100),
            'topicDistribution': [
                {'label': str(topic), 'value': int(count), 'color': f'#{hash(str(topic)) & 0xFFFFFF:06x}'}
                for topic, count in topic_counts.head(5).items()
            ]
        }
        
        # Calculate summary statistics
        summary_stats = {
            'totalArticles': int(len(df)),
            'averageLength': float(df['title'].str.len().mean()),
            'dataCoverage': float((len(df) / 1000) * 100),  # Assuming total possible articles is 1000
            'trendData': [
                {'label': 'Jan', 'value': int(len(df[df['published_date'].str.contains('2023-01')]))},
                {'label': 'Feb', 'value': int(len(df[df['published_date'].str.contains('2023-02')]))},
                {'label': 'Mar', 'value': int(len(df[df['published_date'].str.contains('2023-03')]))},
                {'label': 'Apr', 'value': int(len(df[df['published_date'].str.contains('2023-04')]))},
                {'label': 'May', 'value': int(len(df[df['published_date'].str.contains('2023-05')]))}
            ]
        }
        
        return jsonify({
            'intensity': intensity_stats,
            'relevance': relevance_stats,
            'topics': topic_stats,
            'summary': summary_stats
        })
        
    except Exception as e:
        print(f"Error in get_analysis: {str(e)}")  # Add logging
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 
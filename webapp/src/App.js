import React, { useState } from 'react';
import axios from 'axios';
// import logo from './TTB.png';
import './App.css';

function App() {
  const [tweetIdea, setTweetIdea] = useState('');
  const [generatedTweet, setGeneratedTweet] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [darkMode, setDarkMode] = useState(true);

  const handleTweetIdeaChange = (e) => {
    setTweetIdea(e.target.value);
  }

  const handleGenerateTweet = () => {
    setIsLoading(true);
    setGeneratedTweet(null);
    // Send the tweet idea to the server to generate a tweet
    axios.post('http://localhost:8080/generate-banger', {originalText: tweetIdea})
    .then(response => {
      if (response.status !== 200) {
        throw new Error(`Request failed with status code ${response.status}`);
      }
      return response.data;
    })
    .then(data => {
      setGeneratedTweet(data);
      setIsLoading(false);
    })
    .catch(error => {
      console.error('An error occurred:', error);
      setIsLoading(false);
    });
  };

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
    if (darkMode) {
      document.documentElement.style.setProperty('--background-color', 'var(--light-background-color)');
      document.documentElement.style.setProperty('--text-color', 'var(--light-text-color)');
      document.documentElement.style.setProperty('--panel-background', 'var(--light-panel-background)');
    } else {
      document.documentElement.style.setProperty('--background-color', 'var(--dark-background-color)');
      document.documentElement.style.setProperty('--text-color', 'var(--dark-text-color)');
      document.documentElement.style.setProperty('--panel-background', 'var(--dark-panel-background)');
    }
  };  

  const handleFormSubmit = (e) => {
    e.preventDefault();
    handleGenerateTweet();
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleGenerateTweet();
    }
  };

  return (
    <div className="App">
      <button className="mode-toggle" onClick={toggleDarkMode}>
        {darkMode ? "🌙" : "☀️"}
      </button>
      <header className="App-header">
        <div className="logo-container">
          {/* <img src={logo} className="App-logo" alt="logo" /> */}
          <h1 className="text-logo">text-to-banger</h1>
        </div>
        <div className="content-container">
          <form onSubmit={handleFormSubmit} className="tweet-form"> {/* Wrap everything in a form and attach submit handler */}
            <textarea
              id="tweetIdea"
              value={tweetIdea}
              onChange={handleTweetIdeaChange}
              onKeyDown={handleKeyDown}
              placeholder="What's happening?"
              rows="4"
            />
            <button className="tweet-button" type="submit" disabled={isLoading}>Generate Banger Tweet</button> {/* set type to submit */}
          </form>
          {isLoading && <p>generating a banger...</p>}
          <div className="generated-tweet-container">
            {generatedTweet && (
              <>
                <p>{generatedTweet}</p>
                <a
                  className="tweet-button"
                  href={`https://twitter.com/intent/tweet?text=${encodeURIComponent(generatedTweet)}`}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  Post Banger Tweet
                </a>
              </>
            )}
          </div>
        </div>
      </header>
    </div>
  );
}

export default App;

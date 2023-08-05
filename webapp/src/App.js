import React, { useState } from 'react';
import axios from 'axios';
// import logo from './TTB.png';
import './App.css';

function App() {
  const [tweetIdea, setTweetIdea] = useState('');
  const [generatedTweet, setGeneratedTweet] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [darkMode, setDarkMode] = useState(true); 

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
  };

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

  return (
    <div className={`App ${darkMode ? 'dark-mode' : ''}`}>
        <div className="App-container">
      <header className="App-header">
        <div className="logo-container">
          {/* <img src={logo} className="App-logo" alt="logo" /> */}
          <h1 className="text-logo">text-to-banger</h1>
        </div>
        <div className="content-container"> {/* This new div wraps both the form and the generated tweet container */}
          <div className="tweet-form">
            <textarea
              id="tweetIdea"
              value={tweetIdea}
              onChange={handleTweetIdeaChange}
              placeholder="What's happening?"
              rows="4"
            />
            <button className="tweet-button" onClick={handleGenerateTweet} disabled={isLoading}>Generate Banger Tweet</button>
          </div>
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
      <footer className="App-footer"> {/* Footer containing the dark mode button */}
        <button onClick={toggleDarkMode}>
          {darkMode ? 'Switch to Light Mode' : 'Switch to Dark Mode'}
        </button>
      </footer>
      </div>
    </div>
  );
}

export default App;

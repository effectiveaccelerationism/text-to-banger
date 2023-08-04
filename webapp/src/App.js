import React, { useState } from 'react';
import logo from './TTBwordmark.png';
import axios from 'axios';
import './App.css';

function App() {
  const [tweetIdea, setTweetIdea] = useState('');
  const [generatedTweet, setGeneratedTweet] = useState(null);
  const [errorMessage, setErrorMessage] = useState(null);

  const handleTweetIdeaChange = (e) => {
    setTweetIdea(e.target.value);
  }

  const handleGenerateTweet = () => {
    const tweet = axios.post('http://localhost:8080/generateBanger', {originalText: tweetIdea}).then((response) => {
      setGeneratedTweet(`${response.data}`);
      setErrorMessage(null);
    }).catch((error) => {
      setErrorMessage('Error generating banger. Please try again later.');
    });
  }

  return (
    <div className="App">
    <header className="App-header">
      <img src={logo} className="App-logo" alt="logo" />
      <div className="tweet-form">
        <textarea
          id="tweetIdea"
          value={tweetIdea}
          onChange={handleTweetIdeaChange}
          placeholder="What's happening?"
          rows="4"
        />
        <button className="tweet-button" onClick={handleGenerateTweet}>Generate Banger Tweet</button>
      </div>
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
      {errorMessage && ( 
        <p className="error-text">{errorMessage}</p>
      )}
    </header>
  </div>
  );
}

export default App;


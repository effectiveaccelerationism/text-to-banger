import React, { useState } from 'react';
import logo from './TTBwordmark.png';
import './App.css';

function App() {
  const [tweetIdea, setTweetIdea] = useState('');
  const [generatedTweet, setGeneratedTweet] = useState(null);

  const handleTweetIdeaChange = (e) => {
    setTweetIdea(e.target.value);
  }

  const handleGenerateTweet = () => {
    // Here you can add logic to transform the tweet idea into a "banger" tweet
    // For now, we'll just prepend "Banger Tweet: " to the input
    setGeneratedTweet(`${tweetIdea}`);
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
    </header>
  </div>
  );
}

export default App;


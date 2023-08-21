import "./App.css";
import React, { useState } from "react";
import axios from "axios";
import QRCode from "qrcode.react";

function App() {
  const [tweetIdea, setTweetIdea] = useState("");
  const [generatedTweet, setGeneratedTweet] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [darkMode, setDarkMode] = useState(true);
  const [contentType, setContentType] = useState("stocks");
  const [balance, setBalance] = useState(10);
  const [showQRCode, setShowQRCode] = useState(false);

  const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8080";

  const handleTweetIdeaChange = (e) => setTweetIdea(e.target.value);
  const handleGenerateTweet = () => {
    if (balance <= 0) {
      setShowQRCode(true);
      return;
    }
    setIsLoading(true);
    setGeneratedTweet(null);

    axios
      .post(`${API_URL}/generate-banger`, {
        originalText: tweetIdea,
        contentType,
      })
      .then((response) => response.data)
      .then((data) => {
        setGeneratedTweet(data);
        setBalance(balance - 1);
      })
      .catch(() => setGeneratedTweet("Error generating banger tweet."))
      .finally(() => setIsLoading(false));
  };

  const toggleDarkMode = () => setDarkMode(!darkMode);

  const handleFormSubmit = (e) => {
    e.preventDefault();
    handleGenerateTweet();
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleGenerateTweet();
    }
  };

  const handlePaymentRedirect = () => {
    window.location.href = 'https://buy.stripe.com/00gaGE0mDd4o6K46oo';
  };

  return (
    <div className="App">
      <button className="mode-toggle" onClick={toggleDarkMode}>
        {darkMode ? "🌙" : "☀️"}
      </button>
      <header className="App-header">
        <h1 className="text-logo">intern.gg</h1>
        <div className="content-container">
          <div className="balance-container">
            <p>Your balance: <span className="coin-balance">{balance}</span> coins</p>
          </div>
          {showQRCode ? (
            <>
              <h2 className="action-title"><u><a href="https://buy.stripe.com/00gaGE0mDd4o6K46oo" target="_blank" rel="noopener noreferrer">Subscribe</a></u> for unlimited coins.</h2>
              <div className="button-container">
                <button className="tweet-button" onClick={handlePaymentRedirect}>Subscribe</button>
              </div>
            </>
          ) : (
            <>
              <form onSubmit={handleFormSubmit} className="tweet-form">
                <textarea
                  id="tweetIdea"
                  value={tweetIdea}
                  onChange={handleTweetIdeaChange}
                  onKeyDown={handleKeyDown}
                  placeholder="What's happening?"
                  rows="4"
                />
                <button className="tweet-button" type="submit" disabled={isLoading}>
                  {balance > 0 ? "Generate Banger Tweet" : (showQRCode ? "Subscribe" : "Generate Banger Tweet")}
                </button>
              </form>
              {isLoading && <p>generating a banger...</p>}
              <div className="button-container">
                {generatedTweet && (
                  <>
                    <p style={{color: generatedTweet.startsWith("Error") ? "darkred" : "inherit"}}>
                      {generatedTweet}
                    </p>
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
            </>
          )}
        </div>
      </header>
    </div>
  );
}

export default App;

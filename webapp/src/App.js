// React Component (JSX)
import "./App.css";
import React, { useState, useEffect } from "react";
import axios from "axios";
import QRCode from "qrcode.react";

function App() {
  const [tweetIdea, setTweetIdea] = useState("");
  const [generatedTweet, setGeneratedTweet] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [darkMode, setDarkMode] = useState(true); // Initially set to true
  const [contentType, setContentType] = useState("stocks");
  const [balance, setBalance] = useState(10);
  const [showQRCode, setShowQRCode] = useState(false);

  useEffect(() => {
    if (darkMode) {
      document.documentElement.style.setProperty(
        "--logo-text-color",
        "var(--dark-logo-text-color)"
      );
      document.documentElement.style.setProperty(
        "--background-color",
        "var(--dark-background-color)"
      );
      document.documentElement.style.setProperty(
        "--text-color",
        "var(--dark-text-color)"
      );
      document.documentElement.style.setProperty(
        "--panel-background",
        "var(--dark-panel-background)"
      );
      document.documentElement.style.setProperty(
        "--button-background",
        "var(--dark-button-background)"
      );
      document.documentElement.style.setProperty(
        "--button-text",
        "var(--dark-button-text)"
      );
      document.documentElement.style.setProperty(
        "--border-color",
        "var(--dark-border-color)"
      );
    } else {
      document.documentElement.style.setProperty(
        "--logo-text-color",
        "var(--light-logo-text-color)"
      );
      document.documentElement.style.setProperty(
        "--background-color",
        "var(--light-background-color)"
      );
      document.documentElement.style.setProperty(
        "--text-color",
        "var(--light-text-color)"
      );
      document.documentElement.style.setProperty(
        "--panel-background",
        "var(--light-panel-background)"
      );
      document.documentElement.style.setProperty(
        "--button-background",
        "var(--light-button-background)"
      );
      document.documentElement.style.setProperty(
        "--button-text",
        "var(--light-button-text)"
      );
      document.documentElement.style.setProperty(
        "--border-color",
        "var(--light-border-color)"
      );
    }
  }, [darkMode]); // Watch for changes in darkMode state

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
    window.location.href = "https://buy.stripe.com/00gaGE0mDd4o6K46oo";
  };

  const tweetGeneratedContent = () => {
    const tweetUrl = `https://twitter.com/intent/tweet?text=${encodeURIComponent(
      generatedTweet
    )}`;
    window.open(tweetUrl, "_blank");
  };

  return (
    <div className="App">
      <button className="mode-toggle" onClick={toggleDarkMode}>
        {darkMode ? "🌙" : "☀️"}
      </button>

      <header className="App-header">
        <h1 className="text-logo">text-to-banger</h1>
        <div className="content-container">
          {showQRCode ? (
            <>
              <h2 className="action-title">Subscribe for unlimited tweets.</h2>
              <div className="button-container">
                <button
                  className="share-button"
                  onClick={handlePaymentRedirect}
                >
                  Subscribe
                </button>
              </div>
            </>
          ) : (
            <>
              {isLoading && <p>generating a banger...</p>}
              <form onSubmit={handleFormSubmit} className="tweet-form">
                {generatedTweet && <p>{generatedTweet}</p>}
                <button
                  className="tweet-button"
                  type="submit"
                  disabled={isLoading}
                >
                  {balance > 0 ? "Generate Banger Tweet" : "Subscribe"}
                </button>
                {generatedTweet && (
                  <button
                    className="tweet-button"
                    onClick={tweetGeneratedContent}
                  >
                    Share Banger Tweet
                  </button>
                )}
              </form>
            </>
          )}
        </div>
      </header>
      <footer className="App-footer">{/* Footer content */}</footer>
    </div>
  );
}

export default App;

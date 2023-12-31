import React, { useState, useEffect } from "react";
import axios from "axios";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faGithub } from "@fortawesome/free-brands-svg-icons";
import ReactGA from "react-ga";

import "./App.css";

function App() {
  // Initialize Google Analytics
  useEffect(() => {
    ReactGA.initialize("G-SZEJEE5GGC");
    ReactGA.pageview(window.location.pathname);
  }, []);

  const [tweetIdea, setTweetIdea] = useState("");
  const [generatedTweet, setGeneratedTweet] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [darkMode, setDarkMode] = useState(true);
  // const [contentType, setContentType] = useState("stocks");
  const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8080";

  const handleTweetIdeaChange = (e) => setTweetIdea(e.target.value);

  const handleGenerateTweet = () => {
    setIsLoading(true);
    setGeneratedTweet(null);
    ReactGA.event({
      category: "Button",
      action: "Clicked Generate Banger Tweet",
    }); // Track click

    axios
      .post(`${API_URL}/generate-banger`, {
        originalText: tweetIdea,
        // contentType: contentType,
      })
      .then((response) => {
        if (response.status !== 200) {
          throw new Error(`Request failed with status code ${response.status}`);
        }
        return response.data;
      })
      .then((data) => {
        setGeneratedTweet(data);
      })
      .catch((error) => {
        console.error("An error occurred:", error);
        setGeneratedTweet("Error generating banger tweet.");
      })
      .finally(() => {
        setIsLoading(false);
      });
  };

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
    if (darkMode) {
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
      document.documentElement.style.setProperty(
        "--logo-text-color",
        "var(--light-logo-text-color)"
      );
    } else {
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
      document.documentElement.style.setProperty(
        "--logo-text-color",
        "var(--dark-logo-text-color)"
      );
    }
  };

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

  return (
    <div className="App">
      <div className="icon-container">
        <a
          href="https://github.com/effectiveaccelerationism/text-to-banger"
          target="_blank"
          rel="noopener noreferrer"
        >
          <button className="custom-button custom-icon">
            <FontAwesomeIcon icon={faGithub} color="grey" />
          </button>
        </a>

        <button className="mode-toggle" onClick={toggleDarkMode}>
          {darkMode ? "🌙" : "☀️"}
        </button>
      </div>
      <header className="App-header">
        <div className="logo-container">
          {/* <img src={logo} className="App-logo" alt="logo" /> */}
          <h1 className="text-logo">text-to-banger</h1>
        </div>
        <div className="content-container">
          <form onSubmit={handleFormSubmit} className="tweet-form">
            <textarea
              id="tweetIdea"
              value={tweetIdea}
              onChange={handleTweetIdeaChange}
              onKeyDown={handleKeyDown}
              placeholder="What's happening?"
              rows="4"
            />
          </form>
          <button
            className="tweet-button generate-button"
            onClick={handleGenerateTweet}
            disabled={isLoading}
          >
            Generate Banger Tweet
          </button>
          {isLoading && <p>generating a banger...</p>}
          <div className="generated-tweet-container">
            {generatedTweet && (
              <>
                <p
                  style={{
                    color: generatedTweet.startsWith("Error")
                      ? "darkred"
                      : "inherit",
                  }}
                >
                  {generatedTweet}
                </p>
                {!generatedTweet.startsWith("Error") && (
                  <a
                    className="tweet-button"
                    onClick={() =>
                      ReactGA.event({
                        category: "Button",
                        action: "Clicked Post Banger Tweet",
                      })
                    } // Track click
                    href={`https://twitter.com/intent/tweet?text=${encodeURIComponent(
                      generatedTweet
                    )}`}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    Post Banger Tweet
                  </a>
                )}
              </>
            )}
          </div>
        </div>
      </header>
    </div>
  );
}

export default App;

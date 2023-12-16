import React, { useState } from 'react';
import './App.css';

function App() {
  const [userInput, setUserInput] = useState('');
  const [chatMessages, setChatMessages] = useState([]);
  const [restaurants, setRestaurants] = useState({ suggestions: [], visited: [] });
  const [visitedPage, setVisitedPage] = useState(0);

  const itemsPerPage = 5;  // Adjust as needed
  const visitedPerPage = 5; // Currently not used but declared for future use

  // ... (Other functions and state variables)
  const sendMessageToBot = async (message) => {
    try {
      const response = await fetch('http://127.0.0.1:5000/api/chatbot', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message }),
      });

      const data = await response.json();
      const id1 = data.id.toString();
      fetchRestaurantDetails(id1);
      
      const description = data.reply[1].description;
      const address = data.reply[1].address;
      const restaurantName = data.reply[1].name;

      const botReplyDescription = `Aprašymas: ${description}`;
      const botReplyAddress = `Adresas: ${address}`;
      const botReplyRestaurantName = `Restorano pavadinimas: ${restaurantName}`;

      setChatMessages([
        ...chatMessages,
        { text: message, sender: 'user' },
        { text: botReplyDescription, sender: 'bot' },
        { text: botReplyAddress, sender: 'bot' },
        { text: botReplyRestaurantName, sender: 'bot' },
      ]);
    } catch (error) {
      console.error('Error sending message to bot:', error);
      setChatMessages([
        ...chatMessages,
        { text: message, sender: 'user' },
        { text: 'Failed to get a response from the chatbot.', sender: 'bot' },
      ]);
    }
  };
  const fetchRestaurantDetails = async (restaurantId) => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/api/restaurants/${restaurantId}`);
      const restaurantDetails = await response.json();
      const url = restaurantDetails.url;
      const name = restaurantDetails.name;
      const id = restaurantDetails.id;

      const restaurant = { url, name, id };

      setRestaurants(prevRestaurants => ({
        ...prevRestaurants,
        suggestions: [...prevRestaurants.suggestions, 
          {
            id: restaurant.id,
            name: restaurant.name,
            image_url: restaurant.url,
          },
        ],
      }));
    } catch (error) {
      console.error('Error fetching restaurant details:', error);
    }
  };

  const handleUserInput = (e) => {
    setUserInput(e.target.value);
  };

  const handleSendMessage = () => {
    if (!userInput.trim()) return;
    sendMessageToBot(userInput);
    setUserInput('');
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSendMessage();
    }
  };

  const changeSuggestionPage = (direction) => {
    const totalPages = Math.ceil(restaurants.suggestions.length / itemsPerPage);
    setRestaurants(prevPage => {
      if (direction === "next") {
        return (prevPage + 1) % totalPages;
      } else {
        return (prevPage - 1 + totalPages) % totalPages;
      }
    });
  };

  const changeVisitedPage = (direction) => {
    const totalPages = Math.ceil(restaurants.visited.length / visitedPerPage);
    setVisitedPage(prevPage => {
      if (direction === "next") {
        return (prevPage + 1) % totalPages;
      } else {
        return (prevPage - 1 + totalPages) % totalPages;
      }
    });
  };

  const displayedVisited = restaurants.visited.slice(
    visitedPage * visitedPerPage,
    (visitedPage + 1) * visitedPerPage
  );

  function changeLanguage(lang) {
   return;
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>TABLEO</h1>
        <div className="language-icons">
          <div className="language-icon" onClick={() => changeLanguage('en')}>
            🇬🇧
          </div>
          <div className="language-icon" onClick={() => changeLanguage('lt')}>
            🇱🇹
          </div>
        </div>
      </header>
      <div className="App-content">
        <div className="chatbot-container">
          <div className="chat-messages">
            {chatMessages.map((msg, index) => (
              <div key={index} className={`chat-message ${msg.sender}`}>{msg.text}</div>
            ))}
          </div>
          <div className="chat-input-container">
            <input
              type="text"
              className="chat-input"
              placeholder="Type a message..."
              value={userInput}
              onChange={handleUserInput}
              onKeyPress={handleKeyPress}
            />
            <button className="chat-send-button" onClick={handleSendMessage}>Send</button>
          </div>
        </div>
        <div className="suggestions-section">
          <h2 className="section-title">Suggestions</h2>

          <div className="suggestions-container">
            <div className="suggestions">
            {restaurants.suggestions.map(suggestion => (
              <div key={suggestion.id} className="restaurant-card">
                <a href={suggestion.image_url} target="_blank" rel="noopener noreferrer">
                  <img src={suggestion.image_url} alt={suggestion.name} />
                </a>
                <div className="restaurant-name">{suggestion.name}</div>
              </div>
            ))}
            </div>
          </div>
          <h2 className="section-title">Visited</h2>

          <div className="visited-container">
            <div className="visited">
              {displayedVisited.map(restaurant => (
                <div key={restaurant.id} className="restaurant-card">
                  <img src={restaurant.image_url} alt={restaurant.name} />
                  <div className="restaurant-name">{restaurant.name}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;

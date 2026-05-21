import { useState } from 'react';
import { UserProvider } from './context/UserContext';
import HomePage from './pages/HomePage';
import PostDetailsPage from './pages/PostDetailsPage';

const App = () => {
  const [currentView, setCurrentView] = useState('home');
  const [selectedPostId, setSelectedPostId] = useState(null);

  const handleViewPostDetails = (postId) => {
    setSelectedPostId(postId);
    setCurrentView('details');
  };

  const handleBackToHome = () => {
    setCurrentView('home');
    setSelectedPostId(null);
  };

  return (
    <UserProvider>
      {currentView === 'home' ? (
        <HomePage onViewPostDetails={handleViewPostDetails} />
      ) : (
        <PostDetailsPage postId={selectedPostId} onBack={handleBackToHome} />
      )}
    </UserProvider>
  );
};

export default App;

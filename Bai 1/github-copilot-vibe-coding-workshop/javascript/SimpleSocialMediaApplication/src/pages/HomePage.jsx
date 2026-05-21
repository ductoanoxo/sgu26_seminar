import { useState, useEffect } from 'react';
import { useUser } from '../context/UserContext';
import apiClient, { ApiError } from '../api/apiClient';
import PostCard from '../components/PostCard';
import PostModal from '../components/PostModal';
import UsernameModal from '../components/UsernameModal';

const HomePage = ({ onViewPostDetails }) => {
  const { username } = useUser();
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [isPostModalOpen, setIsPostModalOpen] = useState(false);
  const [isUsernameModalOpen, setIsUsernameModalOpen] = useState(false);

  useEffect(() => {
    loadPosts();
  }, []);

  const loadPosts = async () => {
    setLoading(true);
    setError('');
    try {
      const data = await apiClient.getPosts();
      setPosts(data);
    } catch (err) {
      if (err instanceof ApiError) {
        setError(`Backend API unavailable: ${err.message}`);
      } else {
        setError('Backend API is unreachable. Please check if the server is running.');
      }
    } finally {
      setLoading(false);
    }
  };

  const handlePostCreated = (newPost) => {
    setPosts((prev) => [newPost, ...prev]);
  };

  const handlePostUpdate = (updatedPost) => {
    setPosts((prev) =>
      prev.map((post) => (post.id === updatedPost.id ? updatedPost : post))
    );
  };

  const handlePostDelete = (postId) => {
    setPosts((prev) => prev.filter((post) => post.id !== postId));
  };

  const handleCreatePost = () => {
    if (!username) {
      setIsUsernameModalOpen(true);
      return;
    }
    setIsPostModalOpen(true);
  };

  const filteredPosts = posts.filter(
    (post) =>
      post.content.toLowerCase().includes(searchQuery.toLowerCase()) ||
      post.username.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-white shadow-sm sticky top-0 z-10">
        <div className="max-w-4xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between mb-4">
            <h1 className="text-2xl font-bold text-blue-600">Simple Social Media</h1>
            {username ? (
              <div className="flex items-center gap-3">
                <span className="text-gray-700">👤 {username}</span>
                <button
                  onClick={() => setIsUsernameModalOpen(true)}
                  className="text-sm text-blue-500 hover:text-blue-700"
                >
                  Change
                </button>
              </div>
            ) : (
              <button
                onClick={() => setIsUsernameModalOpen(true)}
                className="px-4 py-2 text-white bg-blue-500 rounded-lg hover:bg-blue-600 transition"
              >
                Set Username
              </button>
            )}
          </div>

          {/* Search Bar */}
          <div className="relative">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search posts or users..."
              className="w-full px-4 py-2 pl-10 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <svg
              className="absolute left-3 top-3 w-5 h-5 text-gray-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
              />
            </svg>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-4 py-6">
        {/* Create Post Button */}
        <button
          onClick={handleCreatePost}
          className="w-full mb-6 px-4 py-3 text-left text-gray-500 bg-white rounded-lg shadow hover:shadow-md transition"
        >
          What's on your mind?
        </button>

        {/* Error Message */}
        {error && (
          <div className="mb-6 p-4 bg-red-100 text-red-700 rounded-lg flex items-start gap-3">
            <svg className="w-6 h-6 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
              <path
                fillRule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                clipRule="evenodd"
              />
            </svg>
            <div>
              <p className="font-semibold">Error</p>
              <p>{error}</p>
            </div>
          </div>
        )}

        {/* Loading State */}
        {loading && (
          <div className="text-center py-12">
            <div className="inline-block w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin" />
            <p className="mt-4 text-gray-600">Loading posts...</p>
          </div>
        )}

        {/* Posts List */}
        {!loading && !error && filteredPosts.length === 0 && (
          <div className="text-center py-12 text-gray-500">
            {searchQuery ? 'No posts found matching your search.' : 'No posts yet. Be the first to post!'}
          </div>
        )}

        {!loading && !error && filteredPosts.length > 0 && (
          <div>
            {filteredPosts.map((post) => (
              <PostCard
                key={post.id}
                post={post}
                onUpdate={handlePostUpdate}
                onDelete={handlePostDelete}
                onViewDetails={onViewPostDetails}
              />
            ))}
          </div>
        )}
      </main>

      {/* Modals */}
      <PostModal
        isOpen={isPostModalOpen}
        onClose={() => setIsPostModalOpen(false)}
        onPostCreated={handlePostCreated}
      />
      <UsernameModal
        isOpen={isUsernameModalOpen}
        onClose={() => setIsUsernameModalOpen(false)}
      />
    </div>
  );
};

export default HomePage;

import { useState } from 'react';
import { useUser } from '../context/UserContext';
import apiClient from '../api/apiClient';

const PostCard = ({ post, onUpdate, onDelete, onViewDetails }) => {
  const { username } = useUser();
  const [isLiking, setIsLiking] = useState(false);

  const handleLike = async () => {
    if (!username || isLiking) return;

    setIsLiking(true);
    try {
      await apiClient.likePost(post.id, username);
      // Fetch updated post to get new like count
      const updatedPost = await apiClient.getPostById(post.id);
      onUpdate(updatedPost);
    } catch (err) {
      console.error('Failed to like post:', err);
    } finally {
      setIsLiking(false);
    }
  };

  const handleUnlike = async () => {
    if (!username || isLiking) return;

    setIsLiking(true);
    try {
      await apiClient.unlikePost(post.id, username);
      // Fetch updated post to get new like count
      const updatedPost = await apiClient.getPostById(post.id);
      onUpdate(updatedPost);
    } catch (err) {
      console.error('Failed to unlike post:', err);
    } finally {
      setIsLiking(false);
    }
  };

  const handleDelete = async () => {
    if (!confirm('Are you sure you want to delete this post?')) return;

    try {
      await apiClient.deletePost(post.id);
      onDelete(post.id);
    } catch (err) {
      console.error('Failed to delete post:', err);
      alert('Failed to delete post');
    }
  };

  const isOwnPost = username === post.username;

  return (
    <div className="bg-white rounded-lg shadow-md p-6 mb-4 hover:shadow-lg transition">
      <div className="flex items-start justify-between mb-4">
        <div>
          <h3 className="font-bold text-lg">{post.username}</h3>
          <p className="text-sm text-gray-500">
            {new Date(post.createdAt).toLocaleString()}
          </p>
        </div>
        {isOwnPost && (
          <button
            onClick={handleDelete}
            className="text-red-500 hover:text-red-700 transition"
            aria-label="Delete post"
          >
            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
          </button>
        )}
      </div>

      <p className="text-gray-800 mb-4 whitespace-pre-wrap">{post.content}</p>

      <div className="flex items-center gap-6 text-gray-600">
        <div className="flex items-center gap-2">
          <button
            onClick={handleLike}
            disabled={!username || isLiking}
            className="flex items-center gap-1 hover:text-red-500 transition disabled:opacity-50 disabled:cursor-not-allowed"
            aria-label="Like post"
            title="Like post"
          >
            <svg
              className="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"
              />
            </svg>
          </button>
          <span className="font-semibold">{post.likesCount}</span>
          <button
            onClick={handleUnlike}
            disabled={!username || isLiking}
            className="flex items-center text-xs hover:text-blue-500 transition disabled:opacity-50 disabled:cursor-not-allowed ml-1"
            aria-label="Unlike post"
            title="Unlike post"
          >
            (unlike)
          </button>
        </div>

        <button
          onClick={() => onViewDetails(post.id)}
          className="flex items-center gap-2 hover:text-blue-500 transition"
          aria-label="View comments"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
            />
          </svg>
          <span>Comments</span>
        </button>
      </div>
    </div>
  );
};

export default PostCard;

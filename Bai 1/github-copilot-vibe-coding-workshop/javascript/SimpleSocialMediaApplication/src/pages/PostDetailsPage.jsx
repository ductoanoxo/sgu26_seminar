import { useState, useEffect } from 'react';
import { useUser } from '../context/UserContext';
import apiClient from '../api/apiClient';
import CommentItem from '../components/CommentItem';

const PostDetailsPage = ({ postId, onBack }) => {
  const { username } = useUser();
  const [post, setPost] = useState(null);
  const [comments, setComments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [commentContent, setCommentContent] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isLiking, setIsLiking] = useState(false);

  useEffect(() => {
    loadPostDetails();
  }, [postId]);

  const loadPostDetails = async () => {
    setLoading(true);
    setError('');
    try {
      const [postData, commentsData] = await Promise.all([
        apiClient.getPostById(postId),
        apiClient.getCommentsByPostId(postId),
      ]);
      setPost(postData);
      setComments(commentsData);
    } catch (err) {
      setError(err.message || 'Failed to load post details');
    } finally {
      setLoading(false);
    }
  };

  const handleLike = async () => {
    if (!username || isLiking || !post) return;

    setIsLiking(true);
    try {
      await apiClient.likePost(post.id, username);
      // Fetch updated post to get new like count
      const updatedPost = await apiClient.getPostById(post.id);
      setPost(updatedPost);
    } catch (err) {
      console.error('Failed to like post:', err);
    } finally {
      setIsLiking(false);
    }
  };

  const handleUnlike = async () => {
    if (!username || isLiking || !post) return;

    setIsLiking(true);
    try {
      await apiClient.unlikePost(post.id, username);
      // Fetch updated post to get new like count
      const updatedPost = await apiClient.getPostById(post.id);
      setPost(updatedPost);
    } catch (err) {
      console.error('Failed to unlike post:', err);
    } finally {
      setIsLiking(false);
    }
  };

  const handleAddComment = async (e) => {
    e.preventDefault();
    if (!username || !commentContent.trim()) return;

    setIsSubmitting(true);
    try {
      const newComment = await apiClient.createComment(postId, {
        username,
        content: commentContent.trim(),
      });
      setComments([...comments, newComment]);
      setCommentContent('');
    } catch (err) {
      alert('Failed to add comment');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleCommentUpdate = (updatedComment) => {
    setComments(
      comments.map((comment) =>
        comment.id === updatedComment.id ? updatedComment : comment
      )
    );
  };

  const handleCommentDelete = (commentId) => {
    setComments(comments.filter((comment) => comment.id !== commentId));
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin" />
          <p className="mt-4 text-gray-600">Loading post...</p>
        </div>
      </div>
    );
  }

  if (error || !post) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-600 mb-4">{error || 'Post not found'}</p>
          <button
            onClick={onBack}
            className="px-4 py-2 text-white bg-blue-500 rounded-lg hover:bg-blue-600"
          >
            Go Back
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-white shadow-sm sticky top-0 z-10">
        <div className="max-w-4xl mx-auto px-4 py-4 flex items-center gap-4">
          <button
            onClick={onBack}
            className="p-2 hover:bg-gray-100 rounded-full transition"
            aria-label="Go back"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M10 19l-7-7m0 0l7-7m-7 7h18"
              />
            </svg>
          </button>
          <h1 className="text-xl font-bold">Post Details</h1>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-4 py-6">
        {/* Post */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <div className="mb-4">
            <h3 className="font-bold text-lg">{post.username}</h3>
            <p className="text-sm text-gray-500">
              {new Date(post.createdAt).toLocaleString()}
            </p>
          </div>

          <p className="text-gray-800 mb-4 whitespace-pre-wrap text-lg">{post.content}</p>

          <div className="flex items-center gap-6 text-gray-600">
            <div className="flex items-center gap-2">
              <button
                onClick={handleLike}
                disabled={!username || isLiking}
                className="flex items-center gap-1 hover:text-red-500 transition disabled:opacity-50"
                title="Like post"
              >
                <svg
                  className="w-6 h-6"
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
                className="text-xs hover:text-blue-500 transition disabled:opacity-50 ml-1"
                title="Unlike post"
              >
                (unlike)
              </button>
            </div>
          </div>
        </div>

        {/* Add Comment */}
        {username ? (
          <form onSubmit={handleAddComment} className="bg-white rounded-lg shadow-md p-4 mb-6">
            <textarea
              value={commentContent}
              onChange={(e) => setCommentContent(e.target.value)}
              placeholder="Write a comment..."
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 mb-3"
              rows={3}
              required
              disabled={isSubmitting}
            />
            <button
              type="submit"
              disabled={isSubmitting || !commentContent.trim()}
              className="px-4 py-2 text-white bg-blue-500 rounded-lg hover:bg-blue-600 transition disabled:opacity-50"
            >
              {isSubmitting ? 'Posting...' : 'Add Comment'}
            </button>
          </form>
        ) : (
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-6 text-center">
            <p className="text-yellow-800">Please set your username to comment</p>
          </div>
        )}

        {/* Comments */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-lg font-bold mb-4">
            Comments ({comments.length})
          </h2>
          {comments.length === 0 ? (
            <p className="text-gray-500 text-center py-8">
              No comments yet. Be the first to comment!
            </p>
          ) : (
            <div>
              {comments.map((comment) => (
                <CommentItem
                  key={comment.id}
                  comment={comment}
                  postId={postId}
                  onUpdate={handleCommentUpdate}
                  onDelete={handleCommentDelete}
                />
              ))}
            </div>
          )}
        </div>
      </main>
    </div>
  );
};

export default PostDetailsPage;

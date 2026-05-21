import { useState } from 'react';
import { useUser } from '../context/UserContext';
import apiClient from '../api/apiClient';

const CommentItem = ({ comment, postId, onUpdate, onDelete }) => {
  const { username } = useUser();
  const [isEditing, setIsEditing] = useState(false);
  const [editContent, setEditContent] = useState(comment.content);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const isOwnComment = username === comment.username;

  const handleUpdate = async (e) => {
    e.preventDefault();
    if (!editContent.trim()) return;

    setIsSubmitting(true);
    try {
      const updated = await apiClient.updateComment(postId, comment.id, {
        username,
        content: editContent.trim(),
      });
      onUpdate(updated);
      setIsEditing(false);
    } catch (err) {
      console.error('Failed to update comment:', err);
      alert('Failed to update comment');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleDelete = async () => {
    if (!confirm('Are you sure you want to delete this comment?')) return;

    try {
      await apiClient.deleteComment(postId, comment.id);
      onDelete(comment.id);
    } catch (err) {
      console.error('Failed to delete comment:', err);
      alert('Failed to delete comment');
    }
  };

  return (
    <div className="bg-gray-50 rounded-lg p-4 mb-3">
      <div className="flex items-start justify-between mb-2">
        <div>
          <span className="font-semibold text-sm">{comment.username}</span>
          <span className="text-xs text-gray-500 ml-2">
            {new Date(comment.createdAt).toLocaleString()}
          </span>
        </div>
        {isOwnComment && !isEditing && (
          <div className="flex gap-2">
            <button
              onClick={() => setIsEditing(true)}
              className="text-blue-500 hover:text-blue-700 text-sm"
            >
              Edit
            </button>
            <button
              onClick={handleDelete}
              className="text-red-500 hover:text-red-700 text-sm"
            >
              Delete
            </button>
          </div>
        )}
      </div>

      {isEditing ? (
        <form onSubmit={handleUpdate} className="mt-2">
          <textarea
            value={editContent}
            onChange={(e) => setEditContent(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
            rows={3}
            required
            disabled={isSubmitting}
          />
          <div className="flex gap-2 mt-2">
            <button
              type="submit"
              disabled={isSubmitting || !editContent.trim()}
              className="px-3 py-1 text-sm text-white bg-blue-500 rounded hover:bg-blue-600 transition disabled:opacity-50"
            >
              {isSubmitting ? 'Saving...' : 'Save'}
            </button>
            <button
              type="button"
              onClick={() => {
                setIsEditing(false);
                setEditContent(comment.content);
              }}
              disabled={isSubmitting}
              className="px-3 py-1 text-sm text-gray-700 bg-gray-200 rounded hover:bg-gray-300 transition"
            >
              Cancel
            </button>
          </div>
        </form>
      ) : (
        <p className="text-gray-800 text-sm whitespace-pre-wrap">{comment.content}</p>
      )}
    </div>
  );
};

export default CommentItem;

const API_BASE_URL = 'http://localhost:8000/api';

export class ApiError extends Error {
  constructor(message, status) {
    super(message);
    this.status = status;
    this.name = 'ApiError';
  }
}

const handleResponse = async (response) => {
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ message: 'Unknown error' }));
    throw new ApiError(errorData.message || `HTTP error ${response.status}`, response.status);
  }
  
  if (response.status === 204) {
    return null;
  }
  
  return response.json();
};

const apiClient = {
  // Posts
  getPosts: async () => {
    const response = await fetch(`${API_BASE_URL}/posts`);
    return handleResponse(response);
  },

  createPost: async (postData) => {
    const response = await fetch(`${API_BASE_URL}/posts`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(postData),
    });
    return handleResponse(response);
  },

  getPostById: async (postId) => {
    const response = await fetch(`${API_BASE_URL}/posts/${postId}`);
    return handleResponse(response);
  },

  updatePost: async (postId, postData) => {
    const response = await fetch(`${API_BASE_URL}/posts/${postId}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(postData),
    });
    return handleResponse(response);
  },

  deletePost: async (postId) => {
    const response = await fetch(`${API_BASE_URL}/posts/${postId}`, {
      method: 'DELETE',
    });
    return handleResponse(response);
  },

  // Comments
  getCommentsByPostId: async (postId) => {
    const response = await fetch(`${API_BASE_URL}/posts/${postId}/comments`);
    return handleResponse(response);
  },

  createComment: async (postId, commentData) => {
    const response = await fetch(`${API_BASE_URL}/posts/${postId}/comments`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(commentData),
    });
    return handleResponse(response);
  },

  getCommentById: async (postId, commentId) => {
    const response = await fetch(`${API_BASE_URL}/posts/${postId}/comments/${commentId}`);
    return handleResponse(response);
  },

  updateComment: async (postId, commentId, commentData) => {
    const response = await fetch(`${API_BASE_URL}/posts/${postId}/comments/${commentId}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(commentData),
    });
    return handleResponse(response);
  },

  deleteComment: async (postId, commentId) => {
    const response = await fetch(`${API_BASE_URL}/posts/${postId}/comments/${commentId}`, {
      method: 'DELETE',
    });
    return handleResponse(response);
  },

  // Likes
  likePost: async (postId, username) => {
    const response = await fetch(`${API_BASE_URL}/posts/${postId}/likes`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username }),
    });
    return handleResponse(response);
  },

  unlikePost: async (postId, username) => {
    const response = await fetch(`${API_BASE_URL}/posts/${postId}/likes`, {
      method: 'DELETE',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username }),
    });
    return handleResponse(response);
  },
};

export default apiClient;

'use client';

import React from 'react';

export default function VideoBackground() {
  return (
    <div className="hero-video-container">
      <video
        className="hero-video"
        src="/6747258-hd_1920_1080_30fps.mp4"
        muted
        playsInline
        autoPlay
        loop
      />
    </div>
  );
}

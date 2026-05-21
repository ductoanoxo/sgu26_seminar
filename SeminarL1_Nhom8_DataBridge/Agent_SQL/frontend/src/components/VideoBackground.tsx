'use client';

import React from 'react';

export default function VideoBackground() {
  return (
    <div className="hero-video-container">
      <video
        className="hero-video"
        src="https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260329_050842_be71947f-f16e-4a14-810c-06e83d23ddb5.mp4"
        muted
        playsInline
        autoPlay
        loop
      />
    </div>
  );
}

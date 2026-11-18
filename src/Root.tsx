import React from 'react';
import { Composition } from 'remotion';
import { KhyberAnimatedDeckAR } from './Composition';
import { PaintWhiteboard9x16 } from './PaintWhiteboard';
import episodeData from '../public/current_episode.json';
import wbData from '../public/current_whiteboard.json';

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="PaintWhiteboard9x16"
        component={PaintWhiteboard9x16}
        durationInFrames={wbData.totalFrames || 3600}
        fps={60}
        width={1080}
        height={1920}
      />
      <Composition
        id="KhyberAnimatedDeckAR"
        component={KhyberAnimatedDeckAR}
        durationInFrames={episodeData.totalFrames || 1800}
        fps={60}
        width={1080}
        height={1920}
      />
    </>
  );
};
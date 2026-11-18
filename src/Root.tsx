import React from 'react';
import { Composition } from 'remotion';
import { KhyberAnimatedDeckAR } from './Composition';
import { ZackDocumentary16x9 } from './DocComposition';
import { VectorExplainer16x9 } from './VectorExplainer';
import { WhiteboardExplainer16x9 } from './WhiteboardExplainer';
import { PaintWhiteboard9x16 } from './PaintWhiteboard';
import episodeData from '../public/current_episode.json';
import docData from '../public/current_doc.json';
import vecData from '../public/current_vector.json';
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
      <Composition
        id="ZackDocumentary16x9"
        component={ZackDocumentary16x9}
        durationInFrames={docData.totalFrames || 2400}
        fps={60}
        width={1920}
        height={1080}
      />
      <Composition
        id="VectorExplainer16x9"
        component={VectorExplainer16x9}
        durationInFrames={vecData.totalFrames || 1800}
        fps={60}
        width={1920}
        height={1080}
      />
      <Composition
        id="WhiteboardExplainer16x9"
        component={WhiteboardExplainer16x9}
        durationInFrames={wbData.totalFrames || 3600}
        fps={60}
        width={1920}
        height={1080}
      />
    </>
  );
};
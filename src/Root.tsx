import React from "react";
import { Composition } from "remotion";
import { KhyberAnimatedDeckAR, AnimatedDeckProps } from "./Composition";
import episodeData from "../public/current_episode.json";

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="KhyberAnimatedDeckAR"
      component={KhyberAnimatedDeckAR}
      durationInFrames={episodeData.totalFrames || 2520}
      fps={60}
      width={1080}
      height={1920}
      defaultProps={episodeData as AnimatedDeckProps}
    />
  );
};
